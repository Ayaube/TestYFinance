"""
Script de nettoyage des données financières pour un fichier JSON donné.

Fonctionnement :
1. Vérifier si le chemin du fichier JSON est passé en argument.
2. Déterminer les chemins de stockage des données.
3. Générer le nom du fichier nettoyé.
4. Nettoyer les données de balance_sheet pour ne conserver que les éléments essentiels.
5. Nettoyer les données de quarterly_income_stmt pour ne conserver que les éléments essentiels.
6. Nettoyer les données de info pour ne conserver que les éléments essentiels.
7. Écrire les données nettoyées dans un nouveau fichier JSON dans un sous-dossier 'cleaned'.

Arguments :
- <input_file_path> : Chemin du fichier JSON à nettoyer.

Ordre logique des choses :
1. Vérification des arguments.
2. Définition des chemins de stockage.
3. Génération du nom du fichier nettoyé.
4. Lecture du fichier JSON.
5. Nettoyage des données de balance_sheet.
6. Nettoyage des données de quarterly_income_stmt.
7. Nettoyage des données de info.
8. Écriture des données nettoyées dans un nouveau fichier JSON.
"""

import json
import os
import sys
from datetime import datetime

# Vérifier si le chemin du fichier JSON est passé en argument
if len(sys.argv) != 2:
    print("Usage: python cleanData.py <input_file_path>")
    sys.exit(1)

input_file_path = sys.argv[1]

# Chemin du script actuel
script_path = os.path.abspath(__file__)

# Chemin du dossier contenant le script
script_dir = os.path.dirname(script_path)

# Chemin du dossier de stockage (memory) au même niveau que le dossier contenant le script
storage_path = os.path.join(script_dir, '..', 'memory')

# Chemin du sous-dossier cleaned
cleaned_storage_path = os.path.join(storage_path, 'cleaned')

# Assurer que le dossier cleaned existe
os.makedirs(cleaned_storage_path, exist_ok=True)

# Générer le nom du fichier nettoyé
base_filename = os.path.basename(input_file_path)
cleaned_filename = os.path.splitext(base_filename)[0] + '_cleaned.json'

# Chemin du fichier JSON nettoyé
output_file_path = os.path.join(cleaned_storage_path, cleaned_filename)

# Fonction pour nettoyer les données de balance_sheet
def clean_balance_sheet(data):
    if 'balance_sheet' in data:
        balance_sheet = data['balance_sheet']['data']
        current_year = datetime.now().year
        last_year = current_year - 1
        last_year_str = f"{last_year}-12-31 00:00:00"

        # Éléments à garder
        keep_keys = [
            "Ordinary Shares Number", "Total Debt", "Common Stock Equity",
            "Stockholders Equity", "Retained Earnings", "Total Capitalization",
            "Invested Capital", "Total Liabilities Net Minority Interest",
            "Current Liabilities", "Long Term Debt", "Payables And Accrued Expenses",
            "Total Tax Payable", "Current Debt And Capital Lease Obligation",
            "Total Assets", "Current Assets", "Cash Cash Equivalents And Short Term Investments",
            "Receivables", "Net PPE", "Goodwill And Other Intangible Assets",
            "Investments And Advances", "Working Capital", "Tangible Book Value",
            "Accumulated Depreciation"
        ]

        # Filtrer les données pour ne conserver que les éléments essentiels et les données de la dernière année
        cleaned_data = {}
        for date, values in balance_sheet.items():
            if date >= last_year_str:
                cleaned_data[date] = {k: v for k, v in values.items() if k in keep_keys}

        data['balance_sheet']['data'] = cleaned_data
    return data

# Fonction pour nettoyer les données de quarterly_income_stmt
def clean_quarterly_income_stmt(data):
    if 'quarterly_income_stmt' in data:
        income_stmt = data['quarterly_income_stmt']['data']

        # Éléments à garder
        keep_keys = [
            "Total Revenue", "Gross Profit", "EBITDA", "EBIT", "Operating Income",
            "Net Income", "Normalized Income", "Pretax Income", "Diluted NI Available to Common Stockholders",
            "Total Expenses", "Operating Expense", "Cost Of Revenue", "Selling General And Administration",
            "Selling And Marketing Expense", "Research And Development", "Tax Provision",
            "Tax Rate For Calcs", "Net Interest Income", "Interest Expense", "Interest Income",
            "Total Unusual Items", "Tax Effect Of Unusual Items", "Gain On Sale Of Security",
            "Other Income Expense", "Earnings From Equity Interest"
        ]

        # Filtrer les données pour ne conserver que les éléments essentiels
        cleaned_data = {}
        for date, values in income_stmt.items():
            cleaned_data[date] = {k: v for k, v in values.items() if k in keep_keys}

        data['quarterly_income_stmt']['data'] = cleaned_data
    return data

# Fonction pour nettoyer les données de info
def clean_info(data):
    if 'info' in data:
        info = data['info']['data']

        # Éléments à garder
        keep_keys = [
            "shortName", "symbol", "sector", "industry",
            "totalRevenue", "grossProfits", "ebitda", "netIncomeToCommon",
            "revenueGrowth", "earningsGrowth", "grossMargins", "operatingMargins",
            "returnOnAssets", "returnOnEquity", "currentPrice", "marketCap",
            "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months",
            "enterpriseToRevenue", "enterpriseToEbitda", "dividendRate",
            "dividendYield", "payoutRatio", "exDividendDate", "totalCash",
            "totalDebt", "debtToEquity", "quickRatio", "currentRatio",
            "freeCashflow", "operatingCashflow",
            "targetHighPrice", "targetLowPrice", "targetMeanPrice",
            "recommendationMean", "numberOfAnalystOpinions", "beta",
            "52WeekChange", "SandP52WeekChange", "fiftyTwoWeekHigh",
            "fiftyTwoWeekLow", "fiftyDayAverage", "twoHundredDayAverage",
            "lastDividendValue", "lastDividendDate", "trailingPegRatio",
            "sharesOutstanding", "floatShares",
            "heldPercentInstitutions", "heldPercentInsiders"
        ]

        # Filtrer les données pour ne conserver que les éléments essentiels
        cleaned_data = {k: v for k, v in info.items() if k in keep_keys}

        data['info']['data'] = cleaned_data
    return data

# Lire le fichier JSON généré par le premier script
with open(input_file_path, 'r') as f:
    data = json.load(f)

# Nettoyer les données de balance_sheet
cleaned_data = clean_balance_sheet(data)

# Nettoyer les données de quarterly_income_stmt
cleaned_data = clean_quarterly_income_stmt(cleaned_data)

# Nettoyer les données de info
cleaned_data = clean_info(cleaned_data)

# Écrire les données nettoyées dans un nouveau fichier JSON
with open(output_file_path, 'w') as f:
    json.dump(cleaned_data, f, indent=4)

print(f"Les données nettoyées ont été enregistrées dans {output_file_path}")