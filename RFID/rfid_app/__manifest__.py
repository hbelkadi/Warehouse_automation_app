# -*- coding: utf-8 -*-
{
    'name': "RFID warehouse management app",
    'summary': "Automate warehouse management using UHF RFID technology.",
    'description': """
        This module allows you to manage warehouse operations by automating the 
        input and output of products using UHF RFID readers. The module integrates 
        with Odoo's Inventory, Sales, and Purchase modules to keep stock levels 
        up-to-date based on RFID scans.
    """,
    'author': "hamza belkadi",
    'website': "https://github.com/hbelkadi/Warehouse_automation_app/tree/master",
    'category': 'inventory/rfid',
    'version': '15.0.0.1',
    'depends': [
        'stock',    # Odoo's Inventory module
        'sale',     # Odoo's Sales module
        'purchase', # Odoo's Purchase module
        ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/rfid_tag_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
