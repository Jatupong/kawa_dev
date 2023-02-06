# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _
from datetime import datetime,timedelta,date
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import datetime
from dateutil.relativedelta import relativedelta


class HrPayrollYearlyRecord(models.Model):
    _name = "hr.payroll.yearly.record"
    _description = "Hr Payroll Yearly Record"
    _rec_name = "year"

    contract_id = fields.Many2one('hr.contract', string='Contract')
    year = fields.Char(string='Year')
    employee_id = fields.Many2one('hr.employee', related='contract_id.employee_id', string='Employee')
    total_revenue_summary_net = fields.Float(string='รายได้สุทธิสะสม', digits='Payroll')
    total_revenue_summary_for_tax = fields.Float(string='รายได้สำหรับคิดภาษีบุคคลธรรมดาสะสม', digits='Payroll')
    total_revenue_summary_for_tax_special = fields.Float(string='รายได้สำหรับคิดภาษีบุคคลธรรมดาสะสมเฉพาะงวด', digits='Payroll')
    total_tax_deduction = fields.Float(string='ค่าลดหย่อนสะสม', digits='Payroll')
    total_tax_paid = fields.Float(string='ภาษีบุคคลธรรมดา หัก ณ ที่จ่ายสะสม', digits='Payroll')
    sso_paid_total = fields.Float(string='ประกันสังคมจ่ายสะสม', digits='Payroll')
    sso_company_paid_total = fields.Float(string='ประกันสังคมนายจ้างจ่ายสะสม', digits='Payroll')