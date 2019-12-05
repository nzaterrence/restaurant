{
    'name': "Inclusive Sales Reports",
    'version': '12.0.1.0',
    'category': 'Point of Sale',
    'author': 'Sunflower IT',
    'website': 'http://sunflowerweb.nl',
    'sequence': 0,
    'depends': [
        'point_of_sale',
        'hotel_reservation',
        'hotel_advance_payment'
    ],
    'data': [
        'reports/pos_report.xml',
        'reports/report_saledetails.xml',
        'views/pos_reports.xml',
        'wizards/pos_details.xml'
        # 'views/res_users.xml',
        # 'wizards/remove_pos_order.xml',
    ],
    'installable': True,
    'application': True,
}
