
from odoo import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        res = super(MailMessage, self).create(vals)
        if res.model == 'payment.requisition':
            channel = self.env.ref(
                'tenmet_payment_requisition.channel_mail_extended')
            res.channel_ids = [(6, 0, [channel.id])]
        return res
