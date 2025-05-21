from datetime import datetime
from odoo import models, fields, _


class HrVirementListExportXlsx(models.AbstractModel):
    _name = 'report.togo_payroll_ramco.hr_virement_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Export Excel des ordres de virement'

    def generate_xlsx_report(self, workbook, data, virements):
        # Format pour les en-têtes
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bg_color': '#D3D3D3',
            'border': 1
        })

        # Format pour les données
        data_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1
        })

        # Format pour les dates
        date_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'num_format': 'dd/mm/yyyy'
        })

        # Format pour les montants
        amount_format = workbook.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'num_format': '# ##0'
        })

        # Créer une feuille pour la liste des virements
        sheet = workbook.add_worksheet('Ordres de Virement')

        # Définir la largeur des colonnes
        sheet.set_column('A:A', 5)  # No
        sheet.set_column('B:B', 30)  # Référence
        sheet.set_column('C:C', 15)  # Date
        sheet.set_column('D:D', 15)  # Type de paiement
        sheet.set_column('E:E', 15)  # Mois de paie
        sheet.set_column('F:F', 12)  # Année
        sheet.set_column('G:G', 20)  # Numéro de chèque
        sheet.set_column('H:H', 25)  # Banque
        sheet.set_column('I:I', 10)  # Nb fiches
        sheet.set_column('J:J', 15)  # Montant total

        # En-têtes des colonnes
        headers = [
            'No', 'Référence', 'Date', 'Type de paiement',
            'Mois de paie', 'Année', 'Numéro de chèque', 'Banque', 'Nb fiches', 'Montant total'
        ]

        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Données des virements
        for row, virement in enumerate(virements, 1):
            sheet.write(row, 0, row, data_format)  # No
            sheet.write(row, 1, virement.name or '', data_format)  # Référence
            sheet.write(row, 2, virement.date or '', date_format)  # Date

            # Type de paiement
            type_paiement = dict(self.env['hr.virement']._fields['type_paiement'].selection).get(virement.type_paiement,
                                                                                                 '')
            sheet.write(row, 3, type_paiement, data_format)

            sheet.write(row, 4, virement.mois_de_paie or '', data_format)  # Mois de paie
            sheet.write(row, 5, virement.annee or '', data_format)  # Année
            sheet.write(row, 6, virement.check_number or '', data_format)  # Numéro de chèque
            sheet.write(row, 7, virement.bank_id.name if virement.bank_id else '', data_format)  # Banque

            # Nombre de fiches de paie
            sheet.write(row, 8, len(virement.payslip_ids), data_format)

            # Montant total des virements
            total_montant = sum(payslip.net_wage for payslip in virement.payslip_ids)
            sheet.write(row, 9, total_montant, amount_format)