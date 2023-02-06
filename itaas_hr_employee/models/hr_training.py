# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class HrTrainingRequest(models.Model):
    _name = 'hr.training.request'
    _description = 'HR Training Request'
    _rec_name = 'course_id'

    employee_id = fields.Many2one('hr.employee', "Employee", required=True)
    course_id = fields.Many2one("course.training", string='Course Training', required=True)
    price = fields.Float("Price", digits=(16, 2))
    hr_approve_id = fields.Many2one("res.users", "Hr Approve")
    description = fields.Text(string='Description')
    evaluator_id = fields.Many2one("res.users", "Evaluator")
    state = fields.Selection([('new','New'),
                              ('submit','Submit'),
                              ('department_approve','Department Approve'),
                              ('hr_approve','Hr Approve'),
                              ('done','CEO Approve'),
                              ('reject','Reject')], default="new", required=True, copy=False)
    training_record_id = fields.Many2one('hr.training.record', string='Training Record')

    @api.onchange('course_id')
    def onchange_course_id(self):
        if not self.course_id:
            return

        self.description = self.course_id.description

    def action_submit(self):
        for obj in self:
            obj.update({'state': 'submit'})

    def action_department_approve(self):
        for obj in self:
            if not obj.employee_id.department_id:
                raise UserError(_('Please, assign department to employee'))
            departments = self.env['hr.department'].search([('manager_id', '=', self.env.user.employee_id.id)])
            if not departments and obj.employee_id.department_id and obj.employee_id.department_id.id not in departments.ids:
                raise UserError(
                    _('You are not authorized to approve this department (%s).') % (obj.employee_id.department_id.name))

            obj.update({'state': 'department_approve'})

    def action_hr_approve(self):
        for obj in self:
            course = self.env['hr.course.schedule'].search([('state','=', 'open'),
                                                            ('course_id','=', self.course_id.id),
                                                            ('remain','>=', 1)
                                                            ], limit=1)
            if not course:
                raise UserError(_("The course is not available to training."))

            val_training_record = obj._prepare_training_record()
            # print('val_training_record: ',val_training_record)
            val_training_record.update({'course_schedule_id': course.id})
            self.env['hr.training.record'].create(val_training_record)

            obj.update({'state': 'hr_approve',
                        'hr_approve_id': self.env.uid})

    def action_done(self):
        for obj in self:
            obj.update({'state': 'done'})

    def action_reject(self):
        for obj in self:
            obj.update({'state': 'reject'})

    def action_set_to_draft(self):
        for obj in self:
            obj.update({'state': 'new'})

    def _prepare_training_record(self):
        val = {
            'employee_id': self.employee_id.id,
            'course_id': self.course_id.id,
            'evaluator_id': self.evaluator_id.id,
            'description': self.description,
        }
        return val


class HrCourseSchedule(models.Model):
    _name = 'hr.course.schedule'
    _description = 'HR Course Schedule'
    _rec_name = 'course_id'

    course_id = fields.Many2one("course.training", string='Course Training', required=True)
    datetime_form = fields.Datetime('Date Form')
    datetime_to = fields.Datetime('Date to')
    duration_days = fields.Integer('Duration Days', compute='_compute_duration_days', store=True)
    capacity = fields.Integer('Capacity')
    remain = fields.Integer('Remaining', compute='_compute_remain')
    location = fields.Char("Institution")
    state = fields.Selection([('new', 'New'),
                              ('open', 'Open'),
                              ('close', 'Close')], default="new", required=True, copy=False)
    description = fields.Text(string='Description')

    @api.onchange('course_id')
    def onchange_course_id(self):
        if not self.course_id:
            return

        self.description = self.course_id.description

    @api.depends('datetime_form', 'datetime_to')
    def _compute_duration_days(self):
        for obj in self:
            duration_days = 0
            if obj.datetime_to and obj.datetime_form:
                duration_days = (obj.datetime_to - obj.datetime_form).days + 1
            obj.duration_days = duration_days

    @api.depends('capacity')
    def _compute_remain(self):
        for obj in self:
            request_count = self.env['hr.training.record'].search_count([('course_schedule_id','=',obj.id)])
            obj.remain = obj.capacity - request_count

    def action_open(self):
        for obj in self:
            obj.update({'state': 'open'})

    def action_close(self):
        for obj in self:
            obj.update({'state': 'close'})

    def action_set_to_draft(self):
        for obj in self:
            obj.update({'state': 'new'})


