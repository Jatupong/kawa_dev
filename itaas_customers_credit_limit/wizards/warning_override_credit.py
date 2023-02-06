# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)


from odoo import api, models, fields, _

class WizardWarningOverrideCredit(models.TransientModel):
    _name = 'wizard.warning.override.credit'
    _description = 'Warning Override Credit'

    partner_credit_warning = fields.Text(readonly=True)

    def action_request(self):
        ir_model_data = self.env['ir.model.data']
        template_id = self.env['ir.model.data']._xmlid_to_res_id(
            'itaas_customers_credit_limit.mail_template_request_credit_limit', raise_if_not_found=False
        )
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'sale.order',
            'default_res_id': self.env.context.get('active_id'),
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_confirm_anyway(self):
        order_id = self.env['sale.order'].browse(self.env.context.get('active_id'))
        order_id.is_allow_credit = True
        order_id.action_confirm()