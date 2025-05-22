# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import UserError, ValidationError
from math import *
from datetime import *
import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    anciennete = fields.Float(string="Ancienneté")
    net_wage = fields.Float(string="Salaire net", compute="_compute_salaire_net", store=True)
    heure_suplementaire = fields.Float(string="Heure suplémentaire")

    structure_name = fields.Char(
        string='Nom de la structure',
        compute='_compute_structure_name',
        store=True,
        help="Nom de la structure de paie"
    )

    @api.depends('struct_id', 'struct_id.name')
    def _compute_structure_name(self):
        for payslip in self:
            payslip.structure_name = payslip.struct_id.name if payslip.struct_id else False

    def compute_sheet(self):
        result = super().compute_sheet()
        self._compute_salaire_net()
        return result

    @api.depends('line_ids', 'line_ids.total')
    def _compute_salaire_net(self):
        for rec in self:
            total = 0
            for line in rec.line_ids:
                if line.sequence == 2000:
                    total += line.total
            rec.net_wage = total

    @api.onchange('contract_id', 'employee_id')
    def calcule_anciennete(self):
        for rec in self:
            date_debut = rec.contract_id.date_start
            date_fin = rec.date_to
            if date_debut and date_fin:
                datef = date_debut.strftime('%Y,%m,%d')
                dated = date_fin.strftime('%Y,%m,%d')
                n1 = datef.split(',')
                n2 = dated.split(',')
                d0 = datetime.date(int(n1[0]), int(n1[1]), int(n1[2]))
                d1 = datetime.date(int(n2[0]), int(n2[1]), int(n2[2]))
                deltat = d1 - d0
                annee = (deltat.days) / 365
                mois = ((deltat.days) - int(annee) * 365) / 30
                rec.anciennete = deltat.days
            hs = rec.contract_id.heure_sup_20 + rec.contract_id.heure_sup_40 + rec.contract_id.heure_sup_65 + rec.contract_id.heure_sup_100 + rec.contract_id.heure_sup_nuit
            rec.heure_suplementaire = hs


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def _add_date_libs(self, localdict):
        localdict.update({
            'floor': floor,
            'ceil': ceil,
        })
        return localdict

    def _compute_rule(self, localdict):
        """
        :param localdict: dictionary containing the environement in which to compute the rule
        :return: returns a tuple build as the base/amount computed, the quantity and the rate
        :rtype: (float, float, float)
        """
        self.ensure_one()
        localdict = self._add_date_libs(localdict)
        return super(HrSalaryRule, self)._compute_rule(localdict)

    def _satisfy_condition(self, localdict):
        """
        @param contract_id: id of hr.contract to be tested
        @return: returns True if the given rule match the condition for the given contract. Return False otherwise.
        """
        self.ensure_one()
        localdict = self._add_date_libs(localdict)
        return super(HrSalaryRule, self)._satisfy_condition(localdict)