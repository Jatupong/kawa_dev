# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class HrEmployeeExperience(models.Model):
    _name = 'hr.employee.experience'
    _description = 'HR Employee Experience'
    _rec_name = 'name'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade')
    name = fields.Char("Name of Employer", required=True)
    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    position = fields.Char("Position")
    responsibility = fields.Char("Responsibility")
    salary = fields.Float("Last Salary")
    reason = fields.Char("Reason for leaving")