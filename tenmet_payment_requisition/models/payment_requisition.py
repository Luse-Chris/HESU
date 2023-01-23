# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class PaymentRequisition(models.Model):
    _name = 'payment.requisition'
    _description = 'Payment Requisition'
    _inherit = 'mail.thread'
    _order = 'name desc'

    
    def _active_budget(self):
        return self.env['crossovered.budget'].search([('state', 'in', ('confirm', 'validate'))], limit=1).id

    name = fields.Char(string='Payment Requisition', copy=False, default=lambda self: ('New'), readonly=True)
    requestor = fields.Many2one('res.partner', string='Payee', required=True)
    date = fields.Date(string='Date', default=datetime.today())
    purpose = fields.Text(string='Purpose', required=True)
    project = fields.Many2one('account.analytic.tag', string='Project')
    budget_id = fields.Many2one('crossovered.budget', string='Budget', default=_active_budget)
    activity = fields.Many2one('account.analytic.account', string='Activity')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    budget_balance = fields.Float(string='Budget Balance', compute='_compute_budget_balance', store=True, readonly=True)
    payment_requisition_lines = fields.One2many('payment.requisition.lines', 'payment_requisition_id',
                                                string='Payment Requisiton Lines')
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user.id)
    requisition_total = fields.Float(compute='_compute_requisition_total', store=True, string='Requisition Total')
    requisition_total_in_words = fields.Char(string='Amount in Words', compute='_amount_in_words')
    authorizer_id = fields.Many2one('res.users', string='To Authorise')
    certifier_id = fields.Many2one('res.users', string='To Certify')
    approver_id = fields.Many2one('res.users', string='To Approve')
    is_authorizer = fields.Boolean(string='Is Authorizer', compute='_is_authorizer', default=False) # - Has not been used anywhere
    is_certifier = fields.Boolean(string='Is Certifier', compute='_is_certifier', default=False) # - Has not been used anywhere
    is_approver = fields.Boolean(string='Is Approver', compute='_is_approver', default=False) # - Has not been used anywhere
    authorized_by = fields.Many2one('hr.employee', string='Authorized By')
    certified_by = fields.Many2one('hr.employee', string='Certified By')
    approved_by = fields.Many2one('hr.employee', string='Approved By')
    date_authorized = fields.Datetime(string='Date Authorized')
    date_certified = fields.Datetime(string='Date Certified')
    date_approved = fields.Datetime(string='Date Approved')
    created_by_id = fields.Many2one('hr.employee', readonly=True, string='Created by',
                                    default=lambda self: self.env['hr.employee'].search(
                                        [('user_id', '=', self.env.uid)], limit=1))
    state = fields.Selection([
        ('draft', "Draft"),
        ('submitted', "Submitted"),
        ('authorized', "Authorized"),
        ('certified', "Certified"),
        ('approved', "Approved"),
        ('posted', "Posted"),
        ('rejected', "Rejected")], default='draft', track_visibility='onchange')
    bank_account_id = fields.Many2one('account.account', string='Bank Account')

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.requisition') or ('New')
            return super(PaymentRequisition, self).create(vals)

    @api.depends('activity')
    def _compute_budget_balance(self):
        for request in self:
            amount = 0.0
            if request.activity:
                budget_line = self.env['crossovered.budget.lines']. \
                    search([
                    ('analytic_account_id', '=', request.activity.id), ('crossovered_budget_id', '=', request.budget_id.id)])
                for line in budget_line:
                    amount += (line.practical_amount - line.planned_amount)
            request.budget_balance = amount

    @api.depends('payment_requisition_lines')
    def _compute_requisition_total(self):
        for items in self:
            total_amount = 0.0
            for line in items.payment_requisition_lines:
                total_amount += line.line_total
            items.requisition_total = total_amount

    def _amount_in_words(self):
        self.requisition_total_in_words = self.currency_id.amount_to_text(self.requisition_total) if self.currency_id else ''

    # Determine if logged-in user is the one to authorize - Has not been used anywhere
    @api.depends('current_user')
    def _is_authorizer(self):
        if self.env.user.id == self.authorizer_id.id:
            self.is_authorizer = True
        else:
            self.is_authorizer = False

    # Determine if logged in user is the one to certify - Has not been used anywhere
    @api.depends('current_user')
    def _is_certifier(self):
        if self.env.user.id == self.certifier_id.id:
            self.is_certifier = True
        else:
            self.is_certifier = False

    # Determine if logged in user is the one to approve - Has not been used anywhere
    @api.depends('current_user')
    def _is_approver(self):
        if self.env.user.id == self.approver_id.id:
            self.is_approver = True
        else:
            self.is_approver = False

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_submitted(self):
        self.write({'state': 'submitted'})
        for applications in self:
           # if self.requisition_total > self.budget_balance:
            #    raise UserError('Budget balance for this Activity has been exceeded! '
             #                     'Please contact FGAM to review the Activity Budget or select a different Activity')
            if not applications.payment_requisition_lines:
                raise UserError('Requisition details are missing. Please fill the details before submitting!')
            if not applications.authorizer_id:
                raise UserError('Include name of Person to authorize the Application')
            if not applications.certifier_id:
                raise UserError('Include name of Person to Certify the Application')
            if not applications.approver_id:
                raise UserError('Include name of Person to Approve the Application')

    def action_authorized(self):
        authorizer = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if self.env.user.id != self.authorizer_id.id:
            raise UserError(_('Only %s can Authorize or Reject this requisition!')%(self.authorizer_id.name))
        self.write({'state': 'authorized', 'authorized_by': authorizer})
        self.date_authorized = fields.Datetime.now()

    def action_certified(self):
        certifier = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if self.env.user.id != self.certifier_id.id:
            raise UserError(_('Only %s can Certify or Reject this requisition!')%(self.certifier_id.name))
        self.write({'state': 'certified', 'certified_by': certifier})
        self.date_certified = fields.Datetime.now()

    def action_approved(self):
        approver = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if self.env.user.id != self.approver_id.id:
            raise UserError(_('Only %s can Approve or Reject this requisition!')%(self.approver_id.name))
        self.write({'state': 'approved', 'approved_by': approver})
        self.date_approved = fields.Datetime.now()

    def action_reject1(self):
        if self.env.user.id != self.authorizer_id.id:
            raise UserError(_('Only %s can Authorize or Reject this requisition!') % (self.authorizer_id.name))
        self.write({'state': 'rejected'})

    def action_reject2(self):
        if self.env.user.id != self.certifier_id.id:
            raise UserError(_('Only %s can Certify or Reject this requisition!') % (self.certifier_id.name))
        self.write({'state': 'rejected'})

    def action_reject3(self):
        if self.env.user.id != self.approver_id.id:
            raise UserError(_('Only %s can Approve or Reject this requisition!') % (self.approver_id.name))
        self.write({'state': 'rejected'})
    
    def action_cancel(self):
        self.write({'state': 'rejected'})

    def reset_to_approved(self):
        self.write({'state': 'approved'})

    def create_bill(self):
        self.write({'state': 'posted'})
        bill_obj = self.env['account.move']
        for record in self:
            # record.state = 'draft'
            partner = record.requestor
            if record.payment_requisition_lines:
                bill_lines = []
                for items in record.payment_requisition_lines:
                    bill_lines.append(
                        (0, 0,
                         {'name': items.name or False,
                          'account_id': items.account_id and items.account_id.id or False,
                          'analytic_account_id': items.activity and items.activity.id or False,
                          'analytic_tag_ids': items.project and items.project.ids or False,
                          'quantity': items.quantity,
                          'price_unit': items.unit_price
                          })
                    )
                vals = {
                    'partner_id': record.requestor,
                    'type': 'in_invoice',
                    'ref': record.name,
                    'invoice_line_ids': bill_lines or False
                }
                bill = bill_obj.create(vals)
                bill_view_id = self.env.ref('account.view_move_form')

                return {
                    'name': ("Bill"),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'view_id': bill_view_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': bill.id,
                    'context': {}
                }

    def action_view_bill(self):
        return {
            'name': 'Bill',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('ref', '=', self.name)]
        }

    # def create_journal(self):
    #     self.write({'state': 'posted'})
    #     journal_object = self.env['account.move']
    #     for record in self:
    #         if record.payment_requisition_lines:
    #             journal_lines = []
    #             for items in record.payment_requisition_lines:
    #                 journal_lines.append(
    #                     (0, 0,
    #                      {'account_id': items.account_id and items.account_id.id or False,
    #                       'analytic_account_id': items.activity and items.activity.id or False,
    #                       'analytic_tag_ids': items.project and items.project.ids or False,
    #                       'partner_id': items.payment_requisition_id.requestor.id or False,
    #                       'debit': items.payment_requisition_id.requisition_total,
    #                       'credit': items.payment_requisition_id.requisition_total,
    #                       'name': items.payment_requisition_id.purpose
    #                      })
    #                 )
    #             vals = {
    #                 'ref': record.name,
    #                 'line_ids': journal_lines or False
    #             }
    #             journal = journal_object.create(vals)
    #             journal_view_id = self.env.ref('account.view_move_form')
    #
    #             return {
    #                 'name': 'Journal',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'res_model': 'account.move',
    #                 'view_id': journal_view_id.id,
    #                 'type': 'ir.actions.act_window',
    #                 'nodestroy': True,
    #                 'target': 'current',
    #                 'res_id': journal.id,
    #                 'context': {}
    #             }

   # def create_journal(self):
    #    self.write({'state': 'posted'})
     #   journal_object = self.env['account.move']
      #  for record in self:
       #     if record.payment_requisition_lines:
