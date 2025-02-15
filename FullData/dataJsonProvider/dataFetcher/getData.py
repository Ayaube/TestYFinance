"""
Script de récupération et de stockage des données financières pour un ticker donné (GOOG) à l'aide de la bibliothèque yfinance.

Fonctionnement :
1. Activer le mode debug pour yfinance.
2. Déterminer les chemins de stockage des données.
3. Initialiser le ticker pour GOOG.
4. Définir des fonctions pour ajouter et récupérer les données avec gestion des erreurs.
5. Récupérer diverses données financières (historique, bilans, états financiers, etc.).
6. Nettoyer les données pour remplacer les valeurs NaN par None.
7. Sérialiser les données nettoyées en JSON.
8. Écrire les données sérialisées dans un fichier JSON avec un nom dynamique basé sur le ticker, la date et l'heure actuelles.
9. Appeler le script cleanData.py pour nettoyer les données.

Ordre logique des choses :
1. Importations et configuration initiale.
2. Définition des chemins de stockage.
3. Initialisation du ticker.
4. Définition des fonctions de récupération et d'ajout des données.
5. Récupération des données financières.
6. Nettoyage des données.
7. Sérialisation et écriture des données en JSON.
8. Appel du script cleanData.py.
"""

import yfinance as yf
import json
import os
import pandas as pd
from datetime import datetime
import numpy as np
import subprocess

# Activer le mode debug pour yfinance
yf.enable_debug_mode()

# Chemin du script actuel
script_path = os.path.abspath(__file__)

# Chemin du dossier contenant le script
script_dir = os.path.dirname(script_path)

# Chemin du dossier de stockage (memory) au même niveau que le dossier contenant le script
storage_path = os.path.join(script_dir, '..', 'memory/full')

# Assurer que le dossier de stockage existe
os.makedirs(storage_path, exist_ok=True)

# Initialiser le ticker pour GOOG
ticker = yf.Ticker("GOOG")

# Dictionnaire pour stocker les données et les requêtes
data = {}

# Fonction pour ajouter les données et la requête au dictionnaire
def add_data(key, value, request):
    if isinstance(value, dict):
        value = {str(k): v for k, v in value.items()}
    data[key] = {
        "request": request,
        "data": value
    }

# Fonction pour récupérer et ajouter les données avec gestion des erreurs
def fetch_and_add_data(key, fetch_function, request):
    try:
        value = fetch_function()
        if value is not None and (not hasattr(value, 'empty') or not value.empty):
            add_data(key, value, request)
        else:
            print(f"Aucune donnée récupérée pour {key}")
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour {key}: {e}")

# Récupérer les données historiques pour les 5 dernières années
fetch_and_add_data("history", lambda: ticker.history(period="5y").reset_index().to_dict(orient='list'), "ticker.history(period='5y')")

# Récupérer les bilans
fetch_and_add_data("balance_sheet", lambda: ticker.balance_sheet.to_dict(), "ticker.balance_sheet")

# Récupérer les états financiers trimestriels
fetch_and_add_data("quarterly_income_stmt", lambda: ticker.quarterly_income_stmt.to_dict(), "ticker.quarterly_income_stmt")

# Récupérer le calendrier
fetch_and_add_data("calendar", lambda: ticker.calendar, "ticker.calendar")

# Récupérer les informations générales
fetch_and_add_data("info", lambda: ticker.info, "ticker.info")

# Récupérer les cibles de prix des analystes
fetch_and_add_data("analyst_price_targets", lambda: ticker.analyst_price_targets, "ticker.analyst_price_targets")

# Récupérer les dividendes
fetch_and_add_data("dividends", lambda: ticker.dividends.to_dict(), "ticker.dividends")

# Récupérer les splits
fetch_and_add_data("splits", lambda: ticker.splits.to_dict(), "ticker.splits")

# Récupérer les gains en capital
fetch_and_add_data("capital_gains", lambda: ticker.capital_gains.to_dict(), "ticker.capital_gains")

# Récupérer les flux de trésorerie
fetch_and_add_data("cash_flow", lambda: ticker.cashflow.to_dict(), "ticker.cashflow")

# Récupérer les revenus estimés
fetch_and_add_data("revenue_estimate", lambda: ticker.revenue_estimate.to_dict(), "ticker.revenue_estimate")

# Récupérer les estimations de croissance
fetch_and_add_data("growth_estimates", lambda: ticker.growth_estimates.to_dict(), "ticker.growth_estimates")

# Récupérer les recommandations
fetch_and_add_data("recommendations", lambda: ticker.recommendations.to_dict(orient='list'), "ticker.recommendations")

# Récupérer les résumés des recommandations
fetch_and_add_data("recommendations_summary", lambda: ticker.recommendations_summary.to_dict(), "ticker.recommendations_summary")

