# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class HrEmployeeEducation(models.Model):
    _name = 'hr.employee.education'
    _description = 'HR Employee Education'
    _rec_name = 'name'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade')
    education_level = fields.Selection([('high_school', 'High School'),
                                        ('vocational', 'Vocational'),
                                        ('diploma', 'Diploma'),
                                        ('bachelor_degree', 'Bachelor Degree'),
                                        ('post_graduate', 'Post-Graduate'),
                                        ('others', 'Others')])
    name = fields.Char("Name of Institution", required=True)
    major = fields.Char("Major")
    date_from = fields.Date("From")
    date_to = fields.Date("To")