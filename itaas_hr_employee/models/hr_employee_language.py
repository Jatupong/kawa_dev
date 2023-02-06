# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _


class HrEmployeeLanguage(models.Model):
    _name = 'hr.employee.language'
    _description = 'HR Employee Language Ability'
    _rec_name = 'language'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade')
    language = fields.Selection([('thai', 'Thai'),
                                 ('english', 'English'),
                                 ('other', 'Other')
                                 ], required=True)
    name = fields.Char("Description")
    speaking = fields.Selection([('good', 'Good'),
                                 ('fair', 'Fair'),
                                 ('poor', 'Poor')
                                 ], string='Speaking')
    writing = fields.Selection([('good', 'Good'),
                                ('fair', 'Fair'),
                                ('poor', 'Poor')
                                ], string='Writing')
    reading = fields.Selection([('good', 'Good'),
                                ('fair', 'Fair'),
                                ('poor', 'Poor')
                                ], string='Reading')