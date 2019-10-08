# -*- coding: utf-8 -*-
{
    'name': "Pos Product extend.",

    'summary': """
     Pos Product extend.
       """,

    'description': """
         Product extend.
    """,
    'sequence': 20,

    'author': "hs",
    'category': 'Sales',
    'version': '0.1',

    'depends': ['product','point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_extend.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,

}