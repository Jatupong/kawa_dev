# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

import datetime
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import fields, api, models, _
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    emp_code = fields.Char(string='รหัสพนักงาน')
    title = fields.Char(string='คำนำหน้า')
    first_name = fields.Char(string="ชื่อ")
    last_name = fields.Char(string="นามสกุล")
    nick_name = fields.Char(string='ชื่อเล่น')
    eng_firstname = fields.Char(string='ชื่อภาษาอังกฤษ')
    eng_lastname = fields.Char(string='นามสกุลภาษาอังกฤษ')
    eng_nick_name = fields.Char(string='ชื่อเล่นภาษาอังกฤษ')
    home_address = fields.Text(string='ที่อยู่')

    # Page Personal Information
    residence = fields.Selection([('living_with_parent', 'Living with parent'),
                                  ('own_home', 'Own home'),
                                  ('rented_house', 'Rented house'),
                                  ('domitory', 'Domitory')], string='Residence')
    # SSO
    sso_id = fields.Char(string='เลขที่ประกันสังคม')
    sso_hospital = fields.Char(string='โรงพยาบาลประกันสังคม')
    # Bank
    bank_name = fields.Char(string='ชื่อธนาคาร')
    bank_branch = fields.Char(string='สาขาธนาคาร')
    bank_number = fields.Char(string='หมายเลขบัญชี')
    bank_detail = fields.Char(string='หมายเหตุบัญชีธนาคาร')
    # Citizenship
    race = fields.Char('Yrs. Race')
    religion = fields.Char('Religion')
    ident_exp_date = fields.Date(string='Identity Expiry Date')
    ident_issued_date = fields.Date(string='Identity Issued Date')
    age = fields.Integer('Age')
    military_status = fields.Selection([('exempted', 'Exempted'),
                                        ('served', 'Served'),
                                        ('not_yet_served', 'Not yet served'),
                                        ('discharged', 'Discharged')], string='Military Status')

    # Page Emergency Contact
    ec_name = fields.Char('Name')
    ec_relationship = fields.Char('Relationship')
    ec_tel1 = fields.Char('Primary Phone No.')
    ec_tel2 = fields.Char('Secondary Phone No.')
    ec_woreda = fields.Char('Subcity/Woreda')
    ec_kebele = fields.Char('Kebele')
    ec_houseno = fields.Char('House No.')
    ec_address = fields.Char('Address')
    ec_country_id = fields.Many2one('res.country', 'Country', )
    ec_state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id','=',ec_country_id)]", )
    ec_line_id = fields.Char(string="Line ID")

    # Page Education
    education_ids = fields.One2many('hr.employee.education', 'employee_id', "Education")

    # Page Experience
    experience_ids = fields.One2many('hr.employee.experience', 'employee_id', "Experience")

    # Page Family
    # Spouse
    fam_telephone = fields.Char("Telephone")
    fam_spouse = fields.Char("Spouse's Name")
    fam_spouse_working_place = fields.Char("Spouse's Working Place")
    fam_spouse_job = fields.Char("Spouse's Occupation")
    # Father
    fam_father = fields.Char("Father's Name")
    fam_father_date_of_birth = fields.Date("Father's Date of Birth")
    fam_father_age = fields.Integer("Father's Age")
    fam_father_status = fields.Char("Father's Status")
    fam_father_job = fields.Char("Father's Occupation")
    # Mother
    fam_mother = fields.Char("Mother's Name")
    fam_mother_date_of_birth = fields.Date("Mother's Date of Birth")
    fam_mother_age = fields.Integer("Mother's Age")
    fam_mother_status = fields.Char("Mother's Status")
    fam_mother_job = fields.Char("Mother's Occupation")
    number_of_member = fields.Integer('Number of Members in the family')
    number_of_male_member = fields.Integer('Male')
    number_of_female_member = fields.Integer('Female')
    ordinal_of_member = fields.Integer('Ordinal of member', helps='Ordinal position of each child in the family')
    # Children
    fam_children_ids = fields.One2many('hr.employee.children', 'employee_id', "Children")

    # Page Health
    blood_group = fields.Selection([('a', 'Group A'),
                                    ('b', 'Group B'),
                                    ('o', 'Group O'),
                                    ('ab', 'Group AB')], string='Blood')
    weight = fields.Float("Weight")
    high = fields.Float("High")
    fam_health_ids = fields.One2many('hr.employee.health', 'employee_id', "Health")

    # Page Training
    fam_training_ids = fields.One2many('hr.employee.training', 'employee_id', "Training")

    # Page Language Ability
    ability_language_ids = fields.One2many('hr.employee.language', 'employee_id', "Language Ability")

    # Page Special Ability
    ability_typing = fields.Boolean('Typing')
    ability_typing_note = fields.Text('Typing Note')
    ability_computer = fields.Boolean('Computer')
    ability_computer_note = fields.Text('Computer Note')
    ability_driving = fields.Boolean('Driving')
    ability_driving_license = fields.Char('Driving License No.')
    ability_office_machine = fields.Char('Office Machine')
    ability_hobbies = fields.Char('Hobbies')
    ability_favorites = fields.Char('Favorites')
    ability_knowledge = fields.Char('Special knowledge')
    ability_others = fields.Char('Others')

    # Page behavior
    behavior_ids = fields.One2many('hr.employee.behavior', 'employee_id', "Behavior")

    _sql_constraints = [
        ('uniq_name_id', 'unique(identification_id)', "ID can't duplicate"),
        ('uniq_name_passport_id', 'unique(passport_id)', "Passport can't duplicate"),
        ('uniq_name_sso_id', 'unique(sso_id)', "SSO ID can't duplicate"),
        ('uniq_employee_code', 'unique(employee_code)', "Employee Code ID can't duplicate"),
    ]