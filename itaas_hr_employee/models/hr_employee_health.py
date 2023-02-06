# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _

class HrEmployeeHealth(models.Model):
    _name = 'hr.employee.health'
    _description = 'HR Employee Health'

    name = fields.Char("Name of Hospital", required=True)
    detail = fields.Char("Detail")
    date = fields.Date("Date")
    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade')