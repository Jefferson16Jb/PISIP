# -*- encoding: utf-8 -*-

{
    'name' : 'Módulo AMT',
    'version' : '1.0',
    'summary': 'Módulo de entrada y salida de vehiculos.',
    'sequence': 1,
    'description': """
        Módulo con la capacidad de registrar actividad AMT
    """,
    'category': 'Vehiculos',
    'website': 'https://www.amt.com',
    'images' : [],
    'depends' : ['base', 'base_setup', 'fleet', 'module_settings'],
    'data': [
        'views/fleet_vehicle_views.xml',
        'views/fleet_vehicle_cost_views.xml',
        'views/fleet_vehicle_model_views.xml',
        #'views/reservation_views.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