class HrTrainingRecord(models.Model):
    _name = 'hr.training.record'
    _description = 'HR Training Record'
    _rec_name = 'course_id'

    employee_id = fields.Many2one('hr.employee', "Employee", required=True)
    course_id = fields.Many2one("course.training", string='Course Training', required=True)
    course_schedule_id = fields.Many2one("hr.course.schedule", "Course Schedule")
    datetime_form = fields.Datetime('Date Form', related='course_schedule_id.datetime_form', stored=True)
    datetime_to = fields.Datetime('Date to', related='course_schedule_id.datetime_to', stored=True)
    evaluator_id = fields.Many2one("res.users", "Evaluator")
    description = fields.Text(string='Description')
    state = fields.Selection([('new','New Request'),
                              ('progress','In Progress'),
                              ('done','Done'),
                              ('reject','Reject'),
                              ('cancel','Cancel')], default="new", required=True, copy=False)

    def action_progress(self):
        for obj in self:
            obj.update({'state': 'progress'})

    def action_validate(self):
        for obj in self:
            if obj.evaluator_id.id != obj.env.uid:
                raise UserError(_('You are not authorized to validate'))
            val_training = obj._prepare_employee_training()
            self.env['hr.employee.training'].create(val_training)

            obj.update({'state': 'done'})

    def action_reject(self):
        for obj in self:
            obj.update({'state': 'reject'})

    def action_cancel(self):
        for obj in self:
            obj.update({'state': 'cancel'})

    def action_to_new(self):
        for obj in self:
            obj.update({'state': 'new'})

    def _prepare_employee_training(self):
        val = {
            'employee_id': self.employee_id.id,
            'date_form': self.datetime_form,
            'date_to': self.datetime_to,
            'name': self.course_id.id,
            'certificate_id': self.course_id.certificate_id.id,
            'exp_certificate_date': self.course_id.exp_certificate_date,
            'note': self.course_id.description,
            'location': self.course_schedule_id.location,
            'training_record_id': self.id,
        }
        return val


class HrTraining(models.Model):
    _name = 'hr.employee.training'
    _description = 'HR Employee Training'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade', required=True)
    date_form = fields.Datetime('Date Form')
    date_to = fields.Datetime('Date to')
    name = fields.Many2one('course.training', string='Course Training', required=True)
    note = fields.Char("Course Description")
    certificate_id = fields.Many2one('hr.certificate', string='Certificate No.')
    exp_certificate_date = fields.Date('Exp.Certificate')
    cost = fields.Float(string='Cost')
    location = fields.Char("Institution")
    date = fields.Date("Date")
    type = fields.Selection([('planned', 'Planned Training'),
                             ('new', 'New Request'),
                             ('others', 'Others')])
    training_record_id = fields.Many2one('hr.training.record', string='Training Record')
    evaluation = fields.Selection([('pass', 'ผ่าน'),
                                   ('not_pass', 'ไม่ผ่าน')], string='ประเมินผลการอบรมย้อนหลัง1เดือน')
    evaluation_date = fields.Date(string='Evaluation Date')

    def write(self, vals):
        if 'evaluation' in vals:
            if self.training_record_id and self.training_record_id.evaluator_id.id != self.env.uid:
                raise UserError(_('You are not authorized to evaluate'))
            vals['evaluation_date'] = fields.Datetime.now()

        return super(HrTraining, self).write(vals)


class CourseTraining(models.Model):
    _name = "course.training"
    _description = "Course Training"

    name = fields.Char("Course", required=True)
    code = fields.Char("Code")
    price = fields.Float("Price", digits=(16,2))
    certificate_id = fields.Many2one('hr.certificate', string='Certificate No.')
    exp_certificate_date = fields.Date('Exp.Certificate')
    description = fields.Text(string='Description')

    @api.onchange('certificate_id')
    def onchange_certificate_id(self):
        if not self.certificate_id:
            return

        self.exp_certificate_date = self.certificate_id.exp_certificate_date


class HrCertificate(models.Model):
    _name = "hr.certificate"
    _description = "Hr Certificate"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string='Description')
    exp_certificate_date = fields.Date('Exp.Certificate')