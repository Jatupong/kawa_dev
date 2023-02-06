# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import datetime


class HrContract(models.Model):
    _inherit = 'hr.contract'

    hr_tax_deduction_ids = fields.One2many('hr.employee.tax.deduction', 'hr_contract_id')
    total_deduction_amount = fields.Float(string='Total Deduction Amount', compute='get_total_deduction', store=True)
    total_revenue_summary_net = fields.Float(string='รายได้สุทธิสะสม', digits='Payroll', track_visibility='onchange',
                                             help='รายได้ - รายหัก')
    total_revenue_summary_for_tax = fields.Float(string='รายได้สำหรับคิดภาษีบุคคลธรรมดาสะสม', digits='Payroll',
                                                 track_visibility='onchange', help='ภาษี + ภาษีเฉพาะงวด')
    total_revenue_summary_for_tax_special = fields.Float(string='รายได้สำหรับคิดภาษีบุคคลธรรมดาสะสมเฉพาะงวด',
                                                         digits='Payroll',
                                                         track_visibility='onchange', help='ภาษีเฉพาะงวด')
    total_tax_deduction = fields.Float(string='ค่าลดหย่อนสะสม', digits='Payroll')
    total_tax_paid = fields.Float(string='ภาษีบุคคลธรรมดา หัก ณ ที่จ่ายสะสม', digits='Payroll')
    payroll_year_record_ids = fields.One2many('hr.payroll.yearly.record', 'contract_id', string='Payroll Yearly Record')

    @api.depends('hr_tax_deduction_ids.amount')
    def get_total_deduction(self):
        for contract in self:
            contract.total_deduction_amount = sum(line.amount for line in contract.hr_tax_deduction_ids)

    def action_reset_salary_start(self):
        if self.user_has_groups('hr.group_hr_manager'):
            for obj in self:
                lastyear = fields.Date.today().year - 1
                if self.env['hr.payroll.yearly.record'].search([('year', '=', str(lastyear)),
                                                                ('contract_id', '=', obj.id)]):
                    raise UserError(_("รายการได้บันทึกไปแล้วของ %s หากต้องการแก้ไขให้ลบรายการก่อนหรือปรับปรุงรายการโดยตรง") % (obj.name))
                else:
                    yearly_val = {
                        'year': lastyear,
                        'total_revenue_summary_net': obj.total_revenue_summary_net,
                        'total_revenue_summary_for_tax': obj.total_revenue_summary_for_tax,
                        'total_revenue_summary_for_tax_special': obj.total_revenue_summary_for_tax_special,
                        'total_tax_deduction': obj.total_tax_deduction,
                        'total_tax_paid': obj.total_tax_paid,
                        'sso_paid_total': obj.sso_paid_total,
                        'sso_company_paid_total': obj.sso_company_paid_total,
                        'contract_id': obj.id,
                    }
                    record_id = self.env['hr.payroll.yearly.record'].create(yearly_val)
                    if record_id:
                        obj.total_revenue_summary_net = 0.0
                        obj.total_revenue_summary_for_tax = 0.0
                        obj.total_revenue_summary_for_tax_special = 0.0
                        obj.total_tax_deduction = 0.0
                        obj.total_tax_paid = 0.0
                        obj.sso_paid_total = 0.0
                        obj.sso_company_paid_total = 0.0
                    else:
                        raise UserError(_("%s : ไม่สามารถบันทึกได้") % (obj.name))
        else:
            raise UserError(_("You do not have permission to access"))