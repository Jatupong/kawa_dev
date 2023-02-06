# -*- coding: utf-8 -*-
# Part of IT as a Service Co., Ltd.
# Copyright (C) 2022-today www.itaas.co.th (Dev K.Book)

{
    'name': 'Itaas Customers Credit Limit',
    'version': '16.0.0.1',
    'price': 'Free',
    'currency': 'THB',
    'category': 'Menu',
    'summary': '',
    'description': """
                """,
    'author': 'IT as a Service Co., Ltd.',
    'website': 'www.itaas.co.th',
    'depends': ['sale', 'account'],
    'data': [

        'security/ir.model.access.csv',
        'security/security_group.xml',
        'data/mail_template_data.xml',
        'views/sale_view.xml',
        'wizards/warning_override_credit_view.xml',

    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
