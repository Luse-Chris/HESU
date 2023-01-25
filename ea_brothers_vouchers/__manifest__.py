# -*- coding: utf-8 -*-
{
    'name': "ea_brothers_vouchers",

    'summary': """
        Customizations specific to EA Brothers""",

    'description': """
        Vouchers (Non-Invoice Receipts, Cash Payments, Journal Entries)
        Invoice Receipt
        Bill Payment Voucher
        Internal Bank Transfers
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','mail','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/account_move_form_views.xml',
        'views/account_payment_view.xml',
        'reports/journal_voucher_report_template.xml',
	        'views/quote_and_invoice_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
