# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'KAWA. Print Invoice Report',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Stock',
    'summary': 'Inventory report for Kawainter',
    'description': """
                Invoice Report:
                    - invoice Report
                    """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['base', 'account'],
    'data': [
        'report/invoice_report.xml',
        'report/report_reg.xml',


    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
