# -*- coding: utf-8 -*-
{
    'name': "TENMET Payment Voucher",

    'summary': """
        Print Payment Voucher with Unique sequence independent from Payment Requisition""",

    'description': """
        Print Payment Voucher with Unique sequence independent from Payment Requisition
    """,

    'author': "SoftNet Technologies Limited",
    'website': "http://www.softnet.co.tz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','tenmet_payment_requisition','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payment_voucher.xml',
        'reports/payment_voucher_pdf.xml',
        'views/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
