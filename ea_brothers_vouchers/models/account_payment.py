# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_in_words = fields.Char(string="Amount in Words", compute='_compute_amount_in_words')
    cheque_transfer_number = fields.Char(string='Cheque # / Transfer', track_visibility='onchange')

    def _compute_amount_in_words(self):
        self.amount_in_words = self.currency_id.amount_to_text(self.amount) if self.currency_id else ''