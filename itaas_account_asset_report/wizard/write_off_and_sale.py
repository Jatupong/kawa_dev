# -*- coding: utf-8 -*-
# Copyright (C) 2020-today ITAAS (Dev M)
from six import StringIO
from xlsxwriter import workbook
from odoo import _, api, fields, models
from datetime import datetime, timedelta, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_round
from odoo.exceptions import UserError
import pytz
from io import BytesIO

import xlwt
import base64
from odoo.tools import misc
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone, UTC
from datetime import datetime, time, timedelta
import xlsxwriter


def strToDate(dt):
    return date(int(dt[0:4]), int(dt[5:7]), int(dt[8:10]))

# remove this first by JA, Not sure why need this, default already working
# class AccountAsset_inherit(models.Model):
#     _inherit = 'account.asset'

# @api.onchange('model_id')
# def _onchange_model_id(self):
#     model = self.model_id
#     if model:
#         self.method = model.method
#         # self.method_number = model.method_number
#         self.method_period = model.method_period
#         self.method_progress_factor = model.method_progress_factor
#         self.prorata = model.prorata
#         self.prorata_date = fields.Date.today()
#         self.account_analytic_id = model.account_analytic_id.id
#         self.analytic_tag_ids = [(6, 0, model.analytic_tag_ids.ids)]
#         self.account_depreciation_id = model.account_depreciation_id
#         self.account_depreciation_expense_id = model.account_depreciation_expense_id
#         self.journal_id = model.journal_id
#         self.account_asset_id = model.account_asset_id


class account_account_asset(models.Model):
    _inherit = 'account.account'

    is_asset_vat = fields.Boolean('Is Asset Vat')

