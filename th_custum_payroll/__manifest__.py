# -*- coding: utf-8 -*-
{
    'name': 'Paie TOGO',
    'version': '1.2.0',
    'price': 15.99,
    'currency': 'EUR',
    'license': 'AGPL-3',
    'summary': """
       Ajout des champs de rubriques de paie
    """,
    'category': 'Paie',
    'author': 'Thomas ATCHA',
    'maintainer': 'Thomas ATCHA',
    'company': 'Thomas ATCHA',
    'website': 'https://digitaltg.net',
    'depends': ['base', 'hr', 'hr_payroll', 'th_order_virement'],
    'data': [
        'security/ir.model.access.csv',        
        'data/data.xml',
        'reports/fiche_de_paie.xml',
        'reports/fiche_de_paie_conges.xml',  # Nouveau fichier
        'reports/fiche_de_paie_expa.xml',    # Nouveau fichier
        'reports/fiche_de_paie_stagiaire.xml',  # Nouveau fichier
        'views/contract.xml',
        'views/ordre_virement.xml',  # Ajout du nouveau fichier de vues

        # 'views/employee_fields_view.xml',
        'reports/report_livre_mensuel.xml',
        'reports/report_livre_annuel.xml',
        'reports/ordre_de_virement.xml',
        'reports/fiche_individuelle_paie_template.xml',
        'wizards/payroll_pdf_report.xml',
        'wizards/livre_annuel_pdf.xml',
        'wizards/print_fiche_individuelle_paie.xml',
        # 'wizards/dnr_wizard_view.xml',
        'wizards/payroll_report_wiz.xml',
        # 'views/periode_view.xml',
        'views/payslip_view.xml',  # Fichier pour les boutons
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['xlsxwriter'],
    },
}
