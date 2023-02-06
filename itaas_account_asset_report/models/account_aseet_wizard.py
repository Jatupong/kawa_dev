# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017  www.itaas.co.th

from odoo import models, fields, api, _
from datetime import datetime
#from StringIO import StringIO
#import xlwt
#import base64
from odoo.exceptions import UserError
from odoo.tools import misc
from decimal import *
from dateutil.relativedelta import relativedelta
import calendar
import xlwt
import base64

from io import BytesIO
import xlsxwriter


class account_asset_wizard(models.TransientModel):
    _name = 'account.asset.wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    asset_model = fields.Many2one('account.asset', string='Asset Model')

    def print_report_excel(self):
        print('print_report_xls')
        domain = []
        check_move_line = []
        check_params = []
        check_params_2 = []
        check_asset = []
        check_asset_2 = []
        fl = BytesIO()
        workbook = xlsxwriter.Workbook(fl)
        name = 'Asset_report'
        namexls = 'Asset_report' + '.xls'
        worksheet = workbook.add_worksheet(name)

        for_left_bold_no_border = workbook.add_format({'align': 'left', 'bold': True})
        for_left_bold_border_total = workbook.add_format({'align': 'left', 'bold': True})
        for_left_bold_border_total.set_bottom()
        for_left_bold_border_total.set_top()
        for_left_bold_border_total.set_underline(2)

        for_left_bold_border_total_1 = workbook.add_format({'align': 'left', 'bold': True})
        for_left_bold_border_total_1.set_top()
        for_left_bold_border_total_1.set_underline(2)
        for_center_bold_no_border = workbook.add_format({'align': 'center', 'bold': True})
        for_right_bold_no_border = workbook.add_format({'align': 'right', 'bold': True})

        for_left_no_border = workbook.add_format({'align': 'left'})
        for_center_no_border = workbook.add_format({'align': 'center'})
        for_right_no_border = workbook.add_format({'align': 'right'})

        for_left_bold = workbook.add_format({'align': 'left', 'bold': True, 'border': True})
        for_center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': True})
        for_right_bold = workbook.add_format({'align': 'right', 'bold': True, 'border': True})

        for_left = workbook.add_format({'align': 'left', 'border': True})
        for_center = workbook.add_format({'align': 'center', 'border': True})
        for_right = workbook.add_format({'align': 'right', 'border': True , 'num_format': '#,##0.00'})

        for_right_bold_no_border_date = workbook.add_format({'align': 'right', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_right_border_num_format = workbook.add_format({'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format({'align': 'right', 'bold': True, 'border': True, 'num_format': '#,##0.00'})

        for_center_bold_no_border_date = workbook.add_format(
            {'align': 'center', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_left_bold_no_border_date = workbook.add_format({'align': 'left', 'bold': True, 'num_format': 'dd/mm/yy'})

        for_center_date = workbook.add_format({'align': 'center', 'border': True, 'num_format': 'dd/mm/yyyy'})

        company_id = self.env.company
        date_from = self.date_from.strftime("%d/%m/%Y")
        date_to = self.date_to.strftime("%d/%m/%Y")
        inv_row = 7
        # domain.append([('asset_type', '=', 'purchase'), ('state', '=', 'model')])
        if self.asset_model:
            domain.append(('id', '=', self.asset_model.id))
        domain.append(('asset_type', '=', 'purchase'))
        domain.append(('state', '=', 'model'))
        print('domain:',domain)
        asset_ids = self.env['account.asset'].search(domain)
        print('asset_ids:',asset_ids)
        for asset_id in asset_ids:
            if asset_id.account_asset_id and asset_id.account_asset_id.id not in check_params:
                print('asset_id:',asset_id.id)
                check_asset.append(asset_id)
                check_params.append(asset_id.account_asset_id.id)
            if asset_id.account_depreciation_id and asset_id.account_depreciation_id.id not in check_params_2:
                print('asset_id:',asset_id.id)
                check_asset_2.append(asset_id)
                check_params_2.append(asset_id.account_depreciation_id.id)
        print('check_params:',check_params)
        print('check_params_2:',check_params_2)
        params = (tuple(check_params),self.date_from)
        query = """SELECT aml.account_id,sum(aml.balance)
                        FROM account_move_line AS aml
                        WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date <= %s
                        GROUP BY aml.account_id

                          """
        self.env.cr.execute(query, params)
        start_period_ids = self.env.cr.fetchall()
        print('start_period_ids:',start_period_ids)

        # ==================================================================

        params_2 = (tuple(check_params), self.date_from,self.date_to)
        query = """SELECT aml.account_id,sum(aml.debit),sum(credit)
                               FROM account_move_line AS aml
                               WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date >= %s and date <= %s
                               GROUP BY aml.account_id

                                 """
        self.env.cr.execute(query, params_2)
        start_period_ids_2 = self.env.cr.fetchall()
        print('start_period_ids_2:',start_period_ids_2)

        params_3 = (tuple(check_params), self.date_to)
        query = """SELECT aml.account_id,sum(aml.balance)
                                     FROM account_move_line AS aml
                                     WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date <= %s
                                     GROUP BY aml.account_id

                                       """
        self.env.cr.execute(query, params_3)
        start_period_ids_3 = self.env.cr.fetchall()
        print('start_period_ids_3:',start_period_ids_3)

        worksheet.write(0, 0, 'Date From', for_left_bold_no_border)
        worksheet.write(0, 1, date_from, for_left_bold_no_border)
        worksheet.write(0, 2, 'Date To', for_left_bold_no_border)
        worksheet.write(0, 3, date_to, for_left_bold_no_border)
        worksheet.write(1, 0, 'SEPERATED FINANCIAL STATEMENT - ' + company_id.name, for_left_bold_no_border)

        worksheet.write(3, 2,'Balance as at', for_left_bold_no_border)
        worksheet.write(3, 3,'Additions', for_left_bold_no_border)
        worksheet.write(3, 4,'Disposal', for_left_bold_no_border)
        worksheet.write(3, 5,'Transfers', for_left_bold_no_border)
        worksheet.write(3, 6,'Balance as at', for_left_bold_no_border)

        worksheet.write(4, 2, date_from, for_left_bold_no_border)
        worksheet.write(4, 6, date_to, for_left_bold_no_border)


        worksheet.write(6, 0,'Cost', for_left_bold_no_border)
        print('====================  WRITE  ===========================')

        sum_colum_1 = 0
        sum_colum_2 = 0
        sum_colum_3 = 0
        sum_colum_4 = 0

        for i in check_asset:
            worksheet.write(inv_row, 1, i.name, for_left_bold_no_border)
            for start_period_id in start_period_ids:
                for start_period_id_2 in start_period_ids_2:
                    for start_period_id_3 in start_period_ids_3:
                        if i.account_asset_id.id == start_period_id[0]:
                            if start_period_id[1]:
                                worksheet.write(inv_row, 2, start_period_id[1], for_left_bold_no_border)
                                sum_colum_1 += start_period_id[1]
                        else:
                            break

                        # Colum Debit  /// Credit
                        if i.account_asset_id.id == start_period_id_2[0]:
                            worksheet.write(inv_row, 3, start_period_id_2[1] or '-', for_left_bold_no_border)
                            sum_colum_2 += start_period_id_2[1]
                            worksheet.write(inv_row, 4, start_period_id_2[2] or '-', for_left_bold_no_border)
                            sum_colum_3 += start_period_id_2[2]

                        else:
                            break

                        if i.account_asset_id.id == start_period_id_3[0]:
                            if start_period_id_3[1]:
                                worksheet.write(inv_row, 6, start_period_id_3[1] or '-', for_left_bold_no_border)
                                sum_colum_4 += start_period_id_3[1]
                            else:
                                worksheet.write(inv_row, 6, start_period_id_3[2] or '-', for_left_bold_no_border)
                                sum_colum_4 += start_period_id_3[2]

                        else:
                            break


            inv_row += 1
        inv_row += 1
        worksheet.write(inv_row, 0, 'Total', for_left_bold_no_border)
        worksheet.write(inv_row, 2, sum_colum_1 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 3, sum_colum_2 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 4, sum_colum_3 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 6, sum_colum_4 or '-', for_left_bold_border_total)


        inv_row += 3
        worksheet.write(inv_row, 0,'Accumulated depreciation', for_left_bold_no_border)
        inv_row += 1

        sum_colum_1_1 = 0
        sum_colum_2_2 = 0
        sum_colum_3_3 = 0
        sum_colum_4_4 = 0


        # ==================================================================
        print('========================CASE 2========================')
        print('check_params_2:',check_params_2)
        params = (tuple(check_params_2), self.date_from)
        query = """SELECT aml.account_id,sum(aml.balance)
                                           FROM account_move_line AS aml
                                           WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date <= %s
                                           GROUP BY aml.account_id

                                             """
        self.env.cr.execute(query, params)
        start_period_ids = self.env.cr.fetchall()
        print('start_period_ids:', start_period_ids)

        params_2 = (tuple(check_params_2), self.date_from, self.date_to)
        query = """SELECT aml.account_id,sum(aml.debit),sum(credit)
                                            FROM account_move_line AS aml
                                            WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date >= %s and date <= %s
                                            GROUP BY aml.account_id

                                              """
        self.env.cr.execute(query, params_2)
        start_period_ids_2 = self.env.cr.fetchall()
        print('start_period_ids_2:', start_period_ids_2)

        params_3 = (tuple(check_params_2), self.date_to)
        query = """SELECT aml.account_id,sum(aml.balance)
                                                  FROM account_move_line AS aml
                                                  WHERE aml.account_id IS NOT NULL and aml.account_id IN %s and date <= %s
                                                  GROUP BY aml.account_id

                                                    """
        self.env.cr.execute(query, params_3)
        start_period_ids_3 = self.env.cr.fetchall()
        print('start_period_ids_3:', start_period_ids_3)

        for i in check_asset:
            worksheet.write(inv_row, 1, i.name, for_left_bold_no_border)
            for start_period_id in start_period_ids:
                for start_period_id_2 in start_period_ids_2:
                    for start_period_id_3 in start_period_ids_3:
                        print('TEST:',i.account_asset_id.id)
                        print('TEST:',start_period_id[0])
                        if i.account_depreciation_id.id == start_period_id[0]:

                            if start_period_id[1]:
                                worksheet.write(inv_row, 2, start_period_id[1], for_left_bold_no_border)
                                sum_colum_1_1 += start_period_id[1]
                        else:
                            break
                        # Colum Credit  /// Debit
                        if i.account_depreciation_id.id == start_period_id_2[0]:
                            worksheet.write(inv_row, 3, start_period_id_2[2] or '-', for_left_bold_no_border)
                            sum_colum_2_2 += start_period_id_2[2]
                            worksheet.write(inv_row, 4, start_period_id_2[1] or '-', for_left_bold_no_border)
                            sum_colum_3_3 += start_period_id_2[1]

                        else:
                            break

                        if i.account_depreciation_id.id == start_period_id_3[0]:
                            if start_period_id_3[1]:
                                worksheet.write(inv_row, 6, start_period_id_3[1] or '-', for_left_bold_no_border)
                                sum_colum_4_4 += start_period_id_3[1]

                            else:
                                worksheet.write(inv_row, 6, start_period_id_3[2] or '-', for_left_bold_no_border)
                                sum_colum_4_4 += start_period_id_3[2]

                        else:
                            break

            inv_row += 1
        inv_row += 1
        worksheet.write(inv_row, 0, 'Total', for_left_bold_no_border)
        worksheet.write(inv_row, 2, sum_colum_1_1 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 3, sum_colum_2_2 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 4, sum_colum_3_3 or '-', for_left_bold_border_total)
        worksheet.write(inv_row, 6, sum_colum_4_4 or '-', for_left_bold_border_total)
        inv_row += 1
        worksheet.write(inv_row, 0, 'Property, Plant and equipment', for_left_bold_no_border)
        worksheet.write(inv_row, 2, sum_colum_1_1 - sum_colum_1 or '-', for_left_bold_border_total_1)
        worksheet.write(inv_row, 3, sum_colum_2_2 - sum_colum_2 or '-', for_left_bold_border_total_1)
        worksheet.write(inv_row, 4, sum_colum_3_3 - sum_colum_3 or '-', for_left_bold_border_total_1)
        worksheet.write(inv_row, 6, sum_colum_4_4 - sum_colum_4 or '-', for_left_bold_border_total_1)











        workbook.close()
        buf = fl.getvalue()
        vals = {'name': namexls, 'report_file': base64.encodestring(buf)}
        wizard_id = self.env['account.asset.excel.export'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.asset.excel.export',
            'target': 'new',
            'res_id': wizard_id.id,
        }



class account_asset_excel_export(models.TransientModel):
    _name = 'account.asset.excel.export'

    report_file = fields.Binary('File')
    name = fields.Char(string='File Name', size=32)

    def action_back(self):
        if self._context is None:
            self._context = {}
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.asset.wizard',
            'target': 'new',
        }

