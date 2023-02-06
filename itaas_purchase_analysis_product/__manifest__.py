# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'Itaas Purchase Analysis Product',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Purchase',
    'summary': '',
    'description': """
                """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['purchase', 'purchase_discount', 'itaas_analysis_report', 'report_xlsx'],
    'data': [

        'security/ir.model.access.csv',
        'wizard/purchase_product.xml',
        'reports/report_reg.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
