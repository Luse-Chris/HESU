# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentVoucher(models.Model):
    _name = 'payment.voucher'
    _description = 'Print Payment Voucher'
    _order = 'name desc'
    _inherit = 'mail.thread', 'mail.activity.mixin'

    name = fields.Char(string='Payment Requisition', copy=False, default=lambda self: ('New'), readonly=True)
    pr_id = fields.Many2one('payment.requisition', string='For Payment Requisition', track_visibility='onchange')
    print_date = fields.Date(string='Date')

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.voucher') or ('New')
            return super(PaymentVoucher, self).create(vals)

    _sql_constraints = [
        ('unique_payment_req_id', 'unique (pr_id)', 'A Payment Voucher for this Payment Requisition already exists !')
    ]
