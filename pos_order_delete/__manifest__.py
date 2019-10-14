{
    'name': "Delete POS Orders",
    'version': '12.0.1.0',
    'category': 'Point of Sale',
    'author': 'Sunflower IT',
    'website': 'http://sunflowerweb.nl',
    'sequence': 0,
    'depends': [
        'sale_stock',
        'account',
        'account_cancel',
        'point_of_sale',
        'bus',
        'stock',
    ],
    'data': [
        'views/res_users.xml',
        'wizards/remove_pos_order.xml',
    ],
    'installable': True,
    'application': True,
}
