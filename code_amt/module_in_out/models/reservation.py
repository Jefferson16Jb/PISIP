# -*- encoding: utf-8 -*-

from odoo import models, fields
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
    ('denied', u'Negado')]

class reservation(models.Model):
    _name = 'reservation'
    _inherit = ['mail.thread']
    _description = u'Tramite para la reservación de vehículos'
    _order = "date desc, name desc, id desc"


    name = fields.Char(string=u'Código', size=150, default='Nuevo', readonly=True, help=u'Código o nombre del documento unico que identifición.')
    authorized_id = fields.Many2one('res.partner', string=u'Autorizado por', required=True, help=u'Asigna a la persona responsable que autoriza el documento.')
    elaborared_id = fields.Many2one('res.partner', string=u'Elaborado por', required=True, help=u'Asigna la persona responsable en elaborar el documento.', track_visibility='always')
    applicant_id = fields.Many2one('res.partner', string=u'Solicitante', required=True, 
                               help=u'Asigna a la persona que estara a cargo de los vehiculos.', track_visibility='always')
    date = fields.Date(string=u'Fecha', required=True, default=fields.Date.context_today, help=u'Fecha en que se elabora el documento.')
    comment = fields.Text(string=u'Descripción', readonly=True, states={'draft': [('readonly', False)]}, help=u'Escribe un texto relacionado al documento.')
    state = fields.Selection(selection=list_state, string=u'Estado', default='draft', index=True, readonly=True, 
                             track_visibility='onchange', copy=False, help=u'Etapas del documento.')
    company_id = fields.Many2one('res.company', string=u'Compañia', readonly=True, states={'draft': [('readonly', False)]}, 
                                 default=lambda self: self.env.user.company_id)
    reservation_line_ids = fields.One2many('reservation.line', 'reservation_id', string=u'Lineas reservación', readonly=True, states={'draft': [('readonly', False)]}, copy=True)


class reservation_line(models.Model):
    _name = 'reservation.line'
    _description = u'Lineas de los conductores que solicitan un vehículo.'
    _order = "id desc"
    
    name = fields.Char(string=u'Ruta', size=150)
    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Vehículo', readonly=True, ondelete='restrict', index=True, help=u'Asigna un vehículo disponible al conductor.')
    drive_id = fields.Many2one('res.partner', string=u'Conductor', required=True, ondelete='restrict', index=True, help=u'Asigna la persona responsable en elaborar el documento.')
    date_out = fields.Date(string=u'Fecha salida', required=True, help=u'Fecha salida del vehículo.')
    date_in = fields.Date(string=u'Fecha reingreso', required=True, help=u'Fecha reingresa el vehículo.')
    state_request = fields.Selection(selection=list_state_line, string=u'Estado', readonly=True, help=u'Estado en que se encuentra la solicitud.')
    reservation_id = fields.Many2one('reservation', string=u'Reservación', ondelete='cascade', index=True, help=u'Asigna un reservación.')
    company_id = fields.Many2one('res.company', string=u'Compañia', related='reservation_id.company_id', store=True, readonly=True, related_sudo=False)

