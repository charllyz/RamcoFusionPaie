# Paie TOGO avec Ordres de Virement

## Description

Ce module a été développé pour gérer la paie des entreprises au Togo, avec une attention particulière aux spécificités locales. Il intègre également la gestion complète des ordres de virement, offrant ainsi une solution de bout en bout pour le processus de paie.

## Principales fonctionnalités

### Gestion de la paie

- **Structures de paie spécifiques** pour différentes catégories d'employés :
  - PAIE TOGO (employés standard)
  - PAIE TOGO Congés (pour les périodes de congés)
  - PAIE EXPA (pour les expatriés)
  - PAIE TOGO STAGIAIRE (pour les stagiaires)

- **Calcul automatique des éléments de paie** :
  - Salaire de base
  - Prime d'ancienneté (calculée automatiquement selon l'ancienneté de l'employé)
  - Heures supplémentaires (avec différents taux : 20%, 40%, 65%, 100%)
  - Diverses primes et indemnités couramment utilisées au Togo
  - Retenues légales et conventionnelles (CNSS, IRPP, etc.)

- **Gestion des personnes à charge** avec calcul automatique de l'âge

### Ordres de virement

- Génération des ordres de virement à partir des bulletins de paie
- Support de différents types de paiement :
  - Virement bancaire
  - Chèque
  - Espèce
- Format d'impression standardisé pour les banques togolaises
- Export Excel des ordres de virement

### Rapports avancés

- **Bulletins de paie personnalisés** selon la structure de paie
- **Livre de paie mensuel** en format PDF et Excel
- **Livre de paie annuel** pour une vision consolidée
- **Fiche individuelle de paie** sur diverses périodes :
  - Mensuelle
  - Trimestrielle
  - Semestrielle
  - Annuelle

## Installation

1. Téléchargez le module dans le dossier des addons Odoo
2. Mettez à jour la liste des applications
3. Installez le module "Paie TOGO avec Ordres de Virement"

## Configuration

### Prérequis

Ce module nécessite l'installation préalable des modules suivants :
- `hr` (Ressources Humaines)
- `hr_payroll` (Paie)
- `report_xlsx` (pour les rapports Excel)

### Étapes de configuration

1. **Structures de paie** : Le module installe automatiquement 4 structures de paie principales (PAIE TOGO, PAIE TOGO Congés, PAIE EXPA, PAIE TOGO STAGIAIRE)

2. **Catégories de rubriques et règles salariales** : Le module crée automatiquement les catégories et règles de base. Vous pouvez les personnaliser selon vos besoins.

3. **Personnalisation des contrats** : Utilisez les champs supplémentaires des contrats pour spécifier les éléments de rémunération spécifiques (primes, avantages, etc.)

## Utilisation

### Gestion des bulletins de paie

1. Créez un nouveau bulletin de paie pour un employé
2. Sélectionnez la structure de paie appropriée
3. Calculez le bulletin
4. Utilisez les boutons spécifiques pour imprimer le modèle de bulletin adapté à la structure

### Génération des ordres de virement

1. Accédez au menu "Ordres de virement"
2. Créez un nouvel ordre de virement
3. Sélectionnez la banque, le mois de paie et le type de paiement
4. Ajoutez les bulletins de paie concernés
5. Générez le rapport PDF ou Excel

### Rapports

- **Livre de paie mensuel** : Menu Rapports de paie > Livre de paie en PDF/Excel
- **Livre de paie annuel** : Menu Rapports de paie > Livre de paie annuel en PDF
- **Fiche individuelle de paie** : Menu Rapports de paie > Fiche individuelle de paie

## Détails techniques

Ce module est le résultat de la fusion de deux modules complémentaires :
- `th_custum_payroll` : Gestion de la paie adaptée au Togo
- `th_order_virement` : Gestion des ordres de virement

La fusion a permis :
- D'éliminer les redondances
- D'optimiser le code
- D'assurer une meilleure intégration entre les fonctionnalités
- D'améliorer l'expérience utilisateur

## Contributions et support

Pour toute question, suggestion d'amélioration ou signalement de bug, veuillez contacter :
- Email : votre@email.com
- Site web : https://yourdomain.com

## Licence

Ce module est distribué sous licence AGPL-3.