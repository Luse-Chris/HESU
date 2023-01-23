# -*- coding: utf-8 -*-
# from odoo import http


# class TenmetPaymentVoucher(http.Controller):
#     @http.route('/tenmet_payment_voucher/tenmet_payment_voucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tenmet_payment_voucher/tenmet_payment_voucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tenmet_payment_voucher.listing', {
#             'root': '/tenmet_payment_voucher/tenmet_payment_voucher',
#             'objects': http.request.env['tenmet_payment_voucher.tenmet_payment_voucher'].search([]),
#         })

#     @http.route('/tenmet_payment_voucher/tenmet_payment_voucher/objects/<model("tenmet_payment_voucher.tenmet_payment_voucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tenmet_payment_voucher.object', {
#             'object': obj
#         })
