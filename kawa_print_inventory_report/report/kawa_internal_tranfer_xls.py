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


class KawaInternalTranferxls(models.AbstractModel):
    _name = 'report.kawa_print_inventory_report.kawa_internal_tranfer_xls'
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
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 20)

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
        worksheet.insert_image(0, 4, "image.png", {'image_data': company_image, 'x_scale': 0.4, 'y_scale': 0.4})

        i_row = 6
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row, i_col + 8, 'ใบย้ายคลังสินค้า', for_center_bold_underline)

        i_row += 3
        i_col = 0
        worksheet.write(i_row, i_col, 'ลำดับที่', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ชื่อสินค้า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'Lot', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'น้ำหนัก', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'มูลค่า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'คลังต้นทาง', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'คลังปลายทาง', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'สาเหตุ/ผู้ปฎิบัติงาน', for_center_bold_border)

        if picking_id.move_line_nosuggest_ids:
            move_line = picking_id.move_line_nosuggest_ids
        else:
            move_line = picking_id.move_line_ids

        i_num = 0
        for line in move_line:
            i_row += 1
            i_num += 1
            i_col = 0
            worksheet.write(i_row, i_col, i_num, for_center_border_int_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.product_id.display_name, for_left_border)
            i_col += 1
            if line.lot_id:
                worksheet.write(i_row, i_col, line.lot_id.name, for_left_border)
            else:
                worksheet.write(i_row, i_col, line.lot_name or '', for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, line.qty_done, for_right_border_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, '', for_right_border_num_format)
            i_col += 1
            worksheet.write(i_row, i_col, line.location_id.display_name, for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, line.location_dest_id.display_name, for_left_border)
            i_col += 1
            worksheet.write(i_row, i_col, '', for_left_border)

        attachment_ids = picking_id.env['ir.attachment'].sudo().search([('res_model', '=', 'stock.picking'),
                                                                        ('res_id', '=', picking_id.id),
                                                                        ('type', '=', 'binary'),
                                                                        ('mimetype', '=', 'image/png')])

        if attachment_ids:

            i_row += 2
            i_col = 0
            worksheet.merge_range(i_row, i_col, i_row, i_col + 8, 'รูปสินค้าชำรุด', for_center_bold)
            i_row += 2
            for image in attachment_ids:
                # image_width = 300.0
                # image_height = 300.0
                #
                # cell_width = 300.0
                # cell_height = 300.0
                #
                # x_scale = cell_width / image_width
                # y_scale = cell_height / image_height

                product_image = io.BytesIO(base64.b64decode(image.datas))
                worksheet.insert_image(i_row, 0, "image.png", {'image_data': product_image,
                                                               'x_scale': 0.3,
                                                               'y_scale': 0.3})
                i_row += 15

        workbook.close()
