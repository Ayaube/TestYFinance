"""
Script de nettoyage des données financières pour un fichier JSON donné.

Fonctionnement :
1. Vérifier si le chemin du fichier JSON est passé en argument.
2. Déterminer les chemins de stockage des données.
3. Générer le nom du fichier nettoyé.
4. Nettoyer les données de balance_sheet pour ne conserver que les éléments essentiels.
5. Nettoyer les données de quarterly_income_stmt pour ne conserver que les éléments essentiels.
6. Nettoyer les données de info pour ne conserver que les éléments essentiels.
7. Nettoyer les données de cash_flow pour ne conserver que les éléments essentiels.
8. Nettoyer les données de news pour ne conserver que les éléments essentiels.
9. Nettoyer les données de insider_roster_holders pour ne conserver que les éléments essentiels.
10. Écrire les données nettoyées dans un nouveau fichier JSON dans un sous-dossier 'cleaned'.

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
8. Nettoyage des données de cash_flow.
9. Nettoyage des données de news.
10. Nettoyage des données de insider_roster_holders.
11. Écriture des données nettoyées dans un nouveau fichier JSON.
"""

import json
import sys
from datetime import datetime
import logging
from pathlib import Path

class CleanData:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = self._setup_output_file_path()
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _setup_output_file_path(self):
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        storage_path = script_dir.parent / 'memory'
        cleaned_storage_path = storage_path / 'cleaned'
        cleaned_storage_path.mkdir(parents=True, exist_ok=True)
        base_filename = Path(self.input_file_path).name
        cleaned_filename = base_filename.replace('.json', '_cleaned.json')
        return cleaned_storage_path / cleaned_filename

    def clean_balance_sheet(self, data):
        if 'balance_sheet' in data:
            balance_sheet = data['balance_sheet']['data']
            current_year = datetime.now().year
            last_year = current_year - 1
            last_year_str = f"{last_year}-12-31 00:00:00"

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

            cleaned_data = {}
            for date, values in balance_sheet.items():
                if date >= last_year_str:
                    cleaned_data[date] = {k: v for k, v in values.items() if k in keep_keys}
            data['balance_sheet']['data'] = cleaned_data
        return data

    def clean_quarterly_income_stmt(self, data):
        if 'quarterly_income_stmt' in data:
            income_stmt = data['quarterly_income_stmt']['data']

            keep_keys = [
                "Total Revenue", "Gross Profit", "EBITDA", "EBIT", "Operating Income",
                "Net Income", "Normalized Income", "Pretax Income", "Diluted NI Available to Common Stockholders",
                "Total Expenses", "Operating Expense", "Cost Of Revenue", "Selling General And Administration",
                "Selling And Marketing Expense", "Research And Development", "Tax Provision",
                "Tax Rate For Calcs", "Net Interest Income", "Interest Expense", "Interest Income",
                "Total Unusual Items", "Tax Effect Of Unusual Items", "Gain On Sale Of Security",
                "Other Income Expense", "Earnings From Equity Interest"
            ]

            cleaned_data = {}
            for date, values in income_stmt.items():
                cleaned_data[date] = {k: v for k, v in values.items() if k in keep_keys}
            data['quarterly_income_stmt']['data'] = cleaned_data
        return data

    def clean_info(self, data):
        if 'info' in data:
            info = data['info']['data']

            keep_keys = [
                "shortName", "symbol", "sector", "industry",
                "totalRevenue", "grossProfits", "ebitda", "netIncomeToCommon",
                "revenueGrowth", "earningsGrowth", "grossMargins", "operatingMargins",
                "returnOnAssets", "returnOnEquity", "currentPrice", "marketCap",
                "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months",
                "enterpriseToRevenue", "enterpriseToEbitda", "dividendRate",
                "dividendYield", "payoutRatio", "exDividendDate", "totalCash",
                "totalDebt", "debtToEquity", "quickRatio", "currentRatio",
                "freeCashflow", "operatingCashflow", "targetHighPrice",
                "targetLowPrice", "targetMeanPrice", "recommendationMean",
                "numberOfAnalystOpinions", "beta", "52WeekChange", "SandP52WeekChange",
                "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyDayAverage", "twoHundredDayAverage",
                "lastDividendValue", "lastDividendDate", "trailingPegRatio",
                "sharesOutstanding", "floatShares", "heldPercentInstitutions", "heldPercentInsiders"
            ]

            cleaned_data = {k: v for k, v in info.items() if k in keep_keys}
            data['info']['data'] = cleaned_data
        return data

    def clean_cash_flow(self, data):
        if 'cash_flow' in data:
            cash_flow = data['cash_flow']['data']

            keep_keys = [
                "Operating Cash Flow", "Cash Flow From Continuing Operating Activities",
                "Net Income From Continuing Operations", "Depreciation And Amortization",
                "Stock Based Compensation", "Deferred Tax", "Investing Cash Flow",
                "Capital Expenditure", "Net PPE Purchase And Sale", "Net Investment Purchase And Sale",
                "Financing Cash Flow", "Repurchase Of Capital Stock", "Cash Dividends Paid",
                "Long Term Debt Issuance", "Long Term Debt Payments", "Net Issuance Payments Of Debt",
                "End Cash Position", "Beginning Cash Position", "Changes In Cash"
            ]

            cleaned_data = {}
            for date, values in cash_flow.items():
                cleaned_data[date] = {k: v for k, v in values.items() if k in keep_keys}
            data['cash_flow']['data'] = cleaned_data
        return data

    def clean_news(self, data):
        if 'news' in data:
            news = data['news']['data']

            keep_keys = [
                "id", "title", "summary", "pubDate", "canonicalUrl"
            ]

            cleaned_data = []
            for item in news:
                cleaned_item = {k: v for k, v in item['content'].items() if k in keep_keys}
                cleaned_data.append({"id": item["id"], "content": cleaned_item})
            data['news']['data'] = cleaned_data
        return data

    def clean_insider_roster_holders(self, data):
        if 'insider_roster_holders' in data:
            insider_roster_holders = data['insider_roster_holders']['data']

            keep_keys = [
                "Name", "Position", "Most Recent Transaction", "Latest Transaction Date",
                "Shares Owned Directly", "Shares Owned Indirectly"
            ]

            cleaned_data = {k: v for k, v in insider_roster_holders.items() if k in keep_keys}
            data['insider_roster_holders']['data'] = cleaned_data
        return data

    def execute(self):
        try:
            with open(self.input_file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du fichier JSON: {e}")
            sys.exit(1)

        cleaned_data = self.clean_balance_sheet(data)
        cleaned_data = self.clean_quarterly_income_stmt(cleaned_data)
        cleaned_data = self.clean_info(cleaned_data)
        cleaned_data = self.clean_cash_flow(cleaned_data)
        cleaned_data = self.clean_news(cleaned_data)
        cleaned_data = self.clean_insider_roster_holders(cleaned_data)

        try:
            with open(self.output_file_path, 'w') as f:
                json.dump(cleaned_data, f, indent=4)
            logging.info(f"Les données nettoyées ont été enregistrées dans {self.output_file_path}")
        except Exception as e:
            logging.error(f"Erreur lors de l'écriture du fichier JSON nettoyé: {e}")
            sys.exit(1)