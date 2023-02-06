# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'KAWA. Print Inventory Report',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Stock',
    'summary': 'Inventory report for Kawainter',
    'description': """
                Inventory Report:
                    - ใบรับสินค้าคืนโกดัง (PDF)
                    - ใบย้ายคลังสินค้า (PDF)
                    - ใบย้ายคลังสินค้า (Excel)
                    """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['stock', 'report_xlsx'],
    'data': [

        'report/return_in_report.xml',
        'report/kawa_internal_tranfer.xml',
        'report/report_reg.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
