# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io
import xlsxwriter
from datetime import datetime

class HrVirement(models.Model):
    _name = 'hr.virement'
    _description = 'Ordre de virement bancaire'

    name = fields.Char(string='Référence')
    date = fields.Date(string='Date')
    payslip_ids = fields.Many2many('hr.payslip')
    check_number = fields.Char(string="Numéro de chèque")
    bank_id = fields.Many2one(
      'res.bank',
      string='Banque',
    )
    x_studio_n_de_compte = fields.Char(string="Numéro de compte")  # Ajout du nouveau champ
    mois_de_paie = fields.Selection([
      ('Janvier','Janvier'),
      ('Février','Février'),
      ('Mars','Mars'),
      ('Avril','Avril'),
      ('Mai','Mai'),
      ('Juin','Juin'),
      ('Juillet','Juillet'),
      ('Août','Août'),
      ('Septembre','Septembre'),
      ('Octobre','Octobre'),
      ('Novembre','Novembre'),
      ('Décembre','Décembre'),
    ])
    annee = fields.Integer(string="Année")
    type_paiement = fields.Selection([
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
        ('espece', 'Espèce')
    ], string='Type de paiement', default='virement')

    excel_file = fields.Binary(string='Fichier Excel', readonly=True)
    excel_filename = fields.Char(string='Nom du fichier Excel', readonly=True)

    @api.onchange('date')
    def _onchange_date(self):
        """Met à jour les champs mois_de_paie et annee en fonction de la date sélectionnée."""
        if not self.date:
            return

        # Mapping des mois en français
        mois_mapping = {
            1: 'Janvier',
            2: 'Février',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Août',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Décembre'
        }

        # Extraire le mois et l'année de la date
        date_obj = self.date
        mois_num = date_obj.month
        annee = date_obj.year

        # Mettre à jour les champs
        self.mois_de_paie = mois_mapping.get(mois_num)
        self.annee = annee

        # Appeler _onchange_type_paiement pour mettre à jour le nom
        self._onchange_type_paiement()

    def generate_xlsx_report_download(self):
        """Génère un fichier Excel pour l'ordre de virement basé sur le format du rapport PDF existant"""
        self.ensure_one()

        if not self.payslip_ids:
            raise UserError(_("Aucune fiche de paie associée à cet ordre de virement."))

        # Créer un fichier Excel en mémoire
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bg_color': '#D3D3D3',
            'border': 1
        })

        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 14,
            'border': 0
        })

        normal_text_format = workbook.add_format({
            'font_size': 12,
            'border': 0
        })

        data_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1
        })

        amount_format = workbook.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'num_format': '# ##0'
        })

        total_format = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1
        })

        total_amount_format = workbook.add_format({
            'bold': True,
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'num_format': '# ##0'
        })

        # Créer une feuille de calcul
        sheet = workbook.add_worksheet('Ordre de Virement')

        # Définir la largeur des colonnes
        sheet.set_column('A:A', 15)  # N° MATR
        sheet.set_column('B:B', 30)  # NOM ET PRENOM
        sheet.set_column('C:C', 40)  # BANQUE ET NUMERO DE COMPTE
        sheet.set_column('D:D', 15)  # NET A PAYER

        # Titre du rapport
        bank_name = self.bank_id.name or ""
        payment_type = dict(self._fields['type_paiement'].selection).get(self.type_paiement, 'Virement')
        title = f"ORDRE DE {payment_type.upper()} - {self.mois_de_paie or ''} {bank_name} {self.annee or ''}"
        sheet.merge_range('A1:D1', title, title_format)

        # Texte d'introduction similaire au rapport PDF
        introduction = f"Messieurs,"
        sheet.merge_range('A3:D3', introduction, normal_text_format)

        if self.type_paiement == 'cheque':
            instruction = f"Par ce présent chèque {self.check_number or ''}, nous vous prions de bien vouloir virer dans les meilleurs délais, les montant ci-dessous(en FCFA) au crédit des comptes ouverts chez vous à {bank_name}"
        else:
            instruction = f"Nous vous prions de bien vouloir virer dans les meilleurs délais, les montant ci-dessous(en FCFA) au crédit des comptes ouverts chez vous à {bank_name}"

        sheet.merge_range('A4:D4', instruction, normal_text_format)

        # En-têtes du tableau - correspondant au format PDF
        row = 6
        headers = ['N° MATR', 'NOM ET PRENOM', 'BANQUE ET NUMERO DE COMPTE', 'NET A PAYER']
        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_format)

        # Données des fiches de paie
        row += 1
        total_amount = 0
        for payslip in self.payslip_ids:
            employee = payslip.employee_id

            # Déterminer le montant net à payer (selon la propriété net_wage utilisée dans le rapport PDF)
            net_amount = payslip.net_wage if hasattr(payslip, 'net_wage') else 0

            # Si net_wage n'est pas disponible, calculer à partir des lignes
            if not net_amount:
                for line in payslip.line_ids:
                    if line.category_id.code == 'NET':
                        net_amount += line.total

            # Matricule
            sheet.write(row, 0, employee.matricule if hasattr(employee, 'matricule') else '', data_format)

            # Nom et prénom
            sheet.write(row, 1, employee.name or '', data_format)

            # Banque et numéro de compte
            bank_account = f"{employee.banque_id.name if hasattr(employee, 'banque_id') else ''}    {employee.account_number or ''}"
            sheet.write(row, 2, bank_account, data_format)

            # Montant
            sheet.write(row, 3, net_amount, amount_format)

            total_amount += net_amount
            row += 1

        # Total
        sheet.write(row, 0, 'Total', total_format)
        sheet.merge_range(f'A{row + 1}:C{row + 1}', 'Total', total_format)
        sheet.write(row, 3, total_amount, total_amount_format)

        # Texte de conclusion - comme dans le rapport PDF
        row += 2
        sheet.merge_range(f'A{row}:D{row}', "Nous vous en remercions à l'avance", normal_text_format)
        row += 1
        sheet.merge_range(f'A{row}:D{row}', "Veuillez agréer Messieurs, nos salutations distinguées",
                          normal_text_format)
        row += 1
        sheet.merge_range(f'A{row}:D{row}', "Pour la Direction Générale", normal_text_format)

        # Signature
        row += 3
        sheet.merge_range(f'C{row}:D{row}', 'Signature et cachet', normal_text_format)

        # Fermer le workbook
        workbook.close()

        # Récupérer le contenu du fichier
        output.seek(0)
        xlsx_data = output.getvalue()

        # Générer le nom du fichier
        filename = f"Ordre_{self.type_paiement}_{self.mois_de_paie or ''}_{self.annee or ''}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # Enregistrer le fichier sur l'enregistrement
        self.write({
            'excel_file': base64.b64encode(xlsx_data),
            'excel_filename': filename
        })

        # Retourner une action pour télécharger le fichier
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/excel_file/{filename}?download=true',
            'target': 'self',
        }

    def export_virements_excel(self):
        """Export le tableau des ordres de virement en Excel exactement comme affiché dans l'interface"""
        if not self:
            raise UserError(_("Aucun ordre de virement sélectionné."))

        # Créer un fichier Excel en mémoire
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 11,
            'bg_color': '#E0E0E0',
            'border': 1
        })

        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 14,
            'border': 0
        })

        data_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1
        })

        date_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'num_format': 'dd/mm/yyyy'
        })

        # Créer une feuille de calcul
        sheet = workbook.add_worksheet('Ordres de Virement')

        # Définir la largeur des colonnes exactement comme dans l'interface
        sheet.set_column('A:A', 15)  # Date
        sheet.set_column('B:B', 15)  # Type de paiement
        sheet.set_column('C:C', 40)  # Description
        sheet.set_column('D:D', 15)  # Mois De Paie
        sheet.set_column('E:E', 10)  # Année
        sheet.set_column('F:F', 20)  # Numéro de chèque
        sheet.set_column('G:G', 25)  # Banque

        # Titre
        sheet.merge_range('A1:G1', 'LISTE DES ORDRES DE VIREMENT', title_format)

        # En-têtes des colonnes exactement comme dans l'interface
        headers = [
            'Date', 'Type de paiement', 'Description', 'Mois De Paie',
            'Année', 'Numéro de chèque', 'Banque'
        ]

        for col, header in enumerate(headers):
            sheet.write(2, col, header, header_format)

        # Données des virements exactement comme affichées dans l'interface
        for row, virement in enumerate(self, 1):
            sheet.write(row + 2, 0, virement.date or '', date_format)  # Date

            # Type de paiement
            type_paiement = dict(self.env['hr.virement']._fields['type_paiement'].selection).get(virement.type_paiement,
                                                                                                 '')
            sheet.write(row + 2, 1, type_paiement, data_format)

            sheet.write(row + 2, 2, virement.name or '', data_format)  # Description
            sheet.write(row + 2, 3, virement.mois_de_paie or '', data_format)  # Mois de paie
            sheet.write(row + 2, 4, virement.annee or '', data_format)  # Année
            sheet.write(row + 2, 5, virement.check_number or '', data_format)  # Numéro de chèque
            sheet.write(row + 2, 6, virement.bank_id.name if virement.bank_id else '', data_format)  # Banque

        # Fermer le workbook
        workbook.close()

        # Récupérer le contenu du fichier
        output.seek(0)
        xlsx_data = output.getvalue()

        # Générer le nom du fichier
        filename = f"Liste_Ordres_Virement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        # Créer une pièce jointe temporaire
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.b64encode(xlsx_data),
            'res_model': 'hr.virement',
            'res_id': self[0].id,
            'type': 'binary',
        })

        # Retourner une action pour télécharger le fichier
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    # Modification de la méthode _onchange_type_paiement existante pour ajouter date aux déclencheurs
    @api.onchange('type_paiement', 'mois_de_paie', 'bank_id', 'annee', 'date')
    def _onchange_type_paiement(self):
        """Met à jour le champ description (name) en fonction du type de paiement sélectionné."""
        if not self.type_paiement:
            return

        # Essayer d'extraire les parties existantes de la description actuelle
        current_description = self.name or ""
        parts = current_description.split()

        # Par défaut, réutiliser les valeurs existantes si disponibles
        mois = self.mois_de_paie or ""
        bank_name = self.bank_id.name if self.bank_id else ""
        annee = str(self.annee) if self.annee else ""

        # Si la description actuelle est au format "SALAIRE MOIS BANQUE ANNEE"
        # ou "ORDRE DE XXXX MOIS BANQUE ANNEE"
        if len(parts) >= 3:
            # Si c'est déjà au format "ORDRE DE XXX", prendre à partir du 4ème mot
            if current_description.startswith("ORDRE DE"):
                if not mois and len(parts) > 2:
                    mois = parts[2]
                if not bank_name and len(parts) > 3:
                    bank_name = parts[3]
                if not annee and len(parts) > 4:
                    annee = parts[4]
            else:
                # Sinon format "SALAIRE MOIS BANQUE ANNEE"
                if not mois and len(parts) > 1:
                    mois = parts[1]
                if not bank_name and len(parts) > 2:
                    bank_name = parts[2]
                if not annee and len(parts) > 3:
                    annee = parts[3]

        # Déterminer le préfixe selon le type de paiement
        prefix = ""
        if self.type_paiement == 'virement':
            prefix = "ORDRE DE VIREMENT"
        elif self.type_paiement == 'cheque':
            prefix = "ORDRE DE PAIEMENT"
        elif self.type_paiement == 'espece':
            prefix = "ORDRE D'ESPÈCE"

        # Construire la nouvelle description
        self.name = f"{prefix} {mois} {bank_name} {annee}"