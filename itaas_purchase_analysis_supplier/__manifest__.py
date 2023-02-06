# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'Itaas Purchase Analysis Supplier',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Purchase',
    'summary': '',
    'description': """
                """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['purchase', 'itaas_analysis_report', 'report_xlsx'],
    'data': [

        'security/ir.model.access.csv',
        'wizard/purchase_supplier.xml',
        'reports/report_reg.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
