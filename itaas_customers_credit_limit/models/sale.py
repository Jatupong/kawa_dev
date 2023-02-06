# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit_state = fields.Selection([('none', 'Credit Limit Not Set'),
                                     ('under', 'Under Credit Limit'),
                                     ('over', 'Over Credit Limit'),
                                     ('allow_over', 'Allow Over Credit Limit')], string='Credit Status',
                                    compute='_compute_partner_credit_warning', store=True)
    is_allow_credit = fields.Boolean('')

    @api.depends('company_id', 'partner_id', 'amount_total', 'is_allow_credit')
    def _compute_partner_credit_warning(self):
        res = super(SaleOrder, self)._compute_partner_credit_warning()
        for order in self:
            if order.partner_credit_warning and order.is_allow_credit:
                order.credit_state = 'allow_over'
            elif not order.partner_credit_warning and order.is_allow_credit:
                order.credit_state = 'allow_over'
            elif order.partner_credit_warning:
                order.credit_state = 'over'
            elif not order.partner_credit_warning and order.partner_id.commercial_partner_id.use_partner_credit_limit:
                order.credit_state = 'under'
            else:
                order.credit_state = 'none'

        return res

    def action_unlock_limit(self):
        # print('action_unlock_limit')
        self.is_allow_credit = True
        message = _("Unlock limit")
        return self.message_post(body=message)

    def action_draft(self):
        res = super(SaleOrder, self).action_draft()
        self.is_allow_credit = False

        return res

    def action_confirm(self):
        # print('action_confirm ')
        if self.credit_state == 'over' and not self.is_allow_credit:
            action = self.env['ir.actions.actions']._for_xml_id('itaas_customers_credit_limit.action_wizard_warning_override_credit')
            action['context'] = {'default_partner_credit_warning': self.partner_credit_warning}
            return action

        return super(SaleOrder, self).action_confirm()

    def _get_mail_group_confirm_anyway(self):
        # print('_get_mail_group_confirm_anyway')
        partner_ids = self.env['res.groups'].search([('name', '=', 'Confirm Anyway')]).users.mapped('partner_id').ids
        text_partner = ''
        if partner_ids:
            # print('partner_ids ', partner_ids)
            text_partner = ', '.join(str(x) for x in partner_ids)
            # print('text_partner', text_partner)

        return text_partner