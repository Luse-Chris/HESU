# -*- coding: utf-8 -*-
# from odoo import http


# class EaBrothersVouchers(http.Controller):
#     @http.route('/ea_brothers_vouchers/ea_brothers_vouchers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ea_brothers_vouchers/ea_brothers_vouchers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ea_brothers_vouchers.listing', {
#             'root': '/ea_brothers_vouchers/ea_brothers_vouchers',
#             'objects': http.request.env['ea_brothers_vouchers.ea_brothers_vouchers'].search([]),
#         })

#     @http.route('/ea_brothers_vouchers/ea_brothers_vouchers/objects/<model("ea_brothers_vouchers.ea_brothers_vouchers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ea_brothers_vouchers.object', {
#             'object': obj
#         })
