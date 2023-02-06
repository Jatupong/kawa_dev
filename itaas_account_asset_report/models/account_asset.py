# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from bahttext import bahttext
from num2words import num2words
import locale


class account_asset(models.Model):
    _inherit = 'account.asset'

    disposal_type = fields.Selection([('sell','Sell'),('dispose','Write Off')],string='Disposal Type')






