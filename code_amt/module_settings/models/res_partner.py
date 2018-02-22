# -*- encoding: utf-8 -*-

from odoo import models, fields

list_type = [
    ('driver', u'Conductor'),
    ('employee', u'Empleado'),
    ('boss', u'Jefe encargado')]

class Partner(models.Model):
    _inherit = 'res.partner'
    
    type_partner = fields.Selection(selection=list_type, string=u'Tipo cargo', default='driver', help=u'Cargo del persona.')
    service_vehicle = fields.Boolean(string='En servicio', default=False, help=u'Conductor se encuentra usando vehiculo.')
    
    