# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, models, fields, _
from datetime import datetime, timedelta, date, time
from odoo.exceptions import UserError
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import io
import base64


class DemoReqSpecificXls(models.AbstractModel):
    _name = 'report.kawa_print_requisitions_report.demo_req_specific_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # left
        for_left = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'valign': 'top'})
        for_left_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'border': True})
        for_left_bold = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'valign': 'top', 'align': 'left', 'bold': True})
        for_left_bold_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'bold': True, 'border': True})
        for_left_date = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'num_format': 'dd/mm/yyyy'})
        for_left_bottom_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left'})
        for_left_bottom_border.set_bottom()

        # right
        for_right = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right'})
        for_right_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True})
        for_right_bold = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'valign': 'top', 'align': 'right', 'bold': True})
        for_right_bold_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'bold': True})
        for_right_border_int_num_format = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'num_format': '#,##0'})
        for_right_border_num_format = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'bold': True, 'num_format': '#,##0.00'})

        # center
        for_center = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center'})
        for_center_bold = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'bold': True})
        for_center_bold_underline = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'bold': True, 'underline': True,})
        for_center_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True})
        for_center_bold_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'valign': 'vcenter', 'align': 'center', 'bold': True, 'border': True})
        for_center_border_int_num_format = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': '#,##0'})
        for_center_border_num_format = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': '#,##0.00'})
        for_center_date = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': 'dd/mm/yyyy'})
        for_center_datetime = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': 'dd/mm/yyyy HH:MM'})

        worksheet = workbook.add_worksheet('Page 1')
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 20)

        def convert_utc_to_usertz(date_time):
            if not date_time:
                return ''
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            tz = pytz.timezone('UTC')
            date_time = tz.localize(fields.Datetime.from_string(date_time)).astimezone(user_tz)
            date_time = date_time.strftime('%d/%m/%Y %H:%M')

            return date_time

        picking_id = lines

        i_row = 0
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row, i_col + 8, 'แบบฟอร์มใบเบิกตัวอย่าง', for_center_bold_underline)

        # right
        i_row = 2
        i_col = 5
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'วันที่ต้องการตัวอย่าง', for_left_bold)
        i_col += 2
        if picking_id.scheduled_date:
            worksheet.merge_range(i_row, i_col, i_row, i_col + 1, picking_id.scheduled_date, for_left_date)
        else:
            worksheet.merge_range(i_row, i_col, i_row, i_col + 1, '...........................................', for_left)

        # left
        i_row = 2
        i_col = 0
        worksheet.write(i_row, i_col, 'วันที่', for_right_bold)
        i_col += 1
        if picking_id.create_date:
            worksheet.write(i_row, i_col, picking_id.create_date, for_left_date)
        else:
            worksheet.write(i_row, i_col, '...........................................', for_left)

        i_row += 1
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'วัตถุประสงค์การใช้งาน', for_left_bold)

        i_col += 2
        requisition_type_ids = self.env['material.purchase.requisition.type'].sudo().search([])
        for req_type in requisition_type_ids:
            if req_type.id == picking_id.type_request_id.id:
                worksheet.write(i_row, i_col, '[ / ]', for_right)
            else:
                worksheet.write(i_row, i_col, '[  ]', for_right)
            i_col += 1
            worksheet.merge_range(i_row, i_col, i_row, i_col + 4, req_type.name, for_left)
            i_row += 1
            i_col = 2

        i_row += 1
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row + 1, i_col, 'คลัง', for_center_bold_border)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 2, 'ผู้เบิกสินค้าตัวอย่าง', for_center_bold_border)
        i_col += 3
        worksheet.merge_range(i_row, i_col, i_row, i_col + 3, 'จำนวน', for_center_bold_border)
        i_col += 4
        worksheet.merge_range(i_row, i_col, i_row + 1, i_col, 'lot.no', for_center_bold_border)

        i_col = 0
        i_row += 1
        i_col += 1
        worksheet.write(i_row, i_col, 'ลำดับ', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'รายการ', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ลูกค้า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'น้ำหนัก(kgs.)', for_center_bold_border)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'หน่วย', for_center_bold_border)
        i_col += 2
        worksheet.write(i_row, i_col, 'รวม', for_center_bold_border)

        i_num = 0
        for line in picking_id.move_line_ids:
            i_row += 1
            i_num += 1
            i_col = 0
            worksheet.write(i_row, i_col, line.location_dest_id.name, for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, i_num, for_center_border_int_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.product_id.name, for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, line.move_id.partner_id.name or '', for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, line.product_id.weight, for_right_border_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.qty_done, for_right_border_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.product_uom_id.display_name, for_left_border)
            i_col += 1
            sum_weight = line.product_id.weight * line.qty_done
            worksheet.write(i_row, i_col, sum_weight, for_right_border_num_format)
            i_col += 1
            if line.lot_id:
                worksheet.write(i_row, i_col, line.lot_id.name, for_left_border)
            else:
                worksheet.write(i_row, i_col, line.lot_name or '', for_left_border)

        i_row += 3
        i_col = 0
        worksheet.write(i_row, i_col, 'ชื่อผู้เบิก', for_right)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 2, '', for_left_bottom_border)
        i_col += 3
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'ฝ่ายคลังสินค้า', for_left)
        i_col += 2
        worksheet.merge_range(i_row, i_col, i_row, i_col + 2, '', for_left_bottom_border)
        i_col += 3

        i_row += 2
        i_col = 0
        worksheet.write(i_row, i_col, 'ผู้ตัด Stock', for_right)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 2, '', for_left_bottom_border)
        i_col += 3
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'ผู้อนุมัติกรณีตัดจากคลัง', for_left)
        i_col += 2
        worksheet.merge_range(i_row, i_col, i_row, i_col + 2, '', for_left_bottom_border)
        i_col += 3

        i_row += 1
        i_col = 4
        worksheet.write(i_row, i_col, '01,04,05 (ของดี)', for_left)

        workbook.close()