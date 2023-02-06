# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)


from odoo import api, models, fields, _
from datetime import datetime, timedelta, date, time
from odoo.exceptions import UserError
import pytz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta


class WizardPurchaseSupplierReport(models.TransientModel):
    _name = 'wizard.purchase.supplier.report'

    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    partner_ids = fields.Many2many('res.partner', string='Partners')
    categ_ids = fields.Many2many('product.category', string='Categorys')
    product_ids = fields.Many2many('product.product', string='Products')

    @api.model
    def default_get(self, fields_list):
        result = super(WizardPurchaseSupplierReport, self).default_get(fields_list)
        curr_date = datetime.now()
        curr_month = curr_date.month
        from_date = datetime(curr_date.year, 1, 1).date() or False
        to_date = datetime(curr_date.year, curr_month, curr_date.day).date() or False
        result.update({'date_from': str(from_date),
                       'date_to': str(to_date),
                       })

        return result

    @api.onchange('categ_ids')
    def onchange_categ_ids(self):
        if self.categ_ids:
            return {'domain': {'product_ids': [('categ_id', 'child_of', self.categ_ids.ids)]}}
        else:
            return {'domain': {'product_ids': []}}

    def _get_product_from(self, categ):
        domain_product = [('type', '=', 'product')]
        if categ:
            domain_product += [('categ_id', 'child_of', categ.ids)]
        product_ids = self.env['product.product'].search(domain_product)

        return product_ids

    def print_excel_report(self):
        [data] = self.read()
        datas = {'form': data}

        product_ids = self._get_product_from(self.categ_ids)
        if not product_ids:
            raise UserError(_('Document is empty.'))
        print('product_ids ', product_ids)
        datas['product_ids'] = product_ids.ids
        if self.partner_ids:
            datas['partner_ids'] = self.partner_ids.ids
        else:
            datas['partner_ids'] = False
        print('datas ', datas)
        return self.env.ref('itaas_purchase_analysis_supplier.purchase_supplier_xls').report_action(self, data=datas)


