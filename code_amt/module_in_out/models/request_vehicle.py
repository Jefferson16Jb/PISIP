# -*- encoding: utf-8 -*-

from odoo import models, fields

list_state = [
    ('draft', u'Borrador'),
    ('wait', u'En espera'),
    ('approved', u'Aprobado'),
    ('circulation', u'En circulación'),
    ('re_entry', u'Reingreso'),
    ('denied', u'Negado'),
    ('cancel', u'Cancelado')]

class RequestVehicle(models.Model):
    _name = 'request.vehicle'
    _inherit = ['mail.thread']
    _description = u'Solicitar reservaci�n de veh�culo.'
    _order = "date desc, name desc, id desc"
    
    name = fields.Char(string=u'N° Documento', size=150, readonly=True, default=u'Nueva solicitud', help=u'Nombre de la solicitud debe ser unico')
    date = fields.Date(string=u'Fecha', required=True, default=fields.Date.context_today, help=u'Fecha en que se elabora el documento.')
    authorized_id = fields.Many2one('res.partner', string=u'Autorizado por', required=True, help=u'Asigna a la persona responsable en autoriza el documento.', track_visibility='always')
    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Vehículo', readonly=True, ondelete='restrict', index=True,
                                 states={'draft': [('readonly', False)]}, help=u'Asigna un vehículo disponible al conductor.', track_visibility='always')
    drive_id = fields.Many2one('res.partner', string=u'Conductor', required=True, readonly=True, states={'draft': [('readonly', False)]}, ondelete='restrict', index=True, help=u'Asigna la persona responsable en elaborar el documento.')
    date_out = fields.Date(string=u'Fecha salida', required=True, help=u'Fecha salida del vehículo.')
    date_in = fields.Date(string=u'Fecha reingreso', required=True, help=u'Fecha ingreso el vehículo.')
    origin = fields.Char(string=u'Documento de origen', size=50, help=u'Documento de origen.')
    address = fields.Char(string=u'Ruta', size=250, required=True)
    state = fields.Selection(selection=list_state, string=u'Estado', readonly=True, index=True,
                             track_visibility='onchange', copy=False, help=u'Estado en que se encuentra la solicitud.')
    reservation_line_id = fields.Many2one('reservation.line', string=u'Reservación', ondelete='cascade', index=True, help=u'Asigna un reservación.')
    comment = fields.Text(string=u'Descripción', readonly=True, states={'draft': [('readonly', False)]}, help=u'Escribe un texto relacionado al solicitud.')
    company_id = fields.Many2one('res.company', string=u'Compañia', related='reservation_line_id.company_id', store=True, readonly=True, related_sudo=False)
