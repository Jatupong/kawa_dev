# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022 (www.itaas.co.th)

{
    'name': 'Itaas Hr Employee',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    "category": 'Hr',
    'summary': 'Hr Employee.',
    'description': """
        การสร้างข้อมูลพนักงาน (Employee)
        Tab : Work Information การเพิ่มข้อมูลการทำงาน
        Tab : Private Information การเพิ่มผู้ติดต่อฉุกเฉิน
        Tab : Education การเพิ่มประวัติการศึกษา
        Tab : Experience การเพิ่มประวัติการทำงาน
        Tab : Family การเพิ่มข้อมูลครอบครัว
        Tab : Health การเพิ่มประวัติสุขภาพ
        Tab : Training ประวัติการอบรม
        Tab : การบันทึกบทลงโทษการทำงาน
        Tab : HR Settings การตั้งค่าข้อมูลเกี่ยวกับฝ่ายบุคคล
            """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['hr', 'hr_appraisal'],
    'data': [

        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_training_views.xml',
        # 'views/hr_appraisal_views.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
