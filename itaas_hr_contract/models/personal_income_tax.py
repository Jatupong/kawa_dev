# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import datetime


class PersonalIncomeTax(models.Model):
    _name = 'personal.income.tax'
    _description = 'Personal Income Tax'
    _rec_name = 'year'

    def current_year(self):
        return datetime.date.today().year

    year = fields.Char(_('Year'), default=current_year)
    # deduct_general_expense_percent = fields.Float(string='General Expense Deduction %')
    # deduct_general_expense_max = fields.Float(string='General Expense Dedcution Max Amount')
    # deduction_after_expense_amount = fields.Float(string='Deduction After Deduct General Expense')
    personal_tax_line_ids = fields.One2many('personal.income.tax.line', 'personal_tax_id')
    tax_salary_rule_code = fields.Char(string="Tax Salary Rule Code")
    tax_salary_rule_id = fields.Many2one('hr.salary.rule', string="Tax Salary Rule")


class PersonalIncomeTaxLine(models.Model):
    _name = 'personal.income.tax.line'
    _description = 'Personal Income Tax Line'
    _rec_name = 'personal_tax_id'

    personal_tax_id = fields.Many2one('personal.income.tax')
    rate_no = fields.Integer('Rate No.')
    minimum_rate = fields.Integer('Minimum Rate')
    maximum_rate = fields.Integer('Maximum Rate')
    tax_rate = fields.Float('Rate %')