#
 #               debit_vals = {
  #                  'name': self.payment_requisition_lines.name,
   #                 'account_id': self.payment_requisition_lines.account_id.id or False,
    #                'partner_id': self.requestor.id or False,
     #               'analytic_account_id': self.activity and self.activity.id or False,
      #              'analytic_tag_ids': self.project and self.project.ids or False,
       #             'debit': self.requisition_total,
        #            'credit': 0.0,
         #       }
#
 #               credit_vals = {
  #                  'name': self.payment_requisition_lines.name,
   #                 'account_id': self.bank_account_id.id or False,
    #                'debit': 0.0,
     #               'credit': self.requisition_total,
      #          }
#
 #               vals = {
  #                  'ref': record.name,
   #                 'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
    #            }
     #           journal = journal_object.create(vals)
      #          journal_view_id = self.env.ref('account.view_move_form')
#
 #               return {
  #                  'name': 'Journal',
   #                 'view_type': 'form',
    #                'view_mode': 'form',
     #               'res_model': 'account.move',
      #              'view_id': journal_view_id.id,
       #             'type': 'ir.actions.act_window',
        #            'nodestroy': True,
         #           'target': 'current',
          #          'res_id': journal.id,
           #         'context': {}
            #    }


    def create_journal(self):
        self.write({'state': 'posted'})
        journal_object = self.env['account.move']
        for record in self:
            if record.payment_requisition_lines:
                name = ''
                account_id = False
                if len(record.payment_requisition_lines.ids) > 1:
                    name = record.payment_requisition_lines[0].name
                    account_id = record.payment_requisition_lines[0].account_id
                else:
                    name = record.payment_requisition_lines.name
                    account_id = record.payment_requisition_lines[0].account_id
                debit_vals = {
                    'name': name or '',
                    'account_id': account_id.id or False,
                    'partner_id': record.requestor.id or False,
                    'analytic_account_id': record.activity and record.activity.id or False,
                    'analytic_tag_ids': record.project and record.project.ids or False,
                    'debit': record.requisition_total,
                    'credit': 0.0,
                }

                credit_vals = {
                    'name': name or '',
                    'account_id': self.bank_account_id.id or False,
                    'debit': 0.0,
                    'credit': self.requisition_total,
                }

                vals = {
                    'ref': record.name,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                journal = journal_object.create(vals)
                journal_view_id = self.env.ref('account.view_move_form')

                return {
                    'name': 'Journal',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'view_id': journal_view_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': journal.id,
                    'context': {}
                }
