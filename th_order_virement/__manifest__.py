{
    'name': 'Ordre de virement bancaire',
    'version': '1.0',
    'description': 'Ordre de virement bancaire',
    'summary': 'Ordre de virment bancaire',
    'author': 'Thomas ATCHA',
    'website': 'https://erptogo.net',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': [
        'base','hr','hr_payroll',
    ],
    'data': [
        'views/ordre_virement_view.xml',
        'reports/ordre_virement_report.xml', 
        'reports/ordre_virement_report_2.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'application': False,
}
