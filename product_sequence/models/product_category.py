# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = "product.category"
    short_name = fields.Char("Category Short Name")
    company_id = fields.Many2one(
        string="Company", comodel_name="res.company"
    )
    #company_id = fields.Many2one(comodel_name='res.company')
