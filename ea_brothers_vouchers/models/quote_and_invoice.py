# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

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

    def _compute_amount_in_words(self):
        self.amount_in_words = self.currency_id.amount_to_text(self.amount_total) if self.currency_id else ''


#class AccountMove(models.Model):
 #   _inherit = "account.move"

  #  amount_in_words = fields.Char(string="Amount in Words", compute='_compute_amount_in_words')
   # branch = fields.Char(string='Branch', track_visibility='onchange')
    #job = fields.Char(string='Job', track_visibility='onchange')
    #lpo = fields.Char(string='LPO', track_visibility='onchange')
    #ticket = fields.Char(string='Ticket', track_visibility='onchange')
    #customer_ref = fields.Selection([
     #   ('branch', "Branch"),
      #  ('job', "Job"),
       # ('lpo', "LPO"),
        #('ticket', "Ticket")], track_visibility='onchange', string='Customer Reference')

    #def _compute_amount_in_words(self):
     #   self.amount_in_words = self.currency_id.amount_to_text(self.amount_total) if self.currency_id else ''
