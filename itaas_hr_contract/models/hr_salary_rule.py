# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class HrSalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    cal_sso = fields.Boolean(string='Calculate SSO')
    cal_tax = fields.Boolean(string='Calculate Tax')
    cal_tax_special = fields.Boolean(string='Calculate Tax Special')


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    cal_sso = fields.Boolean(string='Calculate SSO', related='salary_rule_id.cal_sso', store=True)
    cal_tax = fields.Boolean(string='Cal Tax', related='salary_rule_id.cal_tax', store=True)
    cal_tax_special = fields.Boolean(string='Cal Tax Special', related='salary_rule_id.cal_tax_special', store=True)