# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError


class PaymentRequisitionLines(models.Model):
    _name = 'payment.requisition.lines'
    _description = 'Payment Requisition Lines'

    name = fields.Char('Item Description')
    payment_requisition_id = fields.Many2one('payment.requisition')
    account_id = fields.Many2one('account.account', string='Account')
    product_uom_id = fields.Many2one('uom.uom', string='Unit')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    line_total = fields.Float(string='Line Total')
    project = fields.Many2one(related='payment_requisition_id.project', string='Project')
    activity = fields.Many2one(related='payment_requisition_id.activity', string='Activity')

    @api.onchange('quantity', 'unit_price')
    def _onchange_unit_price(self):
        for rec in self:
            rec.line_total = rec.quantity * rec.unit_price