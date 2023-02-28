# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    voucher_options = fields.Selection([
        ('journal_voucher', "Journal Voucher"),
        ('cash_payment_voucher', "Cash Payment Voucher"),
        ('payment_voucher', "Payment Voucher"),
        ('receipt_voucher', "Receipt Voucher")], track_visibility='onchange', string='Voucher Option')
    bank_account_id = fields.Many2one('res.partner.bank', string='Bank Account No.', track_visibility='onchange')
    cheque_transfer_number = fields.Char(string='Cheque # / Transfer', track_visibility='onchange')
    #amount_in_words = fields.Char(string="Amount in Words", compute='_compute_amount_in_words')

    amount_in_words = fields.Char(string="Amount in Words", compute='_compute_amount_in_words')
    branch = fields.Char(string='Branch', track_visibility='onchange')
    job = fields.Char(string='Job', track_visibility='onchange')
    lpo = fields.Char(string='LPO', track_visibility='onchange')
    ticket = fields.Char(string='Ticket', track_visibility='onchange')
    customer_ref = fields.Selection([
        ('branch', "Branch"),
        ('job', "Job"),
        ('lpo', "LPO"),
        ('ticket', "Ticket")], track_visibility='onchange', string='Customer Reference')


   # def _compute_amount_in_words(self):
    #    self.amount_in_words = self.currency_id.amount_to_text(self.amount_total_signed) if self.currency_id else ''

    
    def _compute_amount_in_words(self):
        self.amount_in_words = self.currency_id.amount_to_text(self.amount_total) if self.currency_id else ''
    def total_debit_credit(self):
        res = {}
        for move in self:
            dr_total = 0.0
            cr_total = 0.0
            for line in move.line_ids:
                dr_total += line.debit
                cr_total += line.credit
            res.update({'cr_total': cr_total, 'dr_total': dr_total})
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    budget_balance = fields.Float(string='Budget Balance', compute='_compute_budget_balance', store=True, readonly=True)

    @api.depends('analytic_distribution')
    def _compute_budget_balance(self):
        for request in self:
            amount = 0.0
            if request.analytic_distribution:
                budget_line = self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', request.analytic_distribution)])
                for line in budget_line:
                    amount += (line.practical_amount - line.planned_amount)
            request.budget_balance = amount


