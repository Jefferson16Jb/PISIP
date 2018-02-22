# -*- encoding: utf-8 -*-

{
    'name' : 'Módulo Seguridad y Configuración',
    'version' : '1.0',
    'author': u'Carrillo-Simbaña-Quispe-Tipan',
    'summary': 'Módulo de seguridad y configuración',
    'sequence': 1,
    'description': """
        Módulo administra la seguridad
    """,
    'category': 'Vehiculos',
    'website': 'https://www.amt.com',
    'images' : [],
    'depends' : ['base', 'mail', 'contacts'],
    'data': [
        'data/res_groups.xml',
        'views/res_partner_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
