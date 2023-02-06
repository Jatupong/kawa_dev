# -*- coding: utf-8 -*-

# Part of ITAAS (www.itaas.co.th)
{
    'name' : 'Itaas Account Asset Report',
    'version' : '16.0.0.1',
    'price' : 'Free',
    'currency': 'THB',
    'category': 'Account Asset',
    'summary' : 'HTC Account Asset Report',
    'description': """
                Account Asset Report:
                    - Creating Account Asset Report
Tags: 
Stock report
            """,
    'author' : 'IT as a Service Co., Ltd.',
    'website' : 'www.itaas.co.th',
    'depends' : ['base', 'account', 'account_asset','analytic'],
    'data' : [
        # report
        # 'report/report_reg.xml',
        # 'views/account_asset.xml',

        # wizard
        'security/ir.model.access.csv',
        'wizard/write_off_and_sale_view.xml',
        'views/account_account.xml',




    ],


    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
