# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _
from datetime import datetime,timedelta,date
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import datetime
from dateutil.relativedelta import relativedelta


INTERVALS = {
    'annually': (relativedelta(months=12), 1),
    'semi-annually': (relativedelta(months=6), 2),
    'quarterly': (relativedelta(months=3), 4),
    'bi-monthly': (relativedelta(months=2), 6),
    'semi-monthly': (relativedelta(weeks=2), 24),
    'monthly': (relativedelta(months=1), 12),
    'bi-weekly': (relativedelta(weeks=2), 26),
    'weekly': (relativedelta(weeks=1), 52),
    'daily': (relativedelta(days=1), 365),
}


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    sso_amount_total = fields.Float(string='Amount SSO Total', digits='Payroll')
    sso_deduct = fields.Float(string='SSO Deduct Amount', digits='Payroll')
    sso_company_deduct = fields.Float(string='SSO Deduct Company Amount', digits='Payroll')
    pvd_amount = fields.Float(string='PVD Amount', digits='Payroll')
    tax_amount_total = fields.Float(string='Amount Tax Total', digits='Payroll')
    tax_special_amount_total = fields.Float(string='Amount Tax Special Total', digits='Payroll')
    tax_deduct = fields.Float(string='Tax Amount', digits='Payroll')
    tax_deduction = fields.Float(string='Tax Deduction Amount', digits='Payroll')
    calculate_tax = fields.Text('Calculate Tax')

    def compute_sheet(self):
        print('compute_sheet: sso', )
        for payslip in self:
            payslip.get_pvd_info()
            payslip.get_tax_amount()

        res = super(HrPayslip, self).compute_sheet()
        for payslip in self:
            payslip.get_sso_amount()
            payslip.get_sso_info()
            payslip.get_tax_info()

        return res

    def get_pvd_info(self):
        input_line = []
        if self.contract_id.pvd_start_date:
            pvd_start_date = self.contract_id.pvd_start_date
        else:
            pvd_start_date = self.date_from
        if self.contract_id.pvd_end_date:
            pvd_end_date = self.contract_id.pvd_end_date
        else:
            pvd_end_date = self.date_to

        pvd_input_type_id = self.contract_id.pvd_input_type_id
        amount = 0.0
        if pvd_input_type_id and self.date_from >= pvd_start_date and self.date_to <= pvd_end_date:
            # print('get_pvd_info: ',pvd_input_type_id)
            paid_amount = self._get_contract_wage()
            amount = paid_amount * (self.contract_id.pvd_rate / 100)
            input_line_id = self.input_line_ids.filtered(lambda r: r.input_type_id == pvd_input_type_id)
            # print('input_line_id: ',input_line_id)
            if input_line_id:
                input_line_id.update({'amount': amount})
            else:
                input_line.append((0, 0, {
                    'input_type_id': pvd_input_type_id.id,
                    'amount': amount,
                }))

            self.update({'input_line_ids': input_line,
                         'pvd_amount': amount,
                         })

    def _get_sso_amount_total(self):
        sso_amount_total = 0.0
        if self.line_ids:
            sso_amount_total = sum(self.line_ids.filtered(lambda x: x.salary_rule_id.cal_sso).mapped('total'))

        return sso_amount_total

    def get_sso_amount(self):
        if not self.contract_id.exclude_sso:
            sso_amount_total = self._get_sso_amount_total()
            # print('get_sso_info: ', sso_amount_total)
            sso_id = self.env['social.security.line'].search([('date_from', '<=', self.date_payment),
                                                              ('date_to', '>=', self.date_payment)], limit=1)
            # print("Year Social Security : " + str(self.date_payment.year) + " Found : " + str(len(sso_id)))

            if not sso_id:
                raise UserError(_('SSO rate does not setup'))

            minimum_rate = sso_id.minimum_rate
            maximum_rate = sso_id.maximum_rate
            sso_rate = sso_id.default_sso_rate * 0.01
            sso_company_rate = sso_id.default_sso_company_rate * 0.01
            maximum_sso = sso_id.default_maximum_sso
            current_sso_amount_total = sso_amount_total

            group_period = self._get_period_multiple_payment_sso(sso_id)
            remain_payslip = len(group_period['group_period']) - len(group_period['group_payslip'])
            sso_amount_total = group_period['group_period_sso_amount'] + (current_sso_amount_total * remain_payslip)
            sso_deduct_total = group_period['group_period_deduct_sso']
            sso_company_deduct_total = group_period['group_period_deduct_sso_company']

            # print('group_period: ', group_period)
            # print('remain_payslip: ', remain_payslip)
            # print('sso_amount_total: ', sso_amount_total)
            # print('sso_deduct_total: ', sso_deduct_total)
            # print('sso_company_deduct_total: ', sso_company_deduct_total)

            if sso_amount_total <= minimum_rate:
                sso_wage = minimum_rate
            elif sso_amount_total >= maximum_rate:
                sso_wage = maximum_rate
            else:
                sso_wage = sso_amount_total

            # print('sso_wage : ', sso_wage)
            result = sso_wage * sso_rate
            result_company = sso_wage * sso_company_rate

            if len(group_period['group_period']) == len(group_period['group_payslip']) + 1:
                # print('- sso_deduct_total : ', sso_deduct_total)
                result = result - sso_deduct_total
                result_company = result_company - sso_company_deduct_total
            else:
                # print('/ len group_period')
                result = result / len(group_period['group_period'])
                result_company = result_company / len(group_period['group_period'])

            # print('result : ', result)
            # print('result_company : ', result_company)

            if result > maximum_sso:
                result_sso = maximum_sso
            else:
                result_sso = result

            if result_company > maximum_sso:
                result_sso_company = maximum_sso
            else:
                result_sso_company = result_company

            result_sso = abs(round(result_sso, 0))
            result_sso_company = abs(round(result_sso_company, 0))
        else:
            sso_amount_total = 0.0
            result_sso = 0.0
            result_sso_company = 0.0

        self.update({'sso_amount_total': sso_amount_total,
                     'sso_deduct': result_sso,
                     'sso_company_deduct': result_sso_company
                     })

    def get_sso_info(self):
        sso_id = self.env['social.security.line'].search([('date_from', '<=', self.date_payment),
                                                          ('date_to', '>=', self.date_payment)], limit=1)
        line_ids = []
        if sso_id:
            sso_salary_rule_id = self.env['hr.salary.rule'].search([('code', '=', sso_id.social_id.sso_salary_rule_code),
                                                                    ('struct_id', '=', self.struct_id.id)], limit=1)
            if sso_salary_rule_id:
                line_id = self.line_ids.filtered(lambda s: s.salary_rule_id == sso_salary_rule_id)
                print('sso input_line_id: ', line_id)
                if line_id:
                    line_id.update({'amount': self.sso_deduct})
                else:
                    line_ids.append((0, 0, {
                        'salary_rule_id': sso_salary_rule_id.id,
                        'code': sso_salary_rule_id.code,
                        'name': sso_salary_rule_id.name,
                        'amount': self.sso_deduct,
                    }))

            sso_company_salary_rule_id = self.env['hr.salary.rule'].search([('code', '=', sso_id.social_id.sso_company_salary_rule_code),
                                                                            ('struct_id', '=', self.struct_id.id)], limit=1)
            if sso_company_salary_rule_id:
                line_id = self.line_ids.filtered(lambda s: s.salary_rule_id == sso_company_salary_rule_id)
                print('sso_company line_id: ',line_id)
                if line_id:
                    line_id.update({'amount': self.sso_company_deduct})
                else:
                    line_ids.append((0, 0, {
                        'salary_rule_id': sso_company_salary_rule_id.id,
                        'code': sso_company_salary_rule_id.code,
                        'name': sso_company_salary_rule_id.name,
                        'amount': self.sso_company_deduct,
                    }))

            self.update({'line_ids': line_ids,
                         })

    def _get_period_multiple_payment_sso(self, sso_id):
        sso_salary_rule_id = sso_id.social_id.sso_salary_rule_id
        group_period = self.env['hr.period']
        group_period_payslip_ids = self.env['hr.payslip']
        group_period_sso_amount = 0.0
        group_period_deduct_sso = 0.0
        group_period_deduct_sso_company = 0.0
        if self.hr_period_id:
            period_date_end = self.hr_period_id.date_end
            date_start = date(period_date_end.year, period_date_end.month, 1)
            if period_date_end.month == 12:
                date_end = date(period_date_end.year + 1, 1, 1) - relativedelta(days=1)
            else:
                date_end = date(period_date_end.year, period_date_end.month + 1, 1) - relativedelta(days=1)
            # print('date_start : ',date_start)
            # print('date_end : ',date_end)

            group_period = self.env['hr.period'].search([('state', '=', 'open'),
                                                         ('schedule_pay', '=', self.hr_period_id.schedule_pay),
                                                         ('date_payment', '>=', date_start),
                                                         ('date_payment', '<=', date_end), ], order='date_start asc')
            # print('group_period : ',group_period)
            group_period_payslip_ids = self.env['hr.payslip'].search([('hr_period_id', 'in', group_period.ids),
                                                                      ('employee_id', '=', self.employee_id.id),
                                                                      ('state', 'in', ['done'])
                                                                      ])

            group_period_sso_amount = sum(group_period_payslip_ids.mapped('sso_amount_total'))
            group_period_deduct_sso = sum(group_period_payslip_ids.mapped('sso_deduct'))
            group_period_deduct_sso_company = sum(group_period_payslip_ids.mapped('sso_company_deduct'))

        return {'group_period': group_period,
                'group_payslip': group_period_payslip_ids,
                'group_period_sso_amount': group_period_sso_amount,
                'group_period_deduct_sso': group_period_deduct_sso,
                'group_period_deduct_sso_company': group_period_deduct_sso_company,
                }

    def _get_sso_payslip_done(self):
        summary_pvd = 0.0
        if self.contract_id.pvd_input_type_id:
            input_line_ids = self.input_line_ids.filtered(lambda r: r.input_type_id == self.contract_id.pvd_input_type_id)
            summary_pvd = sum(input_line_ids.mapped('amount'))

        return {'summary_pvd': summary_pvd,
                'sso_deduct': self.sso_deduct,
                'sso_company_paid_total': self.sso_company_deduct,
                }

    def _get_tax_amount_total(self):
        tax_amount_total = 0.0
        if self.line_ids:
            tax_amount_total = sum(self.line_ids.filtered(lambda x: x.salary_rule_id.cal_tax).mapped('total'))

        return tax_amount_total

    def _get_tax_special_amount_total(self):
        tax_amount_total = 0.0
        if self.line_ids:
            tax_amount_total = sum(self.line_ids.filtered(lambda x: x.salary_rule_id.cal_tax_special).mapped('total'))

        return tax_amount_total

    def get_calculate_tax(self, total_revenue_tax, total_tax_paid, base_tax_receive, base_tax_special_receive):
        # print('def get_calculate_tax : ', total_revenue_tax, base_tax_receive, base_tax_special_receive, total_tax_paid)
        if self.date_to:
            date_year = self.date_to.year
        else:
            date_year = datetime.today().year
        tax_id = self.env['personal.income.tax'].search([('year', '=', date_year)], limit=1)
        schedule_pay = INTERVALS[self.hr_period_id.schedule_pay][1]
        calculate_tax = ""
        date_month = self.hr_period_id.number
        month = 1
        for x in range(date_month, schedule_pay, 1):
            month += 1

        result_base_tax_receive = total_revenue_tax + (base_tax_receive * month)
        result_base_tax_one_receive = result_base_tax_receive + base_tax_special_receive
        # print('result_base_tax_receive: ',result_base_tax_receive)
        # print('result_base_tax_one_receive: ',result_base_tax_one_receive)

        calculate_tax += "ยอดรวมภาษีสะสม = รายได้สำหรับคิดภาษีสะสม + (รายได้สำหรับคิดภาษี * เดือนที่เหลือ)" + "\n"
        calculate_tax += "ยอดรวมภาษีสะสม -> %s + ( %s * %s ) = %s \n" % (
            str("{0:,.2f}".format(total_revenue_tax)), str("{0:,.2f}".format(base_tax_receive)), month,
            result_base_tax_receive)
        calculate_tax += "ยอดรวมภาษี(เฉพาะ)สะสม = ยอดรวมภาษีสะสม + รายได้สำหรับคิดภาษี(เฉพาะ)" + "\n"
        calculate_tax += "ยอดรวมภาษี(เฉพาะ)สะสม -> %s +  %s = %s \n" % (
            str("{0:,.2f}".format(result_base_tax_receive)), str("{0:,.2f}".format(base_tax_special_receive)),
            str("{0:,.2f}".format(result_base_tax_one_receive)))

        # ----------------------------------------------------------------
        result_base = self.get_tax_deduct(result_base_tax_receive, month)
        result_one = self.get_tax_deduct(result_base_tax_one_receive, month)

        net_base_tax = self.get_personal_tax(tax_id, result_base)
        net_base_one_tax = self.get_personal_tax(tax_id, result_one)

        net_diff_tax = net_base_one_tax - net_base_tax
        net_diff_tax = net_diff_tax / month

        calculate_tax += "รายได้สำหรับคิดภาษีหลังหักลดหย่อน = %s \n" % (str("{0:,.2f}".format(result_base)))
        calculate_tax += "รายได้สำหรับคิดภาษีหลังหักลดหย่อน(เฉพาะงวด) = %s \n" % (str("{0:,.2f}".format(result_one)))
        calculate_tax += "ยอดภาษีที่คำนวณได้ = %s \n" % (str("{0:,.2f}".format(net_base_tax)))
        calculate_tax += "ยอดภาษี(เฉพาะงวด)ที่คำนวณได้ = %s \n" % (str("{0:,.2f}".format(net_base_one_tax)))
        calculate_tax += "ส่วนต่าง = %s \n" % (str("{0:,.2f}".format(net_diff_tax)))
        calculate_tax += "หักภาษีที่เสียแล้ว = %s \n" % (str("{0:,.2f}".format(total_tax_paid)))

        # หักภาษีที่เสียแล้ว
        net_base_tax = net_base_tax - total_tax_paid
        if net_base_tax < 0.0:
            net_base_tax = 0.0

        result_base_tax = net_base_tax / month
        result = abs(result_base_tax + net_diff_tax)

        calculate_tax += "ยอดที่ได้ = %s นำไปหารงจ่ายทั้งปี คือ %s ครั้ง เป็นจำนวน %s \n" % \
                         (str("{0:,.2f}".format(net_base_tax)), month, str("{0:,.2f}".format(result_base_tax)))

        if base_tax_special_receive > 0.0:
            calculate_tax += "รายได้ไม่คงที่ = %s \n" % (str("{0:,.2f}".format(base_tax_special_receive)))
            calculate_tax += "ภาษีจากรายได้ไม่คงที่ = %s \n" % (str("{0:,.2f}".format(net_base_one_tax)))

        calculate_tax += "ที่ต้องเสียภาษี = %s \n" % (str("{0:,.2f}".format(result)))
        calculate_tax += "รวมยอดที่ต้องนำไปคำนวณภาษี = %s \n" % (str("{0:,.2f}".format(result)))

        result = round(result, 0)

        return {'tax_deduct': result,
                'calculate_tax': calculate_tax}

    def get_tax_deduct(self, result_base_tax_receive, month):
        # print('def get_tax_deduct : ', result_base_tax_receive, month)
        tax_deduct1 = tax_deduct2 = tax_deduct3 = tax_deduct4 = 0.0

        # ยอดรวมภาษีสะสม
        # 5% of net net max 100,000
        tax_deduct1 = result_base_tax_receive * 0.5
        if tax_deduct1 > 100000:
            tax_deduct1 = 100000

        # ค่าลดหย่อน 60,000
        if self.contract_id.hr_tax_deduction_ids:
            tax_deduct2 += sum(self.contract_id.hr_tax_deduction_ids.mapped('amount'))

        # ประกันสังคม
        sso_paid_total = self.contract_id.sso_paid_total
        tax_deduct3 = sso_paid_total + (self.sso_deduct * month)
        # 5% of net max 90000 ** (ประกันสังคมสะสม + ประกันสังคม) * เดือนที่เหลือ
        if not self.contract_id.exclude_sso and tax_deduct3 > 9000:
            tax_deduct3 = 9000
        elif self.contract_id.exclude_sso:
            tax_deduct3 = 0.0

        # เงินกองทุนสำรอง
        # 15 ก่อน ถ้าเกิน 500,000
        if self.contract_id.pvd_input_type_id:
            input_line_ids = self.input_line_ids.filtered(
                lambda r: r.input_type_id == self.contract_id.pvd_input_type_id)
            amount = sum(input_line_ids.mapped('amount'))
            tax_deduct4 = (amount * month)
        if tax_deduct4 > 500000:
            tax_deduct4 = 500000

        # print('tax_deduct --> ',tax_deduct1 ,tax_deduct2 ,tax_deduct3 ,tax_deduct4)
        tax_deduct = tax_deduct1 + tax_deduct2 + tax_deduct3 + tax_deduct4
        # print('tax_deduct = ', tax_deduct)
        # print('result_base_tax_receive -> ', result_base_tax_receive)
        self.tax_deduction = tax_deduct
        result_tax = result_base_tax_receive - tax_deduct

        if result_tax < 0.0:
            result_tax = 0.0

        # print('result_tax -> ',result_tax)
        return result_tax

    def get_personal_tax(self, tax_id, result):
        # print("def get_personal_tax : ", tax_id, result)
        net_tax = i = 0.0
        step_1 = step_1_rate = step_2 = step_2_rate = 0
        step_3 = step_3_rate = step_4 = step_4_rate = 0
        step_5 = step_5_rate = step_6 = step_6_rate = 0
        step_7 = step_7_rate = step_8 = step_8_rate = 0

        for tax_line in tax_id.personal_tax_line_ids.sorted(key=lambda r: r.rate_no):
            i += 1
            if i == 1:
                step_1 = (tax_line.minimum_rate)
                step_1_rate = tax_line.tax_rate / 100
            elif i == 2:
                step_2 = (tax_line.minimum_rate - 1)
                step_2_rate = tax_line.tax_rate / 100
            elif i == 3:
                step_3 = (tax_line.minimum_rate - 1)
                step_3_rate = tax_line.tax_rate / 100
            elif i == 4:
                step_4 = (tax_line.minimum_rate - 1)
                step_4_rate = tax_line.tax_rate / 100
            elif i == 5:
                step_5 = (tax_line.minimum_rate - 1)
                step_5_rate = tax_line.tax_rate / 100
            elif i == 6:
                step_6 = (tax_line.minimum_rate - 1)
                step_6_rate = tax_line.tax_rate / 100
            elif i == 7:
                step_7 = (tax_line.minimum_rate - 1)
                step_7_rate = tax_line.tax_rate / 100
            elif i == 8:
                step_8 = (tax_line.minimum_rate - 1)
                step_8_rate = tax_line.tax_rate / 100

        if result > step_8:
            # print('if result > step_8')
            # print(result, ' > ', step_8)
            net_tax = (result - step_8) * step_8_rate
            result = step_8
            # print("result8 : " + str(result))
            # print("net_tax : " + str(net_tax))
            # print("step_8 : " + str(step_8))

        if result > step_7:
            # print('if result > step_7')
            # print(result, ' > ', step_7)
            net_tax += (result - step_7) * step_7_rate
            result = step_7
            # print("result7 : " + str(result))
            # print("net_tax : " + str(net_tax))
            # print("step_7 : " + str(step_7))

        if result > step_6:
            # print('if result > step_6')
            # print(result, ' > ', step_6)
            net_tax += (result - step_6) * step_6_rate
            result = step_6
            # print("result6 : " + str(result))
            # print("net_tax : " + str(net_tax))
            # print("step_6 : " + str(step_6))

        if result > step_5:
            # print('if result > step_5')
            # print(result, ' > ', step_5)
            net_tax += (result - step_5) * step_5_rate
            result = step_5
            # print("result5 : " + str(result))
            # print("net_tax : " + str(net_tax))
            # print("step_5 : " + str(step_5))

        if result > step_4:
            # print('if result > step_4')
            # print(result, ' > ', step_4)
            # print(result, ' --> ', result - step_4)
            net_tax += (result - step_4) * step_4_rate
            result = step_4
            # print("net_tax : " + str(net_tax))
            # print("result4 : " + str(result))

        if result > step_3:
            # print('if result > step_3')
            # print(result, ' > ', step_3)
            net_tax += (result - step_3) * step_3_rate
            result = step_3
            # print("net_tax : " + str(net_tax))
            # print("result3 : " + str(result))

        if result > step_2:
            # print('if result > step_2')
            # print(result, ' > ', step_2)
            net_tax += (result - step_2) * step_2_rate
            result = step_2
            # print("net_tax : " + str(net_tax))
            # print("result2 : " + str(result))

        if result > step_1:
            # print('if result > step_1')
            # print(result, ' > ', step_1)
            net_tax += (result - step_1) * step_1_rate
            # print("net_tax : " + str(net_tax))
            # print("result1 : " + str(result))

        # print('net_tax : ' + str(net_tax))
        return net_tax

    def get_tax_amount(self):
        total_revenue_tax = self.contract_id.total_revenue_summary_for_tax
        total_revenue_tax_special = self.contract_id.total_revenue_summary_for_tax_special
        total_tax_paid = self.contract_id.total_tax_paid
        base_tax_receive = self._get_tax_amount_total()
        base_tax_special_receive = self._get_tax_special_amount_total()

        res_calculate_tax = self.get_calculate_tax(total_revenue_tax, total_tax_paid,
                                                   base_tax_receive, base_tax_special_receive)
        calculate_tax = res_calculate_tax.get('calculate_tax')
        tax_deduct = res_calculate_tax.get('tax_deduct')

        self.update({'tax_amount_total': base_tax_receive,
                     'tax_special_amount_total': base_tax_special_receive,
                     'tax_deduct': tax_deduct,
                     'calculate_tax': calculate_tax,
                     })

    def get_tax_info(self):
        if self.date_to:
            date_year = self.date_to.year
        else:
            date_year = datetime.today().year
        tax_id = self.env['personal.income.tax'].search([('year', '=', date_year)], limit=1)
        line_ids = []
        if tax_id:
            tax_salary_rule_id = self.env['hr.salary.rule'].search([('code', '=', tax_id.tax_salary_rule_code),
                                                                    ('struct_id', '=', self.struct_id.id)], limit=1)
            if tax_salary_rule_id:
                line_id = self.line_ids.filtered(lambda s: s.salary_rule_id == tax_salary_rule_id)
                # print('tax tax_salary_rule_id: ', line_id)
                if line_id:
                    line_id.update({'amount': self.tax_deduct})
                else:
                    line_ids.append((0, 0, {
                        'salary_rule_id': tax_salary_rule_id.id,
                        'code': tax_salary_rule_id.code,
                        'name': tax_salary_rule_id.name,
                        'amount': self.tax_deduct,
                    }))

            self.update({'line_ids': line_ids,
                         })

    def _get_tax_payslip_done(self):
        summary_net = sum(self.line_ids.filtered(lambda x: x.code == 'NET').mapped('total'))

        return {'tax_deduct': self.tax_deduct,
                'summary_net': summary_net,
                'tax_amount_total': self.tax_amount_total,
                'tax_special_amount_total': self.tax_special_amount_total,
                }

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for obj in self:
            sso_payslip = obj._get_sso_payslip_done()
            summary_pvd = sso_payslip['summary_pvd']
            sso_deduct = sso_payslip['sso_deduct']
            sso_company_paid_total = sso_payslip['sso_company_paid_total']

            summary_pvd = obj.contract_id.summary_pvd + summary_pvd
            sso_paid_total = obj.contract_id.sso_paid_total + sso_deduct
            sso_company_paid_total = obj.contract_id.sso_company_paid_total + sso_company_paid_total

            tax_payslip = obj._get_tax_payslip_done()
            tax_deduct = tax_payslip['tax_deduct']
            summary_net = tax_payslip['summary_net']
            tax_amount_total = tax_payslip['tax_amount_total']
            tax_special_amount_total = tax_payslip['tax_special_amount_total']

            total_tax_paid = obj.contract_id.total_tax_paid + tax_deduct
            total_revenue_summary_net = obj.contract_id.total_revenue_summary_net + summary_net
            total_revenue_summary_for_tax = obj.contract_id.total_revenue_summary_for_tax + tax_amount_total
            total_revenue_summary_for_tax_special = obj.contract_id.total_revenue_summary_for_tax_special + tax_special_amount_total

            obj.contract_id.update({
                'summary_pvd': summary_pvd,
                'sso_paid_total': sso_paid_total,
                'sso_company_paid_total': sso_company_paid_total,
                'total_tax_paid': total_tax_paid,
                'total_revenue_summary_net': total_revenue_summary_net,
                'total_revenue_summary_for_tax': total_revenue_summary_for_tax,
                'total_revenue_summary_for_tax_special': total_revenue_summary_for_tax_special,
                'total_tax_deduction': self.tax_deduction,
            })

        return res