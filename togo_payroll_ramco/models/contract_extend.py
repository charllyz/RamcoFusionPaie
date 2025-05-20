# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContractExtend(models.Model):
    _inherit = 'hr.contract'

    # Champs Studio à ajouter
    x_studio_mois_dduire = fields.Float(
        string='Mois à déduire',
        default=0,
        help="Nombre de mois à déduire du calcul de l'ancienneté"
    )
    x_studio_moins_peru_sur_salaire = fields.Float(
        string='Moins perçu sur salaire',
        default=0
    )
    x_studio_avantage_en_eau = fields.Float(
        string='Avantage en eau',
        default=0
    )
    x_studio_avantage_en_mdecine = fields.Float(
        string='Avantage en médecine',
        default=0
    )
    x_studio_float_field_tSmF1 = fields.Float(
        string='Complément 13ème mois',
        default=0
    )

    # Champs supplémentaires identifiés dans les règles salariales
    calcul_base = fields.Monetary(
        string="Base de calcul",
        currency_field='currency_id',
        default=0
    )