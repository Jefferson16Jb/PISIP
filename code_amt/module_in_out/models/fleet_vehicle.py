# -*- encoding: utf-8 -*-

from odoo import models, fields

list_state = [
    ('available', u'Disponible'),
    ('service', u'En servicio'),
    ('repair', u'Reparación')]

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    state_availability = fields.Selection(selection=list_state, string=u'Disponibilidad', default='available', help=u'Estado actual del vehículo.')
    