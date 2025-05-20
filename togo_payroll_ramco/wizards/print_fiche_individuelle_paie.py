# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import ValidationError
from math import *
from datetime import *


class PrintFicheIndividuellePaie(models.TransientModel):
    _name = 'print.fiche.individuelle.paie'
    _description = 'Fiche individuelle de paie sur période'

    employee_id = fields.Many2one('hr.employee', string="Employé", required=True)
    date_debut = fields.Date(string="Date de début", required=True)
    date_fin = fields.Date(string="Date de fin", required=True)
    structure_id = fields.Many2one('hr.payroll.structure', string="Structure de paie")
    periode_type = fields.Selection([
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('semestriel', 'Semestriel'),
        ('annuel', 'Annuel')
    ], string="Type de période", default='mensuel')

    @api.onchange('periode_type', 'date_debut')
    def _onchange_periode_type(self):
        """Calcule automatiquement la date de fin en fonction du type de période"""
        if self.date_debut and self.periode_type:
            date_debut = self.date_debut
            if self.periode_type == 'mensuel':
                # Dernier jour du mois
                next_month = date_debut.replace(day=28) + timedelta(days=4)
                self.date_fin = next_month - timedelta(days=next_month.day)
            elif self.periode_type == 'trimestriel':
                # Dernier jour du trimestre
                month = date_debut.month
                quarter_end_month = ((month - 1) // 3 * 3) + 3
                if quarter_end_month > 12:
                    quarter_end_month = 12
                next_month = date_debut.replace(month=quarter_end_month, day=28) + timedelta(days=4)
                self.date_fin = next_month - timedelta(days=next_month.day)
            elif self.periode_type == 'semestriel':
                # Dernier jour du semestre
                month = date_debut.month
                semester_end_month = 6 if month <= 6 else 12
                next_month = date_debut.replace(month=semester_end_month, day=28) + timedelta(days=4)
                self.date_fin = next_month - timedelta(days=next_month.day)
            elif self.periode_type == 'annuel':
                # Dernier jour de l'année
                self.date_fin = date(date_debut.year, 12, 31)

    def print_report(self):
        data = {}

        # Obtenir les règles salariales de la structure de paie sélectionnée
        head_ids = []
        if self.structure_id:
            for rule in self.env['hr.salary.rule'].search([('struct_id', '=', self.structure_id.id)]):
                head_ids.append([rule.name, rule.code])
        else:
            # Si aucune structure n'est sélectionnée, obtenir toutes les règles utilisées dans les fiches de paie de l'employé
            payslips = self.env['hr.payslip'].search([
                ('employee_id', '=', self.employee_id.id),
                ('date_from', '>=', self.date_debut),
                ('date_to', '<=', self.date_fin)
            ])
            rule_codes = set()
            for payslip in payslips:
                for line in payslip.line_ids:
                    rule_codes.add((line.name, line.code))

            head_ids = list(rule_codes)

        # Récupérer les fiches de paie de l'employé pour la période
        employee_payslips = self.env['hr.payslip'].search([
            ('employee_id', '=', self.employee_id.id),
            ('date_from', '>=', self.date_debut),
            ('date_to', '<=', self.date_fin)
        ], order='date_from')

        # Organiser les données par période
        period_data = []

        for payslip in employee_payslips:
            period_values = {
                'period': payslip.date_from.strftime('%B %Y'),
                'date_from': payslip.date_from,
                'date_to': payslip.date_to,
                'lines': []
            }

            # Ajouter les lignes de paie
            for head in head_ids:
                line_value = {
                    'code': head[1],
                    'name': head[0],
                    'total': 0
                }

                # Trouver la valeur correspondante dans la fiche de paie
                for line in payslip.line_ids:
                    if line.code == head[1]:
                        line_value['total'] = line.total
                        break

                period_values['lines'].append(line_value)

            period_data.append(period_values)

        # Calculer les totaux
        total_values = {
            'period': 'Total',
            'lines': []
        }

        for head in head_ids:
            head_total = 0
            for period in period_data:
                for line in period['lines']:
                    if line['code'] == head[1]:
                        head_total += line['total']
                        break

            total_values['lines'].append({
                'code': head[1],
                'name': head[0],
                'total': head_total
            })

        period_data.append(total_values)

        # Informations sur l'employé
        employee_info = {
            'name': self.employee_id.name or '',
            'matricule': self.employee_id.matricule or '',
            'job_title': self.employee_id.job_id.name if self.employee_id.job_id else '',
            'department': self.employee_id.department_id.name if self.employee_id.department_id else '',
            'date_embauche': self.employee_id.first_contract_date,
            'numero_cnss': self.employee_id.numero_cnss or '',
        }

        # Informations sur l'entreprise
        company = self.env.company
        company_info = {
            'name': company.name or '',
            'logo': company.logo or False,
            'street': company.street or '',
            'zip': company.zip or '',
            'country': company.country_id.name if company.country_id else '',
            'city': company.city or '',
            'phone': company.phone or '',
            'email': company.email or '',
        }

        # Préparer les données pour le rapport
        data = {
            'employee': employee_info,
            'compayinfo': company_info,
            'heads': head_ids,
            'periods': period_data,
            'date_debut': self.date_debut.strftime('%d/%m/%Y'),
            'date_fin': self.date_fin.strftime('%d/%m/%Y'),
            'periode_type': dict(self._fields['periode_type'].selection).get(self.periode_type),
        }

        return self.env.ref('togo_payroll_virement.fiche_individuelle_paie_report').report_action(self, data=data)