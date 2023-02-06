# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import models, fields


class HrEmployeeBehavior(models.Model):
    _name = 'hr.employee.behavior'
    _description = 'HR Employee Behavior'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade', required=True)
    date = fields.Date("Date", required=True)
    type_id = fields.Many2one('hr.behavior.type', string='Type', required=True)
    description = fields.Text(string='Detail')


class HrBehaviorType(models.Model):
    _name = 'hr.behavior.type'

    name = fields.Char("Type", required=True)
    description = fields.Text(string='Description')