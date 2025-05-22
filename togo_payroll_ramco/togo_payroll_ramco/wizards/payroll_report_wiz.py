# -*- coding: utf-8 -*-

import base64
import os
from datetime import datetime
from io import BytesIO

import xlsxwriter
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from xlsxwriter.utility import xl_rowcol_to_cell
import logging

_logger = logging.getLogger(__name__)


class PayrollReportExcelWiz(models.TransientModel):
    _name = 'payroll.report.wiz'
    _description = "Assistant d'exportation de la paie en Excel"

    from_date = fields.Date('Date début', required=True)
    company = fields.Many2one('res.company', default=lambda self: self.env.user.company_id,
                              string="Société")
    structure_id = fields.Many2one('hr.payroll.structure', string="Structure de paie")

    def get_rules(self):
        vals = []
        selected_structure = self.structure_id
        heads = self.env['hr.salary.rule'].search(
            [('struct_id', '=', selected_structure.id), ('active', 'in', (True, False))], order='sequence asc')
        list_rules = []
        for head in heads:
            list_rules = [head.name, head.code]
            vals.append(list_rules)

        return vals

    def get_item_data(self):
        _logger.debug('Begin data get_item_data')
        file_name = _('payroll report.xlsx')
        fp = BytesIO()

        workbook = xlsxwriter.Workbook(fp)
        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True, 'size': 14})
        cell_text_format_n = workbook.add_format({'align': 'center',
                                                  'bold': True, 'size': 9,
                                                  })
        cell_text_format = workbook.add_format({'align': 'left',
                                                'bold': True, 'size': 9,
                                                })

        cell_text_format.set_border()
        cell_text_format_new = workbook.add_format({'align': 'left',
                                                    'size': 9,
                                                    })
        cell_text_format_new.set_border()
        cell_number_format = workbook.add_format({'align': 'right',
                                                  'bold': False, 'size': 9,
                                                  'num_format': '#,###0.00'})
        cell_number_format.set_border()
        cell_date_format = workbook.add_format({'align': 'center',
                                                'bold': False, 'size': 9,
                                                'num_format': 'dd/mm/yyyy'})
        cell_date_format.set_border()
        worksheet = workbook.add_worksheet('payroll report.xlsx')
        normal_num_bold = workbook.add_format(
            {'bold': True, 'num_format': '#,###0.00', 'size': 9, })
        normal_num_bold.set_border()
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        _logger.debug('middle data get_item_data')

        if self.from_date:
            date_1 = datetime.strftime(self.from_date, '%d-%m-%Y')
            payroll_month = self.from_date.strftime("%B")
            worksheet.merge_range('A1:F2', 'Paie du mois de %s %s' % (
                payroll_month, self.from_date.year), heading_format)
            worksheet.merge_range('B4:D4', '%s' % (
                self.company.name), cell_text_format_n)
            row = 2
            column = 0
            worksheet.write(row + 1, 0, 'Société', cell_text_format_n)
            row += 2
            worksheet.write(row, 4, '', cell_text_format_n)
            worksheet.write(row, 5, '' or '')
            row += 2
            res = self.get_rules()

            worksheet.write(row, 0, 'Employé', cell_text_format)
            worksheet.write(row, 1, 'Matricule', cell_text_format)
            worksheet.write(row, 2, 'NIF', cell_text_format)
            worksheet.write(row, 3, 'N° CNSS', cell_text_format)
            worksheet.write(row, 4, 'Date d\'embauche', cell_text_format)
            worksheet.write(row, 5, 'Avantages en électricité', cell_text_format)
            worksheet.write(row, 6, 'Avantages en logement', cell_text_format)
            row_set = row
            column = 7  # Modification de la position de début pour les règles de salaire
            # to write salary rules names in the row
            for vals in res:
                worksheet.write(row, column, vals[0], cell_text_format)
                column += 1
            row += 1
            col = 0
            ro = row

            # Modification pour filtrer également par structure
            domain = [('date_from', '=', self.from_date)]
            if self.structure_id:
                domain.append(('struct_id', '=', self.structure_id.id))

            payslip_ids = self.env['hr.payslip'].search(domain)

            if payslip_ids:
                for payslip in payslip_ids:
                    name = payslip.employee_id.name
                    id = payslip.employee_id.matricule
                    nif = payslip.employee_id.registration_number
                    numero_cnss = payslip.employee_id.numero_cnss

                    # Récupération des nouveaux champs depuis le contrat
                    contract = self.env['hr.contract'].search(
                        [('employee_id', '=', payslip.employee_id.id), ('state', '=', 'open')], limit=1)

                    date_embauche = contract.date_start if contract else False
                    avantage_electricite = contract.avantage_voiture if contract else 0
                    avantage_logement = contract.avantage_logement if contract else 0

                    worksheet.write(ro, col, name or '', cell_text_format_new)
                    worksheet.write(ro, col + 1, id or '', cell_text_format_new)
                    worksheet.write(ro, col + 2, nif or '', cell_text_format_new)
                    worksheet.write(ro, col + 3, numero_cnss or '', cell_text_format_new)
                    worksheet.write(ro, col + 4, date_embauche or '', cell_date_format)
                    worksheet.write(ro, col + 5, avantage_electricite or 0, cell_number_format)
                    worksheet.write(ro, col + 6, avantage_logement or 0, cell_number_format)

                    ro = ro + 1
            col = col + 7  # Modification pour refléter les nouvelles colonnes
            colm = col

            if payslip_ids:
                for payslip in payslip_ids:
                    for vals in res:
                        check = False
                        for line in payslip.line_ids:
                            if line.code == vals[1]:
                                check = True
                                r = line.total

                                # Si c'est le Total brut (supposons que le code soit 'BRUT'),
                                # ajoutez l'avantage en électricité
                                if vals[1] == 'BRUT':  # Remplacez 'BRUT' par le code réel du Total brut
                                    contract = self.env['hr.contract'].search(
                                        [('employee_id', '=', payslip.employee_id.id), ('state', '=', 'open')], limit=1)
                                    avantage_electricite = contract.avantage_voiture if contract else 0
                                    r += avantage_electricite

                        if check:
                            worksheet.write(row, col, r, cell_number_format)
                        else:
                            worksheet.write(row, col, 0, cell_number_format)

                        col += 1
                    row += 1
                    col = colm

            worksheet.write(row, 0, 'Total général', cell_text_format)
            worksheet.write(row, 1, '', cell_text_format)
            worksheet.write(row, 2, '', cell_text_format)
            worksheet.write(row, 3, '', cell_text_format)
            worksheet.write(row, 4, '', cell_text_format)
            worksheet.write(row, 5, '', cell_text_format)
            worksheet.write(row, 6, '', cell_text_format)

            # Calcul des sommes par colonne
            roww = row
            columnn = 7  # Position de début pour les totaux des règles de salaire
            for vals in res:
                cell1 = xl_rowcol_to_cell(row_set + 1, columnn)
                cell2 = xl_rowcol_to_cell(row - 1, columnn)
                worksheet.write_formula(row, columnn, '{=SUM(%s:%s)}' % (
                    cell1, cell2), normal_num_bold)
                columnn = columnn + 1

            # Calcul des totaux pour les avantages
            cell_elec_1 = xl_rowcol_to_cell(row_set + 1, 5)
            cell_elec_2 = xl_rowcol_to_cell(row - 1, 5)
            worksheet.write_formula(row, 5, '{=SUM(%s:%s)}' % (
                cell_elec_1, cell_elec_2), normal_num_bold)

            cell_log_1 = xl_rowcol_to_cell(row_set + 1, 6)
            cell_log_2 = xl_rowcol_to_cell(row - 1, 6)
            worksheet.write_formula(row, 6, '{=SUM(%s:%s)}' % (
                cell_log_1, cell_log_2), normal_num_bold)

        workbook.close()
        file_download = base64.b64encode(fp.getvalue())
        fp.close()

        # Créer l'attachement
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_download,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        _logger.info("Attachment created with ID: %s", attachment.id)

        # Retourne une action URL pour téléchargement direct
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


class PayrollReportExcel(models.TransientModel):
    _name = 'payroll.report.excel'
    _description = "Téléchargement du rapport de paie Excel"

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('Download payroll', readonly=True)