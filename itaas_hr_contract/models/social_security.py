# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import datetime

class SocialSecurity(models.Model):
    _name = 'social.security'
    _description = "Social Security"
    _rec_name = 'name'

    name = fields.Char('Name')
    social_line_ids = fields.One2many('social.security.line', 'social_id')
    sso_salary_rule_code = fields.Char(string="SSO Salary Code")
    sso_company_salary_rule_code = fields.Char(string="SSO Company Salary Code")
    sso_salary_rule_id = fields.Many2one('hr.salary.rule', string="SSO Salary Rule")
    sso_company_salary_rule_id = fields.Many2one('hr.salary.rule', string="SSO Company Salary Rule")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)


class SocialSecurityLine(models.Model):
    _name = "social.security.line"
    _description = "Social Security Line"
    _rec_name = "social_id"
    _order = "date_from asc"

    social_id = fields.Many2one('social.security', ondelete='cascade', required=True)
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    default_sso_rate = fields.Float(string='Default SSO Rate(%)', digits=(16, 2))
    default_maximum_sso = fields.Float(string='Default Maximum SSO', digits=(16, 2))
    default_sso_company_rate = fields.Float(string='Default SSO Company Rate(%)', digits=(16, 2))
    minimum_rate = fields.Float('Minimum Rate')
    maximum_rate = fields.Float('Maximum Rate')









