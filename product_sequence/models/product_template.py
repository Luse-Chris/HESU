# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    default_code = fields.Char(compute="_compute_internal_ref")
    
    @api.depends("categ_id")
    def _compute_internal_ref(self):
        for record in self:
            if record.categ_id and record.categ_id.short_name:
               sequence = self.env["ir.sequence"].next_by_code("product_category")
               record.default_code = f"{record.categ_id.parent_id.name}/{record.categ_id.short_name}/{sequence}"

    @api.model
    def create(self, vals):
        # Generate Internal Reference
        barcode = self.env["ir.sequence"].next_by_code("barcode.product.template")
        if not vals.get("barcode"):
           # Generate barcode number
           vals.update({"barcode":barcode})
        res = super(ProductTemplate, self).create(vals)
        return res

