# -*- coding: utf-8 -*-
# from odoo import http


# class TenmetPaymentRequisition(http.Controller):
#     @http.route('/tenmet_payment_requisition/tenmet_payment_requisition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tenmet_payment_requisition/tenmet_payment_requisition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tenmet_payment_requisition.listing', {
#             'root': '/tenmet_payment_requisition/tenmet_payment_requisition',
#             'objects': http.request.env['tenmet_payment_requisition.tenmet_payment_requisition'].search([]),
#         })

#     @http.route('/tenmet_payment_requisition/tenmet_payment_requisition/objects/<model("tenmet_payment_requisition.tenmet_payment_requisition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tenmet_payment_requisition.object', {
#             'object': obj
#         })
