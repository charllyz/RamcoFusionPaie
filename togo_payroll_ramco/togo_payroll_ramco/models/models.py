# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import UserError, ValidationError
from math import *
from datetime import *
import datetime
import dateutil

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    persone_acharge_ids = fields.One2many(
        'hr.personne.acharge',
        'employee_id',
        string='Personnes à charge',
    )
    numero_cnss = fields.Char(
        string="Numéro de CNSS",
    )
    matricule = fields.Char(
        string='Numéro matricule',
    )
    payslip_ids = fields.One2many(
        'hr.payslip',
        'employee_id',
        string='Bulletins de paie',
    )
    heure_travail = fields.Float(
        string="Nombre d'heure de travail",
    )
    account_number = fields.Char(
        string="Numéro de compte"
    )
    banque_id = fields.Many2one(
        'res.bank',
        string='Banque',
    )
    indice = fields.Float(
        string="Indice"
    )
    valeur_indice = fields.Float(
        string="Valeur indice"
    )

    @api.onchange('persone_acharge_ids')
    def onchange_persone_acharge_ids(self):
        for rec in self:
            rec.children = len(rec.persone_acharge_ids)

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    numero_cnss = fields.Char(string="Numéro de CNSS")
    matricule = fields.Char(
        string='Numéro matricule',
    )
    payslip_ids = fields.One2many(
        'hr.payslip',
        'employee_id',
        string='Bulletins de paie',
    )
    heure_travail = fields.Float(
        string="Nombre d'heure de travail",
    )
    account_number = fields.Char(
        string="Numéro de compte"
    )
    banque_id = fields.Many2one(
        'res.bank',
        string='Banque',
    )
    indice = fields.Float(
        string="Indice"
    )
    valeur_indice = fields.Float(
        string="Valeur indice"
    )

class HrContactInherit(models.Model):
    _inherit = 'hr.contract'

    heure_sup_20 = fields.Float(
        string='HEURES SUPP 20%',
        default=0,
    )
    heure_sup_40 = fields.Float(
        string='HEURES SUPP 40%',
        default=0,
    )
    heure_sup_65 = fields.Float(
        string='HEURES SUPP 65%',
        default=0,
    )
    heure_sup_100 = fields.Float(
        string='HEURES SUPP 100%',
        default=0,
    )
    heure_sup_nuit = fields.Float(
        string='HEURES SUPP NUIT',
        default=0,
    )
    adjustement = fields.Float(
        string='Ajustement de salaire net',
        default=0,
    )
    taux_horaire = fields.Float(string="Taux horaire")
    nombre_jour = fields.Float(
        string="Nombre de jours travaillés",
        compute="_compute_nombre_jour",
        store=True
    )
    contrat_declare = fields.Boolean(string="Contrat déclaré")
    appel_urgence = fields.Float(
        string="Appel d'urgence",
        default=0,
    )
    astreinte = fields.Float(
        string='Astreinte',
        default=0,
    )
    conge_sans_solde = fields.Float(
        string='Nbr de jrs de congé sans solde',
        default=0,
    )
    prime_transport = fields.Float(
        string='Prime de transport',
        default=0,
    )
    x_studio_mois_dduire = fields.Float(
        string='Mois à déduire',
        default=0,
        help="Nombre de mois à déduire du calcul de l'ancienneté"
    )
    prime_caisse = fields.Float(
        string='Prime de caisse',
        default=0,
    )
    prime_garde = fields.Float(
        string='Prime de garde',
        default=0,
    )
    prime_panier = fields.Float(
        string='Prime de panier',
        default=0,
    )
    prime_risque = fields.Float(
        string='Prime de risque',
    )
    prime_salisure = fields.Float(
        string="Prime de salissure"
    )
    prime_resultat = fields.Float(string="Prime de resultat")
    prime_speciale = fields.Float(
        string='Prime spéciale',
    )
    prime_fonction = fields.Float(string="Prime de fonction")
    prime_specialite = fields.Float(
        string='Prime de spécialité',
    )
    prime_responsabilite = fields.Float(
        string='Prime de responsabilté',
    )
    rapel_salaire_imp = fields.Float(
        string='Rappel de salaire imposable',
    )
    remboursement_pret = fields.Float(
        string='Remboursement de prêt',
    )
    sursalaire = fields.Float(
        string='Sursalaire',
    )
    regularisation_salaire_net = fields.Float(
        string="Régularisation salaire net",
    )
    trop_percu = fields.Float(
        string='Trop perçu sur prime',
    )
    prime_logement = fields.Float(string="Prime de logement")
    prime_logement_10 = fields.Float(string="Prime de logement 10%")
    prime_13_mois = fields.Float(string="13ème mois")
    conge_paye = fields.Float(string="Congé payé/technique")
    indeminite_retraite_ir = fields.Float(string="Indemnité de retraite 50% A IR")
    indeminite_retraite_non_ir = fields.Float(string="Indemnité de retraite 50% non IR")
    relevement_salaire = fields.Float(string="Relevement de salaire")
    indeminite_compens = fields.Float(string="Indemnité de compens")
    commission = fields.Float(string="Commission")
    avantage_logement = fields.Float(string="Avantage en nature logement")
    avantage_voiture = fields.Float(string="Avantage en nature voiture")
    preavis = fields.Float(string="Préavis")
    precues_salaire = fields.Float(string="Percues sur salaire")
    indemnite_licenciement = fields.Float(string="Indemnité de licencement")
    autres_primes = fields.Float(string="Autres primes")
    habillement_encouragement = fields.Float(string="Habillement et encouragement")
    frais_forfait_remboursement = fields.Float(string="Frais forf remboursement")
    indemnite_non_imposable = fields.Float(string="Indemnité non imposable")
    indemnite_licenciement_35 = fields.Float(string="Indemnité de licencement 35%")
    indemnite_licenciement_40 = fields.Float(string="Indemnité de licencement 40%")
    indemnite_licenciement_45 = fields.Float(string="Indemnité de licencement 45%")
    retenue_syndicat = fields.Float(string="Retenue syndicat")
    retenue_assurance_maladie = fields.Float(string="Retenue assurance maladie")
    avance_accompte_retenues = fields.Float(string="Avance et accompte retenues")
    avance_retenue_13_hon = fields.Float(string="Avance retenue 13ème mois hon")
    absence_a_deduire = fields.Float(string="Absence à déduire")

    calcul_base = fields.Monetary(string="Base de calcul", currency_field='currency_id')

    type_paiement = fields.Selection([
        ('espece','Espèce'),
        ('virement','Virement'),
        ('cheque','Chèque banciare'),
    ], string="Type de paiement", default="virement")

    est_cadre = fields.Boolean(string="Est cadre ?")

    @api.depends('absence_a_deduire')
    def _compute_nombre_jour(self):
        for record in self:
            record.nombre_jour = 30 - record.absence_a_deduire if record.absence_a_deduire else 30

    @api.onchange('wage')
    def onchange_wage(self):
        for rec in self:
            rec.taux_horaire = rec.wage / 173.33

class HrPersoneACharge(models.Model):
    _name = 'hr.personne.acharge'
    _description = 'Personne à charge'

    name = fields.Char(
        string='Nom et prénom(s)',
        required=True,
    )
    date_naissance = fields.Date(string="Date de naissance")
    age = fields.Integer(
        string='Age',
        store=True,
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
    )

    @api.onchange('date_naissance')
    def _calculer_age(self):
        for rec in self:
            if rec.date_naissance:
                today_year = datetime.datetime.today().year
                birth_year = rec.date_naissance.year
                age = today_year - birth_year
                rec.age = age