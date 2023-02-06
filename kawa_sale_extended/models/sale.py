# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_attention = fields.Char(string='Attention')
    history_order_date = fields.Date(string='History Order Date')
    lead_time = fields.Date(string='Lead Time')