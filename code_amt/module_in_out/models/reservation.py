# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

list_state = [
    ('draft', u'Borrador'),
    ('in_process', u'En trámite'),
    ('done', u'Realizado'),
    ('cancel', u'Cancelado')]

list_state_line = [
    ('draft', u'Borrador'),
    ('wait', u'En espera'),
    ('approved', u'Aprobado'),
    ('circulation', u'En circulación'),
    ('re_entry', u'Reingreso'),
    ('denied', u'Negado'),
    ('cancel', u'Cancelado')]

class Reservation(models.Model):
    _name = 'reservation'
    _inherit = ['mail.thread']
    _description = u'Tramite para la reservación de vehículos'
    _order = "date desc, name desc, id desc"


    name = fields.Char(string=u'Código', size=150, default='Nuevo', readonly=True, help=u'Código o nombre del documento unico que identifición.')
    authorized_id = fields.Many2one('res.partner', string=u'Autorizado por', required=True, readonly=True, states={'draft': [('readonly', False)]}, help=u'Asigna a la persona responsable que autoriza el documento.')
    elaborared_id = fields.Many2one('res.partner', string=u'Elaborado por', required=True, readonly=True, states={'draft': [('readonly', False)]}, help=u'Asigna la persona responsable en elaborar el documento.', track_visibility='always')
    applicant_id = fields.Many2one('res.partner', string=u'Solicitante', required=True, readonly=True, states={'draft': [('readonly', False)]},
                               help=u'Asigna a la persona que estara a cargo de los vehiculos.', track_visibility='always')
    date = fields.Date(string=u'Fecha', required=True, default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]}, help=u'Fecha en que se elabora el documento.')
    comment = fields.Text(string=u'Descripción', readonly=True, states={'draft': [('readonly', False)]}, help=u'Escribe un texto relacionado al documento.')
    state = fields.Selection(selection=list_state, string=u'Estado', default='draft', index=True, readonly=True, 
                             track_visibility='onchange', copy=False, help=u'Etapas del documento.')
    company_id = fields.Many2one('res.company', string=u'Compañia', readonly=True, states={'draft': [('readonly', False)]}, 
                                 default=lambda self: self.env.user.company_id)
    reservation_line_ids = fields.One2many('reservation.line', 'reservation_id', string=u'Lineas reservación', readonly=True, states={'draft': [('readonly', False)]}, copy=True)

    
    @api.multi
    def action_process(self):
        self.name = self.env['ir.sequence'].with_context(ir_sequence_date=self.date).next_by_code('sequence.reservation')
        for line in self.reservation_line_ids:
            values = self._generate_values(line)
            request_id = self.env['request.vehicle'].create(values)
            line.request_id = request_id.id
            line.state_request = request_id.state
        self.state = 'in_process'


    def _generate_values(self, line):
        values = {
            'authorized_id' : self.authorized_id.id,
            'drive_id' : line.drive_id.id,
            'date_out' : line.date_out,
            'date_in' : line.date_in,
            'origin' : self.name,
            'address' : line.name,
            'company_id' : self.company_id.id,
            'reservation_line_id' : line.id,
            'state' : 'draft',
        }
        return values

    @api.multi
    def action_cancel(self):
        for line in self.reservation_line_ids:
            request_id = self.env['request.vehicle'].search([('reservation_line_id', '=', line.id)])
            if request_id.state not in ['draft', 'denied']:
                raise UserError(u'Error no se puede cancelar la solicitud %s se encuentra en estado %s' % (request_id.name, request_id.state))
            else:
                request_id.vehicle_id.state_availability = 'available'
                request_id.state = 'cancel'
                line.state_request = request_id.state
        self.state = 'cancel'
    
    @api.multi
    def action_draft(self):
        for line in self.reservation_line_ids:
            request_id = self.env['request.vehicle'].search([('reservation_line_id', '=', line.id)])
            line.write({'request_id':False, 'state_request':False})
            request_id.unlink()
        self.state = 'draft'


class ReservationLine(models.Model):
    _name = 'reservation.line'
    _description = u'Lineas de los conductores que solicitan un vehículo.'
    _order = "id desc"
    
    name = fields.Char(string=u'Ruta', required=True, size=250)
    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Vehículo', readonly=True, ondelete='restrict', index=True, help=u'Asigna un vehículo disponible al conductor.')
    drive_id = fields.Many2one('res.partner', string=u'Conductor', required=True, ondelete='restrict', index=True, help=u'Asigna la persona responsable en elaborar el documento.')
    date_out = fields.Date(string=u'Fecha salida', required=True, help=u'Fecha salida del vehículo.')
    date_in = fields.Date(string=u'Fecha reingreso', required=True, help=u'Fecha ingreso el vehículo.')
    state_request = fields.Selection(selection=list_state_line, string=u'Estado', readonly=True, help=u'Estado en que se encuentra la solicitud.')
    reservation_id = fields.Many2one('reservation', string=u'Reservación', ondelete='cascade', index=True, help=u'Asigna un reservación.')
    request_id = fields.Many2one('request.vehicle', string=u'Solicitud', readonly=True, copy=False)
    company_id = fields.Many2one('res.company', string=u'Compañia', related='reservation_id.company_id', store=True, readonly=True)

