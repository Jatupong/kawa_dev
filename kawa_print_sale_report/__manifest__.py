# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'KAWA. Print Sale Report',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Sale',
    'summary': 'Sale report for Kawainter',
    'description': """
                Sale Report:
                    - Quotation / Order(KAWA)
                    - ใบส่งของชั่วคราว (PDF)
                    """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['sale', 'kawa_sale_extended'],
    'data': [

        'report/sale_order_report.xml',
        'report/delivery_temporary_report.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