class Assetreport_Writeoff(models.TransientModel):
    _name = 'asset.report.write.off'

    date_from = fields.Date(string='Date From', required=True)
    is_unpost = fields.Boolean(string='Include Unposted Entries')
    date_to = fields.Date(string='Date To', required=True)
    report_type = fields.Selection([
        ("registration", "Registration"),
        ("write_off", "Write off"),
        ("sale", "Sale"),
        ("transfer", "Transfer")
    ], string="Type",required=True)

    cost_center_from = fields.Many2one('account.analytic.account', string="Cost Center From")
    cost_center_to = fields.Many2one('account.analytic.account', string="Cost Center To")
    category_id = fields.Many2many('account.asset', string='Category')

    # category_to = fields.Many2one('account.asset', string="Category To")


    # @api.model
    # def default_get(self, fields):
    #     res = super(Assetreport_Writeoff, self).default_get(fields)
    #     curr_date = datetime.now()
    #     curr_month = curr_date.month
    #     from_date = datetime(curr_date.year, 1, 1).date() or False
    #     to_date = datetime(curr_date.year, curr_month, curr_date.day).date() or False
    #     # from_date = datetime(2021, 1, 1).date() or False
    #     # to_date = datetime(2021, 12, 31).date() or False
    #     res.update({'date_from': str(from_date),
    #                 'date_to': str(to_date),
    #                 })
    #     return res


    def get_range(self,date_form,date_to):
        list_month = []
        month_form = date_form.month
        month_to = date_to.month
        for i in range(month_form,month_to+1):
            list_month.append(i)
        return list_month

    def print_report_excel(self):
        print('print_report_xls')
        fl = BytesIO()
        workbook = xlsxwriter.Workbook(fl)
        if self.report_type == 'registration':
            name = 'Asset Report Register'
            namexls = 'Asset Report Register' + '.xls'
        elif self.report_type == 'write_off':
            name = 'Asset Report Write Off'
            namexls = 'Asset Report Write Off' + '.xls'
        elif self.report_type == 'sale':
            name = 'Asset Report Sale'
            namexls = 'Asset Report Sale' + '.xls'
        elif self.report_type == 'transfer':
            name = 'Asset Report Tranfer'
            namexls = 'Asset Report Tranfer' + '.xls'

        worksheet = workbook.add_worksheet(name)
        company_id = self.env.company
        catagory_ids = self.env['account.asset']
        for_center_bold = workbook.add_format({'align': 'left', 'bold': True})
        for_center_bold = workbook.add_format({'align': 'center', 'bold': True})
        for_right_bold_no_border = workbook.add_format({'align': 'right', 'bold': True})

        for_left_no_border = workbook.add_format({'align': 'left'})
        for_center_no_border = workbook.add_format({'align': 'center'})
        for_right_no_border = workbook.add_format({'align': 'right', 'bold': True , 'num_format': '#,##0.00'})

        for_left_bold = workbook.add_format({'align': 'left', 'bold': True, 'border': True})
        for_center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': True})
        for_right_bold = workbook.add_format({'align': 'right', 'bold': True})

        for_left = workbook.add_format({'align': 'left', 'border': True})
        for_center = workbook.add_format({'align': 'center', 'border': True})
        for_right = workbook.add_format({'align': 'right', 'border': True , 'num_format': '#,##0.00'})

        for_right_bold_no_border_date = workbook.add_format({'align': 'right', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_right_border_num_format = workbook.add_format({'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format({'align': 'right', 'bold': True, 'border': True, 'num_format': '#,##0.00'})

        for_border_bottom = workbook.add_format({'align': 'center'})
        for_border_bottom.set_bottom(2)


        for_center_bold_date = workbook.add_format(
            {'align': 'center', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_center_bold_date = workbook.add_format({'align': 'center', 'bold': True, 'num_format': 'dd/mm/yy'})

        for_center_date = workbook.add_format({'align': 'center', 'border': True, 'num_format': 'dd/mm/yy'})

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)

       

        domain = [('date', '>=', self.date_from),
                  ('date', '<=', self.date_to),
                  ('asset_id','!=',False),
                  ('asset_id.active','=',True),
                  ]
        domain_1 = []
        domain_3 = [
            ('acquisition_date', '<=',self.date_from),
            ('book_value', 'in',('0','1')),
            ('depreciated_amount', '=', 0.00),
            ('original_value', 'in', ('1','0')),
            ('depreciation_move_ids', '=', False),
            ('state', '=', 'open'),
            ('asset_disposal_date', '=', False),
        ]
        domain_7 = [
            ('acquisition_date', '>',self.date_from),
            ('acquisition_date', '<=',self.date_to),
            ('book_value', 'in',('0','1')),
            ('depreciated_amount', '=', 0.00),
            ('original_value', 'in', ('1','0')),
            ('depreciation_move_ids', '=', False),
            ('state', '=', 'open'),
            ('asset_disposal_date', '=', False),
        ]


        if self.category_id:
            domain_3.append(('model_id', 'in',self.category_id.ids))
            domain_7.append(('model_id', 'in',self.category_id.ids))

        if not self.is_unpost:
            domain_3.append(('state', '!=', 'draft'))
            domain_7.append(('state', '!=', 'draft'))


        #=================== เคส พิเศษ START
        account_asset = self.env['account.asset'].search(domain_3)
        account_asset_7 = self.env['account.asset'].search(domain_7)
        print('account_asset_domain_3:',account_asset)
        print('account_asset_7:',account_asset_7)
        account_asset_ids = account_asset.filtered(lambda l:l.value_residual == 0)
        account_asset_ids += account_asset_7.filtered(lambda l:l.value_residual == 0)
        print('account_asset_ids:',account_asset_ids)
        #=================== เคส พิเศษ END

        # print(aa)
        if self.report_type:
            if self.report_type == 'registration':
                #ไม่ใช้่ dateform dateto == state open
                #state == close และ disposal_date > date_to
                domain.append(('asset_id.state', 'in',('open','close')))
                domain.append(('asset_remaining_value','>=',0))
                domain_1 = [('asset_id.asset_disposal_date', '>=', self.date_from),
                            ('asset_id.asset_disposal_date', '<=', self.date_to),
                            ('asset_id', '!=', False),
                            ('asset_id.state', '=','close'),
                            ('asset_id.active', '=', True),
                            ('asset_remaining_value','>=',0)]
            elif self.report_type == 'write_off':
                domain.append(('asset_id.state', '=', 'close'))
                # domain.append(('asset_id.disposal_type', '=', 'dispose'))
                domain.append(('asset_remaining_value', '=', 0))
            elif self.report_type == 'sale':
                domain.append(('asset_id.state', '=', 'close'))
                domain.append(('asset_id.disposal_type', '=', 'sell'))
                domain.append(('asset_remaining_value', '=', 0))
        if self.cost_center_from and self.cost_center_to:
            domain_1 = [('code', '>=', self.cost_center_from.code),
                        ('code', '<=', self.cost_center_to.code),
                        ('asset_id.active','=',True)]
            account_analytic_ids = self.env['account.analytic.account'].search(domain_1)
            domain.append(('asset_id.account_analytic_id', 'in',account_analytic_ids.ids))
        if self.category_id:
            domain_2 = [('model_id', 'in',self.category_id.ids)]
            catgory_ids = self.env['account.asset'].search(domain_2)
            domain.append(('asset_id', 'in',catgory_ids.ids))
            domain_1.append(('asset_id', 'in',catgory_ids.ids))
        # if self.is_unpost:
        #     domain.append(('asset_id.state','=','draft'))
        #     domain_1.append(('asset_id.state','=','draft'))
        if not self.is_unpost:
            domain.append(('state','!=','draft'))

        print('domain:',domain)
        move_ids = self.env['account.move'].search(domain)
        if domain_1:
            move_ids |= self.env['account.move'].search(domain_1)
        asset_ids = move_ids.mapped('asset_id')

        domain_4 = [
            ('date', '<', self.date_from),
            ('asset_remaining_value', '=', 0.00),
            ('asset_id.book_value', '=', 1),
            ('asset_id.state', '=', 'open'),
            ('asset_id.asset_disposal_date', '=', False),
        ]
        # domain_5 = [
        #     ('acquisition_date', '<=', self.date_from),
        #     ('original_value', '=', 0.00),
        #     ('purchase_value', '=', 0.00),
        #     ('book_value', '=', 0.00),
        #     ('asset_disposal_date', '=', False),
        #     ('state', '=', 'open'),
        #     ('depreciation_move_ids', '=', False),
        # ]
        domain_6 = [
            ('acquisition_date', '<=', self.date_to),
            ('original_value', '>', 0.00),
            ('purchase_value', '>', 0.00),
            ('book_value', '>', 0.00),
            ('asset_disposal_date', '=', False),
            ('state', '=', 'open'),
            ('depreciation_move_ids', '=', False),
        ]
        if self.category_id:
            # domain_5.append(('model_id', 'in',self.category_id.ids))
            domain_6.append(('model_id', 'in',self.category_id.ids))


        if not self.is_unpost:
            domain_4.append(('state','!=','draft'))

        if asset_ids:
            domain_4.append(('asset_id', 'not in',asset_ids.ids))
        asset_program_end = self.env['account.move'].search(domain_4)
        # account_asset_domain_5_ids = self.env['account.asset'].search(domain_5)
        domain_6.append(('id','not in',move_ids.ids))
        account_asset_domain_6_ids = self.env['account.asset'].search(domain_6)
        asset_program_end_ids = asset_program_end.filtered(lambda l: l.asset_id.value_residual == 0)
        print('asset_program_end_ids:', asset_program_end_ids)
        print('aaaaaa_asset_ids:',asset_ids)
        # print(aaa)
        if move_ids:
            catagory_ids |= move_ids.mapped('asset_id').mapped('model_id')
        if account_asset_ids:
            catagory_ids |= account_asset_ids.mapped('model_id')
        # if account_asset_domain_5_ids:
        #     catagory_ids |= account_asset_domain_5_ids.mapped('model_id')
        if account_asset_domain_6_ids:
            catagory_ids |= account_asset_domain_6_ids.mapped('model_id')


        print('catagory_ids:',catagory_ids)
        if self.report_type == 'registration':
            worksheet.write(0, 0, company_id.name, for_left_no_border)
            worksheet.write(1, 0, 'Report Date :' + str(self.date_to), for_left_no_border)
            worksheet.write(2, 0, 'Depreciation area : ', for_left_no_border)

            worksheet.merge_range(3, 0, 5, 0, 'Group', for_center_bold)
            worksheet.merge_range(3, 1, 5, 1, 'Asset No', for_center_bold)
            worksheet.merge_range(3, 2, 5, 2, 'Asset description', for_center_bold)
            worksheet.merge_range(3, 3, 5, 3, 'Cost Center', for_center_bold)
            worksheet.merge_range(3, 4, 5, 4, 'จำนวน', for_center_bold)
            worksheet.merge_range(3, 5, 5, 5, 'วันที่ซื้อ', for_center_bold)
            worksheet.merge_range(3, 6, 5, 6, 'อัตราค่าเสื่อม', for_center_bold)
            worksheet.merge_range(3, 7, 5, 7, 'ราคาซื้อ', for_center_bold)
            worksheet.merge_range(3, 8, 5, 8, 'ค่าเสือมสะสมยกมา', for_center_bold)
            worksheet.write(3, 9,  'มูลค่าสุทธิยกมา', for_center_bold)
            worksheet.write(4, 9,  self.date_from, for_center_bold_date)
            worksheet.merge_range(3, 10, 3, 26, 'ค่าเสื่อมราคา', for_center_bold)
            worksheet.merge_range(4, 10, 4, 12, 'Q1', for_center_bold)
            worksheet.write(5, 10,  'Jan', for_center_bold)
            worksheet.write(5, 11, 'Feb', for_center_bold)
            worksheet.write(5, 12, 'Mar', for_center_bold)
            worksheet.merge_range(4, 13, 5, 13, 'Total Q1', for_center_bold)
            worksheet.merge_range(4, 14, 4, 16, 'Q2', for_center_bold)
            worksheet.write(5, 14, 'Apr', for_center_bold)
            worksheet.write(5, 15, 'May', for_center_bold)
            worksheet.write(5, 16, 'Jun', for_center_bold)
            worksheet.merge_range(4, 17, 5, 17, 'Total Q2', for_center_bold)
            worksheet.merge_range(4, 18, 4, 20, 'Q3', for_center_bold)
            worksheet.write(5, 18, 'Jul', for_center_bold)
            worksheet.write(5, 19, 'Aug', for_center_bold)
            worksheet.write(5, 20, 'Sept', for_center_bold)
            worksheet.merge_range(4, 21, 5, 21, 'Total Q3', for_center_bold)
            worksheet.merge_range(4, 22, 4, 24, 'Q4', for_center_bold)
            worksheet.write(5, 22, 'Oct', for_center_bold)
            worksheet.write(5, 23, 'Nov', for_center_bold)
            worksheet.write(5, 24, 'Dec', for_center_bold)
            worksheet.merge_range(4, 25, 5, 25, 'Total Q4', for_center_bold)
            worksheet.merge_range(4, 26, 5, 26, 'Total YTD', for_center_bold)
            worksheet.merge_range(3, 27, 5, 27, 'ค่าเสื่อมราคาสะสมยกไป', for_center_bold)
            worksheet.merge_range(3, 28, 5, 28, 'ค่าซาก', for_center_bold)
            worksheet.merge_range(3, 29, 5, 29, 'มูลค่าคงเหลือ', for_center_bold)
            range_month = self.get_range(self.date_from,self.date_to)
            inv_row = 6
            data_temp =[]
            check_asset = []
            print('============= CHECK')
            print('move_ids:',move_ids)
            for catagory_id in catagory_ids:
                for move_id in move_ids.filtered(lambda x: x.asset_id.model_id.id == catagory_id.id):
                    jan=feb=mar=apr=may=jun=jul=aug=sep=oct=nov=dec=0
                    # Quarter 1 START
                    if move_id.date.month == 1:
                        jan += move_id.amount_total
                    if move_id.date.month == 2:
                        feb += move_id.amount_total
                    if move_id.date.month == 3:
                        mar += move_id.amount_total
                    sum_quarter_1 = jan+feb+mar
                    # Quarter 1 END
                    # Quarter 2 START
                    if move_id.date.month == 4:
                        apr += move_id.amount_total
                    if move_id.date.month == 5:
                        may += move_id.amount_total
                    if move_id.date.month == 6:
                        jun += move_id.amount_total
                    sum_quarter_2 = apr+may+jun
                    # Quarter 2 END
                    # Quarter 3 START
                    if move_id.date.month == 7:
                        oct += move_id.amount_total
                    if move_id.date.month == 8:
                        aug += move_id.amount_total
                    if move_id.date.month == 9:
                        sep += move_id.amount_total
                    sum_quarter_3 = oct+aug+sep
                    # Quarter 3 END
                    # Quarter 4 START
                    if move_id.date.month == 10:
                        jul += move_id.amount_total
                    if move_id.date.month == 11:
                        nov += move_id.amount_total
                    if move_id.date.month == 12:
                        dec += move_id.amount_total
                    sum_quarter_4 = jul+nov+dec
                    # Quarter 4 END

                    # purchase < date_form สินทรับเก่า
                    # 1 สินทรัพเก่า
                    # เคส ต่่อเนื่อง ถ้ามี ระดับไลน์ ที่ date < date_form  ให้เอา ฟิว asset_remaining_value เอา รายการ ที่ ใกล้กับ date_from มากที่สุด
                    # เคส ยกมา  ให้เอา original_value  - salvage_value ใน asset_id
                    # 2 สินทรัพเก่า
                    # 0  เสมอ

                    if move_id.asset_id.id not in check_asset:
                        print('===== START =====')
                        print('move_id:',move_id.asset_id)
                        if move_id.asset_id.purchase_date < self.date_from:
                            old_assets = move_id.asset_id.depreciation_move_ids.filtered(lambda x: x.date < self.date_from)
                            if old_assets:
                                print('old_assets:',old_assets)
                                print('old_assets:',old_assets[-1])
                                old_asset_amount = (move_id.asset_id.purchase_value - (old_assets[-1].amount_total + old_assets[-1].asset_remaining_value)) + move_id.asset_id.salvage_value
                            else:
                                print('ELSEEEEEEEEE')
                                old_asset_amount = move_id.asset_id.original_value + move_id.asset_id.salvage_value
                        else:
                            old_asset_amount = 0
                        print('===== END =====')
                        percentage = float_round(100 / (move_id.asset_id.model_id.method_number / 12),2)
                        print('move_id:',move_id)
                        print('asset_id:',move_id.asset_id)
                        print('asset_id:',move_id.asset_id.model_id.method_number   )
                        print('percentage:',percentage)
                        check_asset.append(move_id.asset_id.id)
                        vals={
                            'move_id':move_id,
                            'asset_id':move_id.asset_id,
                            'catagory_id':catagory_id,
                            'account_asset_id':move_id.asset_id.model_id.account_asset_id,
                            'asset_code':move_id.asset_id.code,
                            'asset_name':move_id.asset_id.name,
                            'account_analytic':move_id.asset_id.account_analytic_id,
                            'qty':1,
                            'purchase_date': move_id.asset_id.purchase_date,
                            'percentage': percentage,
                            'purchase_value':move_id.asset_id.purchase_value,
                            'original_value':old_asset_amount,
                            'salvage_value':move_id.asset_id.salvage_value,
                            'sum_quarter_1':sum_quarter_1,
                            'sum_quarter_2':sum_quarter_2,
                            'sum_quarter_3':sum_quarter_3,
                            'sum_quarter_4':sum_quarter_4,
                            'sum_quarter_all':sum_quarter_1 + sum_quarter_2 + sum_quarter_3 + sum_quarter_4,

                            'jan':jan,
                            'feb':feb,
                            'mar':mar,
                            'apr':apr,
                            'may':may,
                            'jun':jun,
                            'oct':oct,
                            'aug':aug,
                            'sep':sep,
                            'jul':jul,
                            'nov':nov,
                            'dec':dec,

                        }
                        data_temp.append(vals)
                    else:
                        asset_check = list(filter(lambda x: x['asset_id'].id == move_id.asset_id.id, data_temp))

                        for list_asset in asset_check:
                            list_asset['sum_quarter_1'] += sum_quarter_1
                            list_asset['sum_quarter_2'] += sum_quarter_2
                            list_asset['sum_quarter_3'] += sum_quarter_3
                            list_asset['sum_quarter_4'] += sum_quarter_4

                            list_asset['sum_quarter_all'] += sum_quarter_1
                            list_asset['sum_quarter_all'] += sum_quarter_2
                            list_asset['sum_quarter_all'] += sum_quarter_3
                            list_asset['sum_quarter_all'] += sum_quarter_4

                            list_asset['jan'] += jan
                            list_asset['feb'] += feb
                            list_asset['mar'] += mar
                            list_asset['apr'] += apr
                            list_asset['may'] += may
                            list_asset['jun'] += jun
                            list_asset['oct'] += oct
                            list_asset['aug'] += aug
                            list_asset['sep'] += sep
                            list_asset['jul'] += jul
                            list_asset['nov'] += nov
                            list_asset['dec'] += dec
            for catagory_id in catagory_ids:
                # print('==== START catagory_id:',catagory_id)
                sum_7 = sum_8 = sum_8_2 = sum_9 = sum_10 = sum_11 = sum_12 = sum_13 = sum_14 = sum_15 = sum_16 = sum_17 = sum_18 = sum_19 = sum_20 = sum_21 = sum_22 = sum_23 = sum_24 = sum_25 = sum_26 = sum_27 = sum_28 = 0
                worksheet.write(inv_row, 0, catagory_id.name, for_center_bold)
                inv_row += 1
                filter_move_ids = list(filter(lambda x: x['catagory_id'].id == catagory_id.id, data_temp))

                for filter_move_id in filter_move_ids:
                    print('TESSTTT1')
                    worksheet.write(inv_row, 0, filter_move_id['asset_id'].model_id.name, for_center)
                    worksheet.write(inv_row, 1, filter_move_id['asset_code'], for_center)
                    worksheet.write(inv_row, 2, filter_move_id['asset_name'], for_center)
                    worksheet.write(inv_row, 3, filter_move_id['account_analytic'].name, for_center)
                    worksheet.write(inv_row, 4, filter_move_id['qty'], for_center)
                    worksheet.write(inv_row, 5, filter_move_id['purchase_date'], for_center_date)
                    worksheet.write(inv_row, 6, str(filter_move_id['percentage']) + '%', for_right)
                    # print('filter_move_ids:',filter_move_ids)
                    if filter_move_id['asset_id'].asset_disposal_date \
                            and filter_move_id['asset_id'].asset_disposal_date >= self.date_from \
                            and filter_move_id['asset_id'].asset_disposal_date <= self.date_to \
                            and filter_move_id['asset_id'].state == 'close' \
                            and filter_move_id['asset_id'].disposal_type == 'dispose':
                        worksheet.write(inv_row, 7, 0.00, for_right)

                    else:
                        worksheet.write(inv_row, 7, filter_move_id['purchase_value'], for_right)
                        sum_7 += filter_move_id['purchase_value']
                    # print('asset_name',filter_move_id['asset_name'])
                    asset_id_not_move_id = filter_move_id['asset_id']
                    account_move_first = asset_id_not_move_id.depreciation_move_ids.filtered(lambda x: x.date > self.date_from)
                    if not filter_move_id['move_id']:
                        print('CAEE 1')
                        #======================================================================
                        worksheet.write(inv_row, 8, ((filter_move_id['purchase_value'] - filter_move_id['original_value']) - filter_move_id['salvage_value']), for_right)
                        sum_8_2 += ((filter_move_id['purchase_value'] - filter_move_id['original_value']) - filter_move_id['salvage_value'])
                        #======================================================================
                        worksheet.write(inv_row, 9, filter_move_id['original_value'], for_right)
                        sum_8 += filter_move_id['original_value']
                        move_id_asset_original = filter_move_id['original_value']
                    else:
                        print('CAEE 2')
                        if account_move_first:
                            print('Case 2.1')
                            #====================================================================

                            worksheet.write(inv_row, 8, ((filter_move_id['purchase_value'] - (account_move_first[0].amount_total + account_move_first[0].asset_remaining_value)) - asset_id_not_move_id.salvage_value), for_right)
                            sum_8_2 += ((filter_move_id['purchase_value'] - (account_move_first[0].amount_total + account_move_first[0].asset_remaining_value)) - asset_id_not_move_id.salvage_value)
                            #=====================================================================
                            worksheet.write(inv_row, 9, (account_move_first[0].amount_total + account_move_first[0].asset_remaining_value) + asset_id_not_move_id.salvage_value, for_right)
                            sum_8 += (account_move_first[0].amount_total + account_move_first[0].asset_remaining_value) + asset_id_not_move_id.salvage_value
                            move_id_asset_original = account_move_first[0].amount_total + account_move_first[0].asset_remaining_value
                        else:
                            move_id_asset_original = 0
                    worksheet.write(inv_row, 10, filter_move_id['jan'] or "", for_right)
                    sum_9 += filter_move_id['jan']


                    worksheet.write(inv_row, 11, filter_move_id['feb'] or "", for_right)
                    sum_10 += filter_move_id['feb']




                    worksheet.write(inv_row, 12, filter_move_id['mar'] or "", for_right)
                    sum_11 += filter_move_id['mar']

                    worksheet.write(inv_row, 13, filter_move_id['sum_quarter_1'] or "", for_right)
                    sum_12 += filter_move_id['sum_quarter_1']


                    worksheet.write(inv_row, 14, filter_move_id['apr'] or "", for_right)
                    sum_13 += filter_move_id['apr']

                    worksheet.write(inv_row, 15, filter_move_id['may'] or "", for_right)
                    sum_14 += filter_move_id['may']

                    worksheet.write(inv_row, 16, filter_move_id['jun'] or "", for_right)
                    sum_15 += filter_move_id['jun']

                    worksheet.write(inv_row, 17, filter_move_id['sum_quarter_2'] or "0.00", for_right)
                    sum_16 += filter_move_id['sum_quarter_2']


                    worksheet.write(inv_row, 18, filter_move_id['oct'] or "", for_right)
                    sum_17 += filter_move_id['oct']

                    worksheet.write(inv_row, 19, filter_move_id['aug'] or "", for_right)
                    sum_18 += filter_move_id['aug']

                    worksheet.write(inv_row, 20, filter_move_id['sep'] or "", for_right)
                    sum_19 += filter_move_id['sep']

                    worksheet.write(inv_row, 21, filter_move_id['sum_quarter_3'] or "0.00", for_right)
                    sum_20 += filter_move_id['sum_quarter_3']

                    worksheet.write(inv_row, 22, filter_move_id['jul'] or "", for_right)
                    sum_21 += filter_move_id['jul']


                    worksheet.write(inv_row, 23, filter_move_id['nov'] or "", for_right)
                    sum_22 += filter_move_id['nov']


                    worksheet.write(inv_row, 24, filter_move_id['dec'] or "", for_right)
                    sum_23 += filter_move_id['dec']


                    worksheet.write(inv_row, 25, filter_move_id['sum_quarter_4'] or "0.00", for_right)
                    sum_24 += filter_move_id['sum_quarter_4']
                    worksheet.write(inv_row, 26, filter_move_id['sum_quarter_all'], for_right)
                    sum_25 += filter_move_id['sum_quarter_all']
                    if account_move_first:
                        colum_8 =  ((filter_move_id['purchase_value'] - (account_move_first[0].amount_total + account_move_first[0].asset_remaining_value)) - asset_id_not_move_id.salvage_value)
                    else:
                        colum_8 =  ((filter_move_id['purchase_value'] - (0.00)) - asset_id_not_move_id.salvage_value)

                    worksheet.write(inv_row, 27, (colum_8 + filter_move_id['sum_quarter_all']), for_right)
                    sum_26 += (colum_8 + filter_move_id['sum_quarter_all'])

                    worksheet.write(inv_row, 28, filter_move_id['salvage_value'], for_right)
                    sum_27 += filter_move_id['salvage_value']

                    worksheet.write(inv_row, 29, filter_move_id['purchase_value'] - (colum_8 + filter_move_id['sum_quarter_all']),for_right)
                    sum_28 += filter_move_id['purchase_value'] - (colum_8 + filter_move_id['sum_quarter_all'])
                    inv_row += 1
                # 3 >> asset
                filter_cat_asset_ids = account_asset_ids.filtered(lambda l: l.model_id.id == catagory_id.id)
                for filter_cat_asset_id in filter_cat_asset_ids:
                    print('filter_cat_asset_id:',filter_cat_asset_id)
                    worksheet.write(inv_row, 0, filter_cat_asset_id.model_id.name, for_center)
                    worksheet.write(inv_row, 1, filter_cat_asset_id.code, for_center)
                    worksheet.write(inv_row, 2, filter_cat_asset_id.name, for_center)
                    worksheet.write(inv_row, 3, filter_cat_asset_id.account_analytic_id.name, for_center)
                    worksheet.write(inv_row, 4, 1, for_center)
                    worksheet.write(inv_row, 5, filter_cat_asset_id.purchase_date, for_center_date)
                    percentage = float_round(100 / (filter_cat_asset_id.model_id.method_number / 12), 2)
                    worksheet.write(inv_row, 6, str(percentage) + '%', for_right)
                    worksheet.write(inv_row, 7, filter_cat_asset_id.purchase_value, for_right)
                    sum_7 += filter_cat_asset_id.purchase_value
                    worksheet.write(inv_row, 8, filter_cat_asset_id.value_residual, for_right)
                    sum_8_2 += filter_cat_asset_id.value_residual
                    sum_8 += filter_cat_asset_id.book_value
                    worksheet.write(inv_row, 9, filter_cat_asset_id.book_value, for_right)
                    worksheet.write(inv_row, 10, '', for_right)
                    worksheet.write(inv_row, 11, '', for_right)
                    worksheet.write(inv_row, 12, '', for_right)
                    worksheet.write(inv_row, 13, 0.00, for_right)
                    worksheet.write(inv_row, 14, '', for_right)
                    worksheet.write(inv_row, 15, '', for_right)
                    worksheet.write(inv_row, 16, '', for_right)
                    worksheet.write(inv_row, 17, 0.00, for_right)
                    worksheet.write(inv_row, 18, '', for_right)
                    worksheet.write(inv_row, 19, '', for_right)
                    worksheet.write(inv_row, 20, '', for_right)
                    worksheet.write(inv_row, 21, 0.00, for_right)
                    worksheet.write(inv_row, 22, '', for_right)
                    worksheet.write(inv_row, 23, '', for_right)
                    worksheet.write(inv_row, 24, '', for_right)
                    worksheet.write(inv_row, 25, 0.00, for_right)
                    worksheet.write(inv_row, 26, 0.00, for_right)
                    worksheet.write(inv_row, 27, filter_cat_asset_id.value_residual, for_right)
                    worksheet.write(inv_row, 28, filter_cat_asset_id.salvage_value, for_right)
                    sum_27 += filter_cat_asset_id.salvage_value
                    worksheet.write(inv_row, 29, filter_cat_asset_id.book_value, for_right)
                    sum_28 += filter_cat_asset_id.book_value

                    sum_26 += filter_cat_asset_id.value_residual
                    # sum_27 += filter_cat_asset_id.value_residual
                    # sum_28 += filter_cat_asset_id.value_residual
                    inv_row += 1

                # 4 >> account.move
                filter_end_asset_ids = asset_program_end_ids.filtered(lambda l: l.asset_id.model_id.id == catagory_id.id)
                for filter_end_asset_id in filter_end_asset_ids:
                    print('filter_end_asset_id:',filter_end_asset_id)
                    worksheet.write(inv_row, 0, filter_end_asset_id.asset_id.model_id.name, for_center)
                    worksheet.write(inv_row, 1, filter_end_asset_id.asset_id.code, for_center)
                    worksheet.write(inv_row, 2, filter_end_asset_id.asset_id.name, for_center)
                    worksheet.write(inv_row, 3, filter_end_asset_id.asset_id.account_analytic_id.name, for_center)
                    worksheet.write(inv_row, 4, 1, for_center)
                    worksheet.write(inv_row, 5, filter_end_asset_id.asset_id.purchase_date, for_center_date)
                    percentage = float_round(100 / (filter_end_asset_id.asset_id.model_id.method_number / 12), 2)
                    worksheet.write(inv_row, 6, str(percentage) + '%', for_right)
                    worksheet.write(inv_row, 7, filter_end_asset_id.asset_id.purchase_value, for_right)
                    sum_7 += filter_end_asset_id.asset_id.purchase_value
                    worksheet.write(inv_row, 8, filter_end_asset_id.asset_id.value_residual, for_right)
                    sum_8_2 += filter_end_asset_id.asset_id.value_residual
                    sum_8 += filter_end_asset_id.asset_id.book_value
                    worksheet.write(inv_row, 9, filter_end_asset_id.asset_id.book_value, for_right)
                    worksheet.write(inv_row, 10, '', for_right)
                    worksheet.write(inv_row, 11, '', for_right)
                    worksheet.write(inv_row, 12, '', for_right)
                    worksheet.write(inv_row, 13, 0.00, for_right)
                    worksheet.write(inv_row, 14, '', for_right)
                    worksheet.write(inv_row, 15, '', for_right)
                    worksheet.write(inv_row, 16, '', for_right)
                    worksheet.write(inv_row, 17, 0.00, for_right)
                    worksheet.write(inv_row, 18, '', for_right)
                    worksheet.write(inv_row, 19, '', for_right)
                    worksheet.write(inv_row, 20, '', for_right)
                    worksheet.write(inv_row, 21, 0.00, for_right)
                    worksheet.write(inv_row, 22, '', for_right)
                    worksheet.write(inv_row, 23, '', for_right)
                    worksheet.write(inv_row, 24, '', for_right)
                    worksheet.write(inv_row, 25, 0.00, for_right)
                    worksheet.write(inv_row, 26, 0.00, for_right)
                    worksheet.write(inv_row, 27, filter_end_asset_id.asset_id.value_residual, for_right)
                    worksheet.write(inv_row, 28, filter_end_asset_id.asset_id.salvage_value, for_right)
                    worksheet.write(inv_row, 29, filter_end_asset_id.asset_id.book_value, for_right)
                    sum_26 += filter_end_asset_id.asset_id.value_residual
                    sum_27 += filter_end_asset_id.asset_id.salvage_value
                    sum_28 += filter_end_asset_id.asset_id.book_value
                    inv_row += 1

                #5 >>asset

                #6 >> asset
                filter_asset_domain_6_ids = account_asset_domain_6_ids.filtered(lambda l: l.original_value != 0 and l.original_value == l.purchase_value and l.original_value == l.book_value and l.model_id.id == catagory_id.id)
                #อีกเคส
                filter_asset_domain_6_ids += account_asset_domain_6_ids.filtered(lambda l: l.original_value != 0 and l.original_value == l.book_value and l.model_id.id == catagory_id.id and l.id not in filter_asset_domain_6_ids.ids)

                print('filter_asset_domain_6_ids:',filter_asset_domain_6_ids)
                for filter_asset_domain_6_id in filter_asset_domain_6_ids:
                    if filter_asset_domain_6_id.id in filter_cat_asset_ids.ids:
                        continue
                    worksheet.write(inv_row, 0, filter_asset_domain_6_id.model_id.name, for_center)
                    worksheet.write(inv_row, 1, filter_asset_domain_6_id.code, for_center)
                    worksheet.write(inv_row, 2, filter_asset_domain_6_id.name, for_center)
                    worksheet.write(inv_row, 3, filter_asset_domain_6_id.account_analytic_id.name, for_center)
                    worksheet.write(inv_row, 4, 1, for_center)
                    worksheet.write(inv_row, 5, filter_asset_domain_6_id.purchase_date, for_center_date)
                    # percentage = float_round(100 / (filter_asset_domain_6_id.model_id.method_number / 12), 2)
                    worksheet.write(inv_row, 6, str(0) + '%', for_right)
                    worksheet.write(inv_row, 7, filter_asset_domain_6_id.purchase_value, for_right)
                    sum_7 += filter_asset_domain_6_id.purchase_value

                    worksheet.write(inv_row, 8, filter_asset_domain_6_id.depreciated_amount, for_right)
                    sum_8_2 += filter_asset_domain_6_id.depreciated_amount
                    sum_8 += filter_asset_domain_6_id.book_value
                    worksheet.write(inv_row, 9, filter_asset_domain_6_id.book_value, for_right)
                    worksheet.write(inv_row, 10, '', for_right)
                    worksheet.write(inv_row, 11, '', for_right)
                    worksheet.write(inv_row, 12, '', for_right)
                    worksheet.write(inv_row, 13, 0.00, for_right)
                    worksheet.write(inv_row, 14, '', for_right)
                    worksheet.write(inv_row, 15, '', for_right)
                    worksheet.write(inv_row, 16, '', for_right)
                    worksheet.write(inv_row, 17, 0.00, for_right)
                    worksheet.write(inv_row, 18, '', for_right)
                    worksheet.write(inv_row, 19, '', for_right)
                    worksheet.write(inv_row, 20, '', for_right)
                    worksheet.write(inv_row, 21, 0.00, for_right)
                    worksheet.write(inv_row, 22, '', for_right)
                    worksheet.write(inv_row, 23, '', for_right)
                    worksheet.write(inv_row, 24, '', for_right)
                    worksheet.write(inv_row, 25, 0.00, for_right)
                    worksheet.write(inv_row, 26, 0.00, for_right)
                    worksheet.write(inv_row, 27, filter_asset_domain_6_id.depreciated_amount, for_right)
                    worksheet.write(inv_row, 28, filter_asset_domain_6_id.salvage_value, for_right)
                    worksheet.write(inv_row, 29, filter_asset_domain_6_id.book_value, for_right)
                    sum_26 += filter_asset_domain_6_id.depreciated_amount
                    sum_27 += filter_asset_domain_6_id.salvage_value
                    sum_28 += filter_asset_domain_6_id.book_value
                    inv_row += 1
                # print(aaa)
                worksheet.write(inv_row, 6, "รวม",for_right_bold)
                worksheet.write(inv_row, 7, sum_7 or '',for_right_no_border)
                worksheet.write(inv_row, 8, sum_8_2 or '',for_right_no_border)
                worksheet.write(inv_row, 9, sum_8 or '',for_right_no_border)
                worksheet.write(inv_row, 10, sum_9 or '',for_right_no_border)
                worksheet.write(inv_row, 11, sum_10 or '',for_right_no_border)
                worksheet.write(inv_row, 12, sum_11 or '',for_right_no_border)
                worksheet.write(inv_row, 13, sum_12 or '',for_right_no_border)
                worksheet.write(inv_row, 14, sum_13 or '',for_right_no_border)
                worksheet.write(inv_row, 15, sum_14 or '',for_right_no_border)
                worksheet.write(inv_row, 16, sum_15 or '',for_right_no_border)
                worksheet.write(inv_row, 17, sum_16 or '',for_right_no_border)
                worksheet.write(inv_row, 18, sum_17 or '',for_right_no_border)
                worksheet.write(inv_row, 19, sum_18 or '',for_right_no_border)
                worksheet.write(inv_row, 20, sum_19 or '',for_right_no_border)
                worksheet.write(inv_row, 21, sum_20 or '',for_right_no_border)
                worksheet.write(inv_row, 22, sum_21 or '',for_right_no_border)
                worksheet.write(inv_row, 23, sum_22 or '',for_right_no_border)
                worksheet.write(inv_row, 24, sum_23 or '',for_right_no_border)
                worksheet.write(inv_row, 25, sum_24 or '',for_right_no_border)
                worksheet.write(inv_row, 26, sum_25 or '',for_right_no_border)
                worksheet.write(inv_row, 27, sum_26 or '',for_right_no_border)
                worksheet.write(inv_row, 28, sum_27 or '',for_right_no_border)
                worksheet.write(inv_row, 29, sum_28 or '',for_right_no_border)

                inv_row += 1
                worksheet.write(inv_row, 0, '', for_border_bottom)
                worksheet.write(inv_row, 1, '', for_border_bottom)
                worksheet.write(inv_row, 2, '', for_border_bottom)
                worksheet.write(inv_row, 3, '', for_border_bottom)
                worksheet.write(inv_row, 4, '', for_border_bottom)
                worksheet.write(inv_row, 5, '', for_border_bottom)
                worksheet.write(inv_row, 6, '', for_border_bottom)
                worksheet.write(inv_row, 7, '', for_border_bottom)
                worksheet.write(inv_row, 8, '', for_border_bottom)
                worksheet.write(inv_row, 9, '', for_border_bottom)
                worksheet.write(inv_row, 10, '', for_border_bottom)
                worksheet.write(inv_row, 11, '', for_border_bottom)
                worksheet.write(inv_row, 12, '', for_border_bottom)
                worksheet.write(inv_row, 13, '', for_border_bottom)
                worksheet.write(inv_row, 14, '', for_border_bottom)
                worksheet.write(inv_row, 15, '', for_border_bottom)
                worksheet.write(inv_row, 16, '', for_border_bottom)
                worksheet.write(inv_row, 17, '', for_border_bottom)
                worksheet.write(inv_row, 18, '', for_border_bottom)
                worksheet.write(inv_row, 19, '', for_border_bottom)
                worksheet.write(inv_row, 20, '', for_border_bottom)
                worksheet.write(inv_row, 21, '', for_border_bottom)
                worksheet.write(inv_row, 22, '', for_border_bottom)
                worksheet.write(inv_row, 23, '', for_border_bottom)
                worksheet.write(inv_row, 24, '', for_border_bottom)
                worksheet.write(inv_row, 25, '', for_border_bottom)
                worksheet.write(inv_row, 26, '', for_border_bottom)
                worksheet.write(inv_row, 27, '', for_border_bottom)
                worksheet.write(inv_row, 28, '', for_border_bottom)
                worksheet.write(inv_row, 29, '', for_border_bottom)
                inv_row += 2

        elif self.report_type == 'write_off':
            worksheet.write(0, 0, company_id.name, for_left_no_border)
            worksheet.write(1, 0, 'Report Date :' + str(self.date_to), for_left_no_border)
            worksheet.write(2, 0, 'Asset No', for_center_bold)
            worksheet.write(2, 1, 'Category', for_center_bold)
            worksheet.write(2, 2, 'Group', for_center_bold)
            worksheet.write(2, 3, 'Asset Description', for_center_bold)
            worksheet.write(2, 4, 'Cost Center', for_center_bold)
            worksheet.write(2, 5, 'จำนวน', for_center_bold)
            worksheet.write(2, 6, 'ราคาซื้อ', for_center_bold)
            worksheet.write(2, 7, 'ค่าเสื่อมราคาสะสม', for_center_bold)
            worksheet.write(2, 8, 'มูลค่าคงเหลือ', for_center_bold)
            worksheet.write(2, 9, 'วันที่ Write off', for_center_bold)
            worksheet.write(2, 10, 'ขาดทุนจากการตัดจำหน่าย', for_center_bold)
            inv_row = 3
            sum_colum_1 = 0
            sum_colum_2 = 0
            sum_colum_3 = 0
            sum_colum_5 = 0
            for move_id in move_ids:
                print('move_id_write_off:',move_id.asset_id)
                worksheet.write(inv_row, 0, move_id.asset_id.code, for_center)
                worksheet.write(inv_row, 1, move_id.asset_id.model_id.name, for_center)
                worksheet.write(inv_row, 2, move_id.asset_id.model_id.account_asset_id.name, for_center)
                worksheet.write(inv_row, 3, move_id.asset_id.name, for_center)
                worksheet.write(inv_row, 4, move_id.asset_id.model_id.account_analytic_id.name, for_center)
                worksheet.write(inv_row, 5, '1', for_right)
                worksheet.write(inv_row, 6, move_id.asset_id.purchase_value, for_right)
                total_sum = sum(move_id.line_ids.filtered(lambda a: a.account_id == move_id.asset_id.model_id.account_depreciation_id).mapped('balance'))
                worksheet.write(inv_row, 7, total_sum, for_right)
                worksheet.write(inv_row, 8, move_id.asset_id.purchase_value - total_sum, for_right)
                worksheet.write(inv_row, 9, move_id.date, for_center_date)
                # worksheet.write(inv_row, 10, move_id.asset_depreciated_value, for_right)
                worksheet.write(inv_row, 10, move_id.asset_id.purchase_value - total_sum, for_right)

                sum_colum_1 += move_id.asset_id.purchase_value
                sum_colum_2 += total_sum
                sum_colum_5 += move_id.asset_depreciated_value
                sum_colum_3 += move_id.asset_id.purchase_value - total_sum
                inv_row += 1
            worksheet.write(inv_row, 6, sum_colum_1, for_right)
            worksheet.write(inv_row, 7, sum_colum_2, for_right)
            worksheet.write(inv_row, 8, sum_colum_3, for_right)
            worksheet.write(inv_row, 10, sum_colum_3, for_right)
            inv_row += 1
            worksheet.write(inv_row, 0, '', for_border_bottom)
            worksheet.write(inv_row, 1, '', for_border_bottom)
            worksheet.write(inv_row, 2, '', for_border_bottom)
            worksheet.write(inv_row, 3, '', for_border_bottom)
            worksheet.write(inv_row, 4, '', for_border_bottom)
            worksheet.write(inv_row, 5, '', for_border_bottom)
            worksheet.write(inv_row, 6, '', for_border_bottom)
            worksheet.write(inv_row, 7, '', for_border_bottom)
            worksheet.write(inv_row, 8, '', for_border_bottom)
            worksheet.write(inv_row, 9, '', for_border_bottom)
            worksheet.write(inv_row, 10, '', for_border_bottom)
            inv_row += 2
        elif self.report_type == 'sale':
            worksheet.write(0, 0, company_id.name, for_left_no_border)
            worksheet.write(1, 0, 'Report Date :'+ str(self.date_from) +'  '+ str(self.date_to), for_left_no_border)
            worksheet.write(2, 0, 'Asset No', for_center_bold)
            worksheet.write(2, 1, 'Category', for_center_bold)
            worksheet.write(2, 2, 'Group', for_center_bold)
            worksheet.write(2, 3, 'Asset Description', for_center_bold)
            worksheet.write(2, 4, 'Cost Center', for_center_bold)
            worksheet.write(2, 5, 'จำนวน', for_center_bold)
            worksheet.write(2, 6, 'ราคาซื้อ', for_center_bold)
            worksheet.write(2, 7, 'ค่าเสื่อมราคาสะสม', for_center_bold)
            worksheet.write(2, 8, 'มูลค่าคงเหลือ', for_center_bold)
            worksheet.write(2, 9, 'วันที่ขาย', for_center_bold)
            worksheet.write(2, 10, 'ราคาขาย(ไม่รวมVat)', for_center_bold)
            worksheet.write(2, 11, 'กำไรขาดทุนจากการจำหน่าย', for_center_bold)
            inv_row = 3
            sum_colum_6 = 0
            sum_colum_7 = 0
            sum_colum_8 = 0
            sum_colum_9 = 0
            sum_colum_10 = 0
            for move_id in move_ids:
                worksheet.write(inv_row, 0, move_id.asset_id.code, for_center)
                worksheet.write(inv_row, 1, move_id.asset_id.model_id.name, for_center)
                worksheet.write(inv_row, 2, move_id.asset_id.model_id.account_asset_id.name, for_center)
                worksheet.write(inv_row, 3, move_id.asset_id.name, for_center)
                worksheet.write(inv_row, 4, move_id.asset_id.model_id.account_analytic_id.name, for_center)
                worksheet.write(inv_row, 5, '1', for_right)
                worksheet.write(inv_row, 6, move_id.asset_id.purchase_value, for_right)
                total_sum = sum(move_id.line_ids.filtered(lambda a: a.account_id == move_id.asset_id.model_id.account_depreciation_id).mapped('balance'))
                profit_total = sum(move_id.line_ids.filtered(lambda a: a.account_id.code == '4211-04').mapped('balance'))
                vat_total = sum(move_id.line_ids.filtered(lambda a: a.account_id.is_asset_vat == True).mapped('balance'))
                worksheet.write(inv_row, 7, total_sum, for_right)
                worksheet.write(inv_row, 8, move_id.asset_id.purchase_value - total_sum, for_right)
                worksheet.write(inv_row, 9, move_id.asset_id.date, for_center_date)
                worksheet.write(inv_row, 10, vat_total, for_right)
                worksheet.write(inv_row, 11, profit_total, for_right)
                sum_colum_6 += move_id.asset_id.purchase_value
                sum_colum_7 += total_sum
                sum_colum_8 += move_id.asset_id.purchase_value - total_sum
                sum_colum_9 += vat_total
                sum_colum_10 += profit_total
                inv_row += 1
            worksheet.write(inv_row, 6,sum_colum_6, for_right)
            worksheet.write(inv_row, 7,sum_colum_7, for_right)
            worksheet.write(inv_row, 8,sum_colum_8, for_right)
            worksheet.write(inv_row, 9,'', for_right)
            worksheet.write(inv_row, 10,sum_colum_9, for_right)
            worksheet.write(inv_row, 11,sum_colum_10, for_right)
            inv_row += 1
            worksheet.write(inv_row, 0, '', for_border_bottom)
            worksheet.write(inv_row, 1, '', for_border_bottom)
            worksheet.write(inv_row, 2, '', for_border_bottom)
            worksheet.write(inv_row, 3, '', for_border_bottom)
            worksheet.write(inv_row, 4, '', for_border_bottom)
            worksheet.write(inv_row, 5, '', for_border_bottom)
            worksheet.write(inv_row, 6, '', for_border_bottom)
            worksheet.write(inv_row, 7, '', for_border_bottom)
            worksheet.write(inv_row, 8, '', for_border_bottom)
            worksheet.write(inv_row, 9, '', for_border_bottom)
            worksheet.write(inv_row, 10, '', for_border_bottom)
            worksheet.write(inv_row, 11, '', for_border_bottom)
            inv_row += 2
        elif self.report_type == 'transfer':
            domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('asset_id', '!=', False)]
            if self.cost_center_from and self.cost_center_to:
                domain_1 = [('code', '>=', self.cost_center_from.code), ('code', '<=', self.cost_center_to.code)]
                account_analytic_ids = self.env['account.analytic.account'].search(domain_1)
                domain.append(('asset_id.account_analytic_id', 'in', account_analytic_ids.ids))
            if self.category_id:
                domain_2 = [('model_id', 'in', self.category_id.ids)]
                catgory_ids = self.env['account.asset'].search(domain_2)
                print('catgory_ids:', catgory_ids)
                domain.append(('asset_id', 'in', catgory_ids.ids))

            move_ids = self.env['asset.move'].search(domain)
            catagory_ids = move_ids.mapped('asset_id').mapped('model_id')
            worksheet.write(0, 0, company_id.name, for_left_no_border)
            worksheet.write(1, 0, 'Report Date :' + str(self.date_from) + '  ' + str(self.date_to), for_left_no_border)
            worksheet.write(2, 0, 'Asset No', for_center_bold)
            worksheet.write(2, 1, 'Asset Description', for_center_bold)
            worksheet.write(2, 2, 'Employee', for_center_bold)
            worksheet.write(2, 3, 'จำนวน', for_center_bold)
            worksheet.write(2, 4, 'วันที่ซื้อ', for_center_bold)
            worksheet.write(2, 5, 'วันที่โอน', for_center_bold)
            worksheet.write(2, 6, 'Tranfer method', for_center_bold)
            worksheet.write(2, 7, 'Tranfer detail', for_center_bold)
            worksheet.write(2, 8, 'อัตราค่าเสื่อมเดิม', for_center_bold)
            worksheet.write(2, 9, 'อัตราค่าเสื่อมใหม่', for_center_bold)
            worksheet.write(2, 10, 'ราคาซื้อ', for_center_bold)
            worksheet.write(2, 11, 'มูลค่า ณ วันที่ Tranfer', for_center_bold)
            worksheet.write(2, 12, 'ค่าเสื่อมราคาสะสม', for_center_bold)
            worksheet.write(2, 13, 'ค่าซาก', for_center_bold)
            worksheet.write(2, 14, 'มูลค่าคงเหลือ', for_center_bold)
            inv_row=3
            for catagory_id in catagory_ids:
                worksheet.write(inv_row, 0,catagory_id.name, for_center_bold)
                inv_row +=1
                colum_1=colum_2=colum_3=colum_4=colum_5 = 0
                for move_id in move_ids.filtered(lambda x: x.asset_id.model_id == catagory_id):
                    worksheet.write(inv_row, 0, move_id.asset_id.code, for_center)
                    worksheet.write(inv_row, 1, move_id.asset_id.name, for_center)
                    worksheet.write(inv_row, 2, move_id.asset_id.employee_id.name or '', for_center)
                    worksheet.write(inv_row, 3, '1', for_center)
                    worksheet.write(inv_row, 4, move_id.asset_id.purchase_date, for_center_date)
                    worksheet.write(inv_row, 5, move_id.date, for_center_date)
                    if move_id.type == '0':
                        tranfer_method = 'Location'
                        tranfer_detail = str(move_id.from_location_id.name) + ' - ' +str(move_id.to_location_id.name)
                    elif move_id.type == '1':
                        tranfer_method = 'Department'
                        tranfer_detail = str(move_id.from_department_id.name) + ' - ' + str(move_id.to_department_id.name)
                    elif move_id.type == '2':
                        tranfer_method = 'Employee'
                        tranfer_detail = str(move_id.from_employee_id.name) + ' - ' + str(move_id.to_employee_id.name)
                    elif move_id.type == '3':
                        tranfer_method = 'Category'
                        tranfer_detail = str(move_id.from_model_id.name) + ' - ' + str(move_id.to_model_id.name)
                    else:
                        tranfer_method = ' '
                        tranfer_detail = ' '
                    worksheet.write(inv_row, 6, tranfer_method, for_center)
                    worksheet.write(inv_row, 7, tranfer_detail, for_center)
                    if move_id.type == '3':
                        worksheet.write(inv_row, 8, str(100 / (move_id.from_model_id.method_number / 12)) + '%', for_right)
                        # worksheet.write(inv_row, 9, str(100 /(move_id.to_model_id.method_number / 12)) + '%',for_right)
                        worksheet.write(inv_row, 9, str(move_id.amount_depreciation_new) + '%',for_right)
                    else:
                        worksheet.write(inv_row, 8, str(100 / (move_id.asset_id.model_id.method_number / 12)) + '%',for_right)
                        # worksheet.write(inv_row, 9, str(100 /(move_id.asset_id.model_id.method_number / 12)) + '%',for_right)
                        worksheet.write(inv_row, 9, str(move_id.amount_depreciation_new) + '%',for_right)

                    worksheet.write(inv_row, 10, move_id.asset_id.purchase_value, for_right)
                    worksheet.write(inv_row, 11, move_id.transfer_value or move_id.asset_id.purchase_value, for_right)
                    line_asset = move_id.asset_id.depreciation_move_ids.filtered(lambda x: x.date < move_id.date)
                    if line_asset:
                        worksheet.write(inv_row, 12, line_asset[-1].asset_depreciated_value, for_right)
                        worksheet.write(inv_row, 14,move_id.asset_id.purchase_value - line_asset[-1].asset_depreciated_value,for_right)
                        colum_5 += move_id.asset_id.purchase_value - line_asset[-1].asset_depreciated_value
                        colum_3 += line_asset[-1].asset_depreciated_value

                    else:
                        worksheet.write(inv_row, 12, '', for_right)

                    worksheet.write(inv_row, 13, move_id.asset_id.salvage_value, for_right)
                    colum_1+= move_id.asset_id.purchase_value
                    colum_2+= move_id.transfer_value
                    colum_4+= move_id.asset_id.salvage_value
                    inv_row += 1
                worksheet.write(inv_row, 10,colum_1,for_right)
                worksheet.write(inv_row, 11,colum_2,for_right)
                worksheet.write(inv_row, 12,colum_3,for_right)
                worksheet.write(inv_row, 13,colum_4,for_right)
                worksheet.write(inv_row, 14,colum_5,for_right)
                inv_row += 1

            inv_row += 1
            worksheet.write(inv_row, 0, '', for_border_bottom)
            worksheet.write(inv_row, 1, '', for_border_bottom)
            worksheet.write(inv_row, 2, '', for_border_bottom)
            worksheet.write(inv_row, 3, '', for_border_bottom)
            worksheet.write(inv_row, 4, '', for_border_bottom)
            worksheet.write(inv_row, 5, '', for_border_bottom)
            worksheet.write(inv_row, 6, '', for_border_bottom)
            worksheet.write(inv_row, 7, '', for_border_bottom)
            worksheet.write(inv_row, 8, '', for_border_bottom)
            worksheet.write(inv_row, 9, '', for_border_bottom)
            worksheet.write(inv_row, 10, '', for_border_bottom)
            worksheet.write(inv_row, 11, '', for_border_bottom)
            worksheet.write(inv_row, 12, '', for_border_bottom)
            worksheet.write(inv_row, 13, '', for_border_bottom)
            worksheet.write(inv_row, 14, '', for_border_bottom)
            inv_row += 2
        workbook.close()
        buf = fl.getvalue()
        vals = {'name': namexls, 'report_file': base64.encodestring(buf)}
        self._cr.execute("TRUNCATE asset_report_write_off CASCADE")
        wizard_id = self.env['asset.write.off.excel.export'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'asset.write.off.excel.export',
            'target': 'new',
            'res_id': wizard_id.id,
        }




def convert_usertz_to_utc(self, date_time):
    user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
    tz = pytz.timezone('UTC')
    date_time = user_tz.localize(date_time).astimezone(tz)
    # date_time = date_time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    return date_time



class wizard_asset_write_off_report_excel(models.TransientModel):
    _name = 'asset.write.off.excel.export'

    report_file = fields.Binary('File')
    name = fields.Char(string='File Name', size=32)

    # @api.multi
    def action_back(self):
        if self._context is None:
            self._context = {}
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'asset.report.write.off',
            'target': 'new',
        }


