# -*- coding: utf-8 -*-
# Copyright (C) 2021-today ITAAS (Dev K.Yiing)

import datetime
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models, _
from odoo.exceptions import UserError

#
class HrAppraisal(models.Model):
    _inherit = "hr.appraisal"

    training_ids = fields.One2many('hr.appraisal.training', 'hr_appraisal_id', string='Training')

    def action_create_training(self):
        for obj in self:
            for line in obj.training_ids.filtered(lambda x: x.state == 'new'):
                val_training_request = line._prepare_training_request()
                self.env['hr.training.request'].create(val_training_request)
                line.update({'state':'create'})


class HrAppraisalTraining(models.Model):
    _name = 'hr.appraisal.training'
    _description = 'HR Appraisal Training'
    _rec_name = 'hr_appraisal_id'

    hr_appraisal_id = fields.Many2one("hr.appraisal", string='HR Appraisal', required=True, ondelete='cascade')
    course_id = fields.Many2one("course.training", string='Course Training', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([('new', 'New'),
                              ('create', 'Create')], default="new", copy=False, readonly=1)

    def _prepare_training_request(self):
        val = {
            'employee_id': self.hr_appraisal_id.employee_id.id,
            'course_id': self.course_id.id,
            'description': self.description,
            'evaluator_id': self.env.uid,
        }
        return val
