# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'KAWA. Print Requisitions Report',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Stock',
    'summary': 'Requisitions report for Kawainter',
    'description': """
                Requisitions Report:
                    - ใบเบิกสินค้าตัวอย่าง (Excel)
                    - ใบเบิกสินค้าตัวอย่าง (PDF)
                    - ใบเบิกตัวอย่างจากคลังใหญ่และคลังตัวอย่าง (Excel)
                    - ใบเบิกตัวอย่างจากคลังใหญ่และคลังตัวอย่าง (PDF)
                    """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['stock', 'material_purchase_requisitions', 'report_xlsx'
                ],
    'data': [

        'report/demo_req_report.xml',
        'report/demo_req_specific.xml',
        'report/report_reg.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