class PurchaseSupplierReportXls(models.AbstractModel):
    _name = 'report.itaas_purchase_analysis_supplier.purchase_supplier_xls'
    _inherit = 'report.report_xlsx.abstract'

    def _get_stock_move(self, date_from, date_to, product_ids, partner_ids, company_id):
        str2d = fields.Date.from_string
        date_from = str2d(date_from)
        date_to = str2d(date_to)
        domain_move = [('date', '>=', date_from),
                       ('date', '<=', date_to),
                       ('company_id', '=', company_id.id),
                       ('product_id', 'in', product_ids),
                       ('state', 'in', ['done']),
                       ('purchase_line_id', '!=', False)]
        if partner_ids:
            domain_move += [('purchase_line_id.order_id.partner_id', 'in', partner_ids)]
        print('domain_move ', domain_move)
        move_ids = self.env['stock.move'].search(domain_move)

        return move_ids

    def generate_xlsx_report(self, workbook, data, lines):
        print('def generate_xlsx_report lines: ', lines)
        print('def generate_xlsx_report data: ', data)

        product_ids = data['product_ids']
        print('product_ids ', product_ids)
        move_ids = self._get_stock_move(lines.date_from, lines.date_to, product_ids, data['partner_ids'], lines.company_id)
        print('move_ids ', move_ids)
        partner_ids = move_ids.mapped('picking_id').mapped('purchase_id').mapped('partner_id')
        print('partner_ids ', partner_ids)

        # left
        for_left = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'valign': 'top'})
        for_left_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'border': True})
        for_left_bold = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'valign': 'top', 'align': 'left', 'bold': True})
        for_left_bold_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'bold': True, 'border': True})
        for_left_date = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'left', 'num_format': 'dd/mm/yyyy'})
        for_left_bottom_border = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'left'})
        for_left_bottom_border.set_bottom()

        # right
        for_right = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'right'})
        for_right_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'num_format': '#,##0.00'})
        for_right_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True})
        for_right_bold = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'valign': 'top', 'align': 'right', 'bold': True})
        for_right_bold_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'bold': True})
        for_right_border_int_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'num_format': '#,##0'})
        for_right_border_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'right', 'border': True, 'bold': True,
             'num_format': '#,##0.00'})

        # center
        for_center = workbook.add_format({'font_name': 'Angsana New', 'font_size': 14, 'align': 'center'})
        for_center_date = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center','num_format': 'dd/mm/yyyy'})
        for_center_bold = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'bold': True})
        for_center_bold_underline = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'bold': True, 'underline': True, })
        for_center_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True})
        for_center_bold_border = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'valign': 'vcenter', 'align': 'center', 'bold': True,
             'border': True})
        for_center_border_int_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': '#,##0'})
        for_center_border_num_format = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True, 'num_format': '#,##0.00'})
        for_center_border_date = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True,
             'num_format': 'dd/mm/yyyy'})
        for_center_datetime = workbook.add_format(
            {'font_name': 'Angsana New', 'font_size': 14, 'align': 'center', 'border': True,
             'num_format': 'dd/mm/yyyy HH:MM'})

        worksheet = workbook.add_worksheet('Page 1')
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 10)
        worksheet.set_column('K:K', 10)
        worksheet.set_column('L:L', 10)
        worksheet.set_column('M:M', 10)

        def convert_utc_to_usertz(date_time):
            if not date_time:
                return ''
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            tz = pytz.timezone('UTC')
            date_time = tz.localize(fields.Datetime.from_string(date_time)).astimezone(user_tz)
            date_time = date_time.strftime('%d/%m/%Y %H:%M')

            return date_time

        i_row = 0
        i_row += 1
        i_col = 0
        worksheet.merge_range(i_row, i_col, i_row, i_col + 12, lines.company_id.name, for_left)
        i_row += 1
        worksheet.merge_range(i_row, i_col, i_row, i_col + 12, 'รายงานประวัติการซื้อ แยกตามผู้จำหน่าย', for_left)
        i_row += 1
        worksheet.write(i_row, i_col, 'วันที่จาก', for_left)
        i_col += 1
        worksheet.write(i_row, i_col, lines.date_from, for_left_date)
        i_col += 3
        worksheet.write(i_row, i_col, 'ถึง', for_left)
        i_col += 1
        worksheet.write(i_row, i_col, lines.date_to, for_left_date)

        i_row += 3
        i_col = 0
        worksheet.write(i_row, i_col, 'ผู้จำหน่าย', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'สินค้า', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'วันที่', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'เลขที่เอกสาร', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'จำนวน', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'คืน', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ราคาต่อหน่วย', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'VAT', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ส่วนลด', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'รวมเงิน', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ส่วนลดรวม', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'ยอดซื้อสุทธิ', for_center_bold_border)
        i_col += 1
        worksheet.write(i_row, i_col, 'อ้างถึง', for_center_bold_border)

        for partner in partner_ids:
            move_by_partner = move_ids.filtered(lambda x:x.picking_id.partner_id.id == partner.id)
            product_ids = move_by_partner.mapped('product_id')
            print('product_ids', product_ids)
            i_row += 1
            i_col = 0
            worksheet.merge_range(i_row, i_col, i_row, i_col + 12, partner.name, for_left)
            sum_partner_qty = 0.0
            sum_partner_subtotal = 0.0
            sum_partner_net_amount = 0.0
            for product in product_ids:
                move_by_partner_product = move_by_partner.filtered(lambda x:x.product_id.id == product.id)
                i_row += 1
                i_col = 1
                worksheet.merge_range(i_row, i_col, i_row, i_col + 11, product.name, for_left)
                sum_product_qty = 0.0
                sum_product_subtotal = 0.0
                sum_product_net_amount = 0.0
                for line in move_by_partner_product:
                    i_row += 1
                    i_col = 2
                    worksheet.write(i_row, i_col, line.date, for_center_date)
                    i_col += 1
                    worksheet.write(i_row, i_col, line.picking_id.name, for_left)
                    i_col += 1
                    if not line.origin_returned_move_id:
                        sum_product_qty += line.quantity_done
                        worksheet.write(i_row, i_col, line.quantity_done, for_right_num_format)
                        i_col += 1
                        worksheet.write(i_row, i_col, '', for_left)
                    else:
                        sum_product_qty -= line.quantity_done
                        worksheet.write(i_row, i_col, '', for_left)
                        i_col += 1
                        worksheet.write(i_row, i_col, line.quantity_done, for_right_num_format)
                    i_col += 1
                    worksheet.write(i_row, i_col, line.purchase_line_id.price_unit, for_right_num_format)
                    i_col += 1
                    # VAT
                    if line.purchase_line_id.taxes_id:
                        worksheet.write(i_row, i_col, ', '.join(line.purchase_line_id.taxes_id.mapped('name')), for_left)
                    else:
                        worksheet.write(i_row, i_col, '', for_left)
                    i_col += 1
                    discount = line.purchase_line_id.discount
                    if discount:
                        worksheet.write(i_row, i_col, str(discount) + '%', for_right)
                    else:
                        worksheet.write(i_row, i_col, '', for_right)
                    i_col += 1
                    worksheet.write(i_row, i_col, line.purchase_line_id.price_subtotal, for_right_num_format)
                    i_col += 1
                    discount_bill = 0.0
                    worksheet.write(i_row, i_col, discount_bill, for_right_num_format)
                    i_col += 1
                    net_amount = line.purchase_line_id.price_subtotal - discount_bill
                    sum_product_net_amount += net_amount
                    worksheet.write(i_row, i_col, net_amount, for_right_num_format)
                    i_col += 1
                    worksheet.write(i_row, i_col, line.purchase_line_id.order_id.name, for_left)

                # summary product
                i_row += 1
                i_col = 2
                worksheet.merge_range(i_row, i_col, i_row, i_col + 1, 'รวมตามซื้อเชื่อ', for_left)
                i_col += 2
                sum_partner_qty += sum_product_qty
                worksheet.write(i_row, i_col, sum_product_qty, for_right_num_format)
                i_col += 5
                sum_partner_subtotal += sum_product_subtotal
                worksheet.write(i_row, i_col, sum_product_subtotal, for_right_num_format)
                i_col += 2
                sum_partner_net_amount += sum_product_net_amount
                worksheet.write(i_row, i_col, sum_product_net_amount, for_right_num_format)

            # summary partner
            i_row += 1
            i_col = 1
            worksheet.merge_range(i_row, i_col, i_row, i_col + 2, 'รวม', for_left)
            i_col += 3
            worksheet.write(i_row, i_col, sum_partner_qty, for_right_num_format)
            i_col += 5
            worksheet.write(i_row, i_col, sum_partner_subtotal, for_right_num_format)
            i_col += 2
            worksheet.write(i_row, i_col, sum_partner_net_amount, for_right_num_format)

        workbook.close()
