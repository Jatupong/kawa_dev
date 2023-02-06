# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class EmployeeTaxDeductionType(models.Model):
    _name = 'employee.tax.deduction.type'
    _description = 'Employee Tax Deduction Type'
    _rec_name = 'name'

    name = fields.Char('Name')
    amount = fields.Float('Amount')


class HrEmployeeTaxDeduction(models.Model):
    _name = "hr.employee.tax.deduction"
    _description = "Hr Employee Tax Deduction"
    _rec_name = 'tax_deduction_id'

    tax_deduction_id = fields.Many2one('employee.tax.deduction.type', string='Type')
    person = fields.Integer(string='Person', default=1)
    rate_amount = fields.Float(related='tax_deduction_id.amount', string='Max Amount Rate', readonly=True)
    amount = fields.Float(string='Amount')
    hr_contract_id = fields.Many2one('hr.contract')

    @api.onchange('employee_tax_deduction_id', 'person')
    def _onchange_employee_tax_deduction(self):
        for deduct in self:
            deduct.amount = deduct.rate_amount * deduct.person