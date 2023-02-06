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


class DemoReqReportxls(models.AbstractModel):
    _name = 'report.kawa_print_requisitions_report.demo_req_report_xls'
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
        worksheet.set_column('A:A', 1)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 10)
        worksheet.set_column('K:K', 1)

        def convert_utc_to_usertz(date_time):
            if not date_time:
                return ''
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            tz = pytz.timezone('UTC')
            date_time = tz.localize(fields.Datetime.from_string(date_time)).astimezone(user_tz)
            date_time = date_time.strftime('%d/%m/%Y %H:%M')

            return date_time

        picking_id = lines

        company_image = io.BytesIO(base64.b64decode(picking_id.company_id.logo))
        worksheet.insert_image(0, 4, "image.png", {'image_data': company_image, 'x_scale': 0.5, 'y_scale': 0.5})

        i_row = 5
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row, i_col + 10, 'ใบขอซื้อสินค้า / ใบขอเบิกสินค้า', for_center_bold_underline)

        # right
        i_row += 1
        i_col = 8
        worksheet.write(i_row, i_col, 'วันที่/Date', for_left_bold)
        i_col += 1
        if picking_id.scheduled_date:
            worksheet.write(i_row, i_col, picking_id.scheduled_date, for_left_date)
        else:
            worksheet.write(i_row, i_col, '...........................................', for_left)

        # left
        i_row = 8
        i_col = 1
        worksheet.write(i_row, i_col, 'แผนก', for_right_bold)
        i_col += 1
        if picking_id.create_date:
            worksheet.write(i_row, i_col, picking_id.custom_requisition_id.department_id.name or '', for_left_date)
        else:
            worksheet.write(i_row, i_col, '...........................................', for_left)

        i_row += 1
        i_col = 1
        worksheet.write(i_row, i_col, 'หมายเหตุ', for_right_bold)
        i_col += 1
        if picking_id.create_date:
            worksheet.write(i_row, i_col, picking_id.note, for_left_date)
        else:
            worksheet.write(i_row, i_col, '...........................................', for_left)

        i_row = 8
        i_col += 2
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'วัตถุประสงค์การใช้งาน', for_left_bold)

        i_col += 2
        requisition_type_ids = self.env['material.purchase.requisition.type'].sudo().search([])
        for req_type in requisition_type_ids:
            if req_type.id == picking_id.type_request_id.id:
                worksheet.write(i_row, i_col, '[ / ]', for_right)
            else:
                worksheet.write(i_row, i_col, '[  ]', for_right)
            i_col += 1
            worksheet.merge_range(i_row, i_col, i_row, i_col + 3, req_type.name, for_left)
            i_row += 1
            i_col = 6

        i_row += 1
        i_col = 1
        worksheet.write(i_row, i_col, 'ลำดับที่', for_center_bold_border)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 3, 'รายการ', for_center_bold_border)
        i_col += 4
        worksheet.write(i_row, i_col, 'จำนวน', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ลูกค้า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'เพื่อผลิตสินค้า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'จำนวนเงิน', for_center_bold_border)

        i_num = 0
        for line in picking_id.move_line_ids:
            i_row += 1
            i_num += 1
            i_col = 1
            worksheet.write(i_row, i_col, i_num, for_center_border_int_num_format)
            i_col += 1
            worksheet.merge_range(i_row, i_col, i_row, i_col + 3, line.product_id.name, for_left_border)
            i_col += 4
            worksheet.write(i_row, i_col, line.qty_done, for_right_border_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.move_id.partner_id.name or '', for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, '', for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, '', for_left_border)

        i_row += 1
        i_col = 8
        worksheet.write(i_row, i_col, 'รวม', for_right)
        i_col += 1
        worksheet.write(i_row, i_col, '', for_right_border)
        i_row += 1
        i_col = 8
        worksheet.write(i_row, i_col, 'VAT 7%', for_right)
        i_col += 1
        worksheet.write(i_row, i_col, '', for_right_border)
        i_row += 1

        i_col = 1
        worksheet.write(i_row, i_col, 'ชื่อผู้เบิก', for_right)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, '', for_left_bottom_border)
        i_col = 8
        worksheet.write(i_row, i_col, 'รวมทั้งสิ้น', for_right)
        i_col += 1
        worksheet.write(i_row, i_col, '', for_right_border)

        i_row += 2
        i_col = 1
        worksheet.write(i_row, i_col, 'ผู้อนุมัติ', for_right)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, '', for_left_bottom_border)
        i_col += 2
        worksheet.write(i_row, i_col, 'ผู้จัดสินค้า', for_left)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, '', for_left_bottom_border)
        i_col += 3
        worksheet.write(i_row, i_col, 'ผู้ตรวจสอบ', for_left)
        i_col += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 1, '', for_left_bottom_border)

        workbook.close()
