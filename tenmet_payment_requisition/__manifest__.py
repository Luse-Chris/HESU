# -*- coding: utf-8 -*-
{
    'name': "TENMET Payment Requisition",

    'summary': """
        Payment Requisition""",

    'description': """
        Payment Requisition, Approvals, Post as Imprest or Normal Payment
    """,

    'author': "SoftNet Technologies Limited",
    'website': "http://www.softnet.co.tz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','account_accountant','hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/payment_requisition.xml',
        'reports/payment_requisition.xml',
       # 'reports/payment_voucher_pdf.xml',
        'views/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
