# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

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
    _description = u'Solicitar reservación de vehículo.'
    _order = "date desc, name desc, id desc"
    
    name = fields.Char(string=u'N° Documento', size=150, readonly=True, default=u'Nueva solicitud', 
                       help=u'Nombre de la solicitud debe ser unico', copy=False)
    date = fields.Date(string=u'Fecha emisión', required=True, default=fields.Date.context_today, 
                       readonly=True, states={'draft': [('readonly', False)]}, help=u'Fecha en que se elabora el documento.')
    authorized_id = fields.Many2one('res.partner', string=u'Autorizado por', required=True, domain=[('type_partner', '=', 'boss')],
                                    help=u'Asigna a la persona responsable en autoriza el documento.', track_visibility='always', copy=False)
    elaborared_id = fields.Many2one('res.partner', string=u'Elaborado por', required=True, domain=[('type_partner', '=', 'employee')], 
                                    help=u'Asigna la persona responsable en elaborar el documento.', track_visibility='always')
    vehicle_id = fields.Many2one('fleet.vehicle', string=u'Vehículo', required=True, domain=[('state_availability', '=', 'available')], 
                                 help=u'Asigna un vehículo disponible al conductor.', track_visibility='always', copy=False)
    drive_id = fields.Many2one('res.partner', string=u'Solicitante', required=True,  ondelete='restrict', index=True, domain=[('type_partner', '=', 'driver'), ('service_vehicle', '=', False)], 
                               readonly=True, states={'draft': [('readonly', False)]}, help=u'Asigna la persona responsable en elaborar el documento.', copy=False)
    date_out = fields.Date(string=u'Fecha salida', required=True, readonly=True, states={'draft': [('readonly', False)]}, help=u'Fecha salida del vehículo.')
    date_in = fields.Date(string=u'Fecha ingreso', required=True, readonly=True, states={'draft': [('readonly', False)]}, help=u'Fecha ingreso el vehículo.')
    address = fields.Text(string=u'Ruta', size=250, required=True, readonly=True, states={'draft': [('readonly', False)]},)
    state = fields.Selection(selection=list_state, string=u'Estado', readonly=True, index=True, default='draft',
                             track_visibility='onchange', copy=False, help=u'Estado en que se encuentra la solicitud.')
    comment = fields.Text(string=u'Descripción', readonly=True, states={'draft': [('readonly', False)]}, help=u'Escribe un texto relacionado al solicitud.')
    company_id = fields.Many2one('res.company', string=u'Compañia', readonly=True, default=lambda self: self.env.user.company_id)


    @api.onchange('date', 'date_out', 'date_in')
    def _onchange_date_range(self):
        if self.date_out and self.date_in:
            if self.date_out > self.date_in or self.date_in < self.date_out:
                raise UserError(u'Error en la fecha de salida o ingreso, se encuentra mal ingresado.')

    
    @api.multi
    def action_process(self):
        self._onchange_date_range()
        vals = {
            'name' : self.env['ir.sequence'].with_context(ir_sequence_date=self.date).next_by_code('sequence.request.vehicle'),
            'state' : 'wait',
        }
        self.vehicle_id.state_availability = 'in_process'
        self.write(vals)
    
    
    @api.multi
    def action_denied(self):
        self.state = 'denied'
        self.vehicle_id.state_availability = 'available'
        self.drive_id.service_vehicle = False
    
    
    @api.multi
    def action_cancel(self):
        self.state = 'cancel'
        self.vehicle_id.state_availability = 'available'
        self.drive_id.service_vehicle = False
        
    
    @api.multi
    def action_aproved(self):
        self.state = 'approved'
        self.vehicle_id.state_availability = 'service'
        self.drive_id.service_vehicle = True
    
    
    @api.multi
    def action_service(self):
        self.state = 'circulation'
    
    
    @api.multi
    def action_re_entry(self):
        self.state = 're_entry'
        self.vehicle_id.state_availability = 'available'
        self.drive_id.service_vehicle = False
    

    @api.multi
    def action_sent_mail(self):
        self.ensure_one()
        template = self.env.ref('module_in_out.email_template_request_vehicle', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='request.vehicle',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            force_email=True
        )
        return {
            'name': u'Envio de correo electrónico',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