# Récupérer les estimations des bénéfices
fetch_and_add_data("earnings_estimate", lambda: ticker.earnings_estimate.to_dict(), "ticker.earnings_estimate")

# Récupérer les historiques des bénéfices
fetch_and_add_data("earnings_history", lambda: ticker.earnings_history.to_dict(orient='list'), "ticker.earnings_history")

# Récupérer les tendances des bénéfices
fetch_and_add_data("eps_trend", lambda: ticker.eps_trend.to_dict(), "ticker.eps_trend")

# Récupérer les révisions des bénéfices
fetch_and_add_data("eps_revisions", lambda: ticker.eps_revisions.to_dict(), "ticker.eps_revisions")

# Récupérer les dates des bénéfices
fetch_and_add_data("earnings_dates", lambda: ticker.earnings_dates.to_dict(orient='list'), "ticker.earnings_dates")

# Récupérer les filings SEC
fetch_and_add_data("sec_filings", lambda: ticker.sec_filings, "ticker.sec_filings")

# Récupérer les actions des insiders
fetch_and_add_data("insider_purchases", lambda: ticker.insider_purchases.to_dict(orient='list'), "ticker.insider_purchases")

# Récupérer les transactions des insiders
fetch_and_add_data("insider_transactions", lambda: ticker.insider_transactions.to_dict(orient='list'), "ticker.insider_transactions")

# Récupérer les principaux détenteurs
fetch_and_add_data("major_holders", lambda: ticker.major_holders.to_dict(orient='list'), "ticker.major_holders")

# Récupérer les détenteurs institutionnels
fetch_and_add_data("institutional_holders", lambda: ticker.institutional_holders.to_dict(orient='list'), "ticker.institutional_holders")

# Récupérer les détenteurs de fonds mutuels
fetch_and_add_data("mutualfund_holders", lambda: ticker.mutualfund_holders.to_dict(orient='list'), "ticker.mutualfund_holders")

# Récupérer les actualités
fetch_and_add_data("news", lambda: ticker.news, "ticker.news")

# Récupérer les données de durabilité
fetch_and_add_data("sustainability", lambda: ticker.sustainability.to_dict(), "ticker.sustainability")

# Récupérer les mises à jour et les baisses de cotation
fetch_and_add_data("upgrades_downgrades", lambda: ticker.upgrades_downgrades.to_dict(orient='list'), "ticker.upgrades_downgrades")

# Récupérer les informations rapides
fetch_and_add_data("fast_info", lambda: ticker.fast_info, "ticker.fast_info")

# Récupérer les informations détaillées sur les actions
fetch_and_add_data("shares_full", lambda: ticker.get_shares_full().to_dict(), "ticker.get_shares_full()")

# Récupérer les détenteurs de la liste des insiders
fetch_and_add_data("insider_roster_holders", lambda: ticker.get_insider_roster_holders().to_dict(orient='list'), "ticker.get_insider_roster_holders()")

# Récupérer les métadonnées des données historiques
fetch_and_add_data("history_metadata", lambda: ticker.get_history_metadata(), "ticker.get_history_metadata()")

# Récupérer le numéro ISIN
fetch_and_add_data("isin", lambda: ticker.get_isin(), "ticker.get_isin()")

# Fonction pour nettoyer les données et remplacer les valeurs NaN par None
def clean_data(obj):
    if isinstance(obj, dict):
        return {k: clean_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_data(v) for v in obj]
    elif isinstance(obj, (float, int)) and np.isnan(obj):
        return None
    else:
        return obj

# Nettoyer les données avant de les sérialiser
cleaned_data = clean_data(data)

# Fonction de conversion pour les valeurs JSON
def json_serializer(obj):
    if isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    elif isinstance(obj, (float, int, str, bool, type(None))):
        return obj
    elif isinstance(obj, dict):
        return {str(k): json_serializer(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_serializer(v) for v in obj]
    else:
        return str(obj)

# Générer le nom du fichier JSON dynamiquement
now = datetime.now()
filename = f"{ticker.ticker}_{now.strftime('%Y%m%d_%H%M')}.json"

# Chemin complet du fichier JSON
file_path = os.path.join(storage_path, filename)

# Écrire les données dans un fichier JSON
with open(file_path, "w") as f:
    json.dump(cleaned_data, f, indent=4, default=json_serializer)

print(f"Les données ont été enregistrées dans {file_path}")

# Chemin du script cleanData.py
clean_data_script_path = os.path.join(script_dir, '..', 'dataCleaner', 'cleanData.py')

# Exécuter le script cleanData.py
subprocess.run(['python', clean_data_script_path, file_path])

print(f"Le script cleanData.py a été exécuté avec succès.")