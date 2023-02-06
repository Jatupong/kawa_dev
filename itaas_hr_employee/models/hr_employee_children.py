# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class HrEmployeeChildren(models.Model):
    _name = 'hr.employee.children'
    _description = 'HR Employee Children'
    _rec_name = 'name'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade')
    name = fields.Char("Name", required=True)
    date_of_birth = fields.Date("Date of Birth")
    age = fields.Char("Age")
    occupation = fields.Char("Occupation")