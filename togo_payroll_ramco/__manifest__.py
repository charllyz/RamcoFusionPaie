# -*- coding: utf-8 -*-
{
    'name': 'Paie TOGO avec Ordres de Virement',
    'version': '1.3.0',
    'price': 15.99,
    'currency': 'EUR',
    'license': 'AGPL-3',
    'summary': """
       Gestion complète de la paie TOGO avec génération des ordres de virement
    """,
    'category': 'Paie',
    'author': 'Votre Nom',
    'maintainer': 'Votre Nom',
    'company': 'Votre Société',
    'website': 'https://yourdomain.com',
    'depends': ['base', 'hr', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',

        # Rapports
        'reports/fiche_de_paie.xml',
        'reports/fiche_de_paie_conges.xml',  # Nouveau fichier
        'reports/fiche_de_paie_expa.xml',  # Nouveau fichier
        'reports/fiche_de_paie_stagiaire.xml',  # Nouveau fichier
        'reports/ordre_virement_report.xml',
        'reports/report_livre_mensuel.xml',
        'reports/report_livre_annuel.xml',
        'reports/fiche_individuelle_paie_template.xml',

        # Vues
        'views/contract.xml',
        'views/ordre_virement.xml',
        'views/payslip_view.xml',

        # Wizards
        'wizards/payroll_pdf_report.xml',
        'wizards/livre_annuel_pdf.xml',
        'wizards/print_fiche_individuelle_paie.xml',
        'wizards/payroll_report_wiz.xml',

        # Données
        'data/data.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['xlsxwriter'],
    },
}

