# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'Itaas Hr Contract',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Hr',
    'summary': 'Hr Employee.',
    "description": """
        การสร้างข้อมูลสัญญาพนักงาน (Contract)
        Tab : Personal Tax
        Tab : Payroll Record
        Tab : Social Security
        Tab : Employee Tax Deduction
    """,
    "sequence": 1,
    "author": "IT as a Service Co., Ltd.",
    "website": "http://www.itaas.co.th/",
    "version": '13.0.1.0',
    "depends": ['hr', 'hr_payroll'],
    "data": [

        'security/ir.model.access.csv',
        'views/employee_tax_deduction_view.xml',
        'views/personal_income_tax_view.xml',
        'views/social_security_view.xml',
        'views/hr_payslip_view.xml',
        'views/hr_salary_rule_view.xml',
        'views/hr_contract_view.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}