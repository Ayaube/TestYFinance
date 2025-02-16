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
import pandas as pd
from datetime import datetime
import numpy as np
import logging
from pathlib import Path

class FetchData:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.data = {}
        self.storage_path = self._setup_storage_path()
        self.ticker = yf.Ticker(self.ticker_symbol)
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _setup_storage_path(self):
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        storage_path = script_dir.parent / 'memory/full'
        storage_path.mkdir(parents=True, exist_ok=True)
        return storage_path

    def add_data(self, key, value, request):
        if isinstance(value, dict):
            value = {str(k): v for k, v in value.items()}
        self.data[key] = {"request": request, "data": value}

    def fetch_and_add_data(self, key, fetch_function, request):
        try:
            value = fetch_function()
            if value is not None and (not hasattr(value, 'empty') or not value.empty):
                self.add_data(key, value, request)
            else:
                logging.warning(f"Aucune donnée récupérée pour {key}")
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des données pour {key}: {e}")

    def fetch_all_data(self):
        self.fetch_and_add_data("history", lambda: self.ticker.history(period="5y").reset_index().to_dict(orient='list'), "ticker.history(period='5y')")
        self.fetch_and_add_data("isin", lambda: self.ticker.get_isin(), "ticker.get_isin()")
        self.fetch_and_add_data("balance_sheet", lambda: self.ticker.balance_sheet.to_dict(), "ticker.balance_sheet")
        self.fetch_and_add_data("quarterly_income_stmt", lambda: self.ticker.quarterly_income_stmt.to_dict(), "ticker.quarterly_income_stmt")
        self.fetch_and_add_data("calendar", lambda: self.ticker.calendar, "ticker.calendar")
        self.fetch_and_add_data("info", lambda: self.ticker.info, "ticker.info")
        self.fetch_and_add_data("analyst_price_targets", lambda: self.ticker.analyst_price_targets, "ticker.analyst_price_targets")
        self.fetch_and_add_data("dividends", lambda: self.ticker.dividends.to_dict(), "ticker.dividends")
        self.fetch_and_add_data("splits", lambda: self.ticker.splits.to_dict(), "ticker.splits")
        self.fetch_and_add_data("capital_gains", lambda: self.ticker.capital_gains.to_dict(), "ticker.capital_gains")
        self.fetch_and_add_data("cash_flow", lambda: self.ticker.cashflow.to_dict(), "ticker.cashflow")
        self.fetch_and_add_data("revenue_estimate", lambda: self.ticker.revenue_estimate.to_dict(), "ticker.revenue_estimate")
        self.fetch_and_add_data("growth_estimates", lambda: self.ticker.growth_estimates.to_dict(), "ticker.growth_estimates")
        self.fetch_and_add_data("recommendations", lambda: self.ticker.recommendations.to_dict(orient='list'), "ticker.recommendations")
        self.fetch_and_add_data("recommendations_summary", lambda: self.ticker.recommendations_summary.to_dict(), "ticker.recommendations_summary")
        self.fetch_and_add_data("earnings_estimate", lambda: self.ticker.earnings_estimate.to_dict(), "ticker.earnings_estimate")
        self.fetch_and_add_data("earnings_history", lambda: self.ticker.earnings_history.to_dict(orient='list'), "ticker.earnings_history")
        self.fetch_and_add_data("eps_trend", lambda: self.ticker.eps_trend.to_dict(), "ticker.eps_trend")
        self.fetch_and_add_data("eps_revisions", lambda: self.ticker.eps_revisions.to_dict(), "ticker.eps_revisions")
        self.fetch_and_add_data("earnings_dates", lambda: self.ticker.earnings_dates.to_dict(orient='list'), "ticker.earnings_dates")
        self.fetch_and_add_data("sec_filings", lambda: self.ticker.sec_filings, "ticker.sec_filings")
        self.fetch_and_add_data("insider_purchases", lambda: self.ticker.insider_purchases.to_dict(orient='list'), "ticker.insider_purchases")
        self.fetch_and_add_data("insider_transactions", lambda: self.ticker.insider_transactions.to_dict(orient='list'), "ticker.insider_transactions")
        self.fetch_and_add_data("major_holders", lambda: self.ticker.major_holders.to_dict(orient='list'), "ticker.major_holders")
        self.fetch_and_add_data("institutional_holders", lambda: self.ticker.institutional_holders.to_dict(orient='list'), "ticker.institutional_holders")
        self.fetch_and_add_data("mutualfund_holders", lambda: self.ticker.mutualfund_holders.to_dict(orient='list'), "ticker.mutualfund_holders")
        self.fetch_and_add_data("news", lambda: self.ticker.news, "ticker.news")
        self.fetch_and_add_data("sustainability", lambda: self.ticker.sustainability.to_dict(), "ticker.sustainability")
        self.fetch_and_add_data("upgrades_downgrades", lambda: self.ticker.get_upgrades_downgrades().reset_index().to_dict(orient='list'), "ticker.upgrades_downgrades")
        self.fetch_and_add_data("insider_roster_holders", lambda: self.ticker.get_insider_roster_holders().to_dict(orient='list'), "ticker.get_insider_roster_holders()")

    def clean_data(self, obj):
        if isinstance(obj, dict):
            return {k: self.clean_data(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.clean_data(v) for v in obj]
        elif isinstance(obj, (float, int)) and np.isnan(obj):
            return None
        else:
            return obj

    def json_serializer(self, obj):
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        elif isinstance(obj, (float, int, str, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            return {str(k): self.json_serializer(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.json_serializer(v) for v in obj]
        else:
            return str(obj)

    def save_data(self):
        cleaned_data = self.clean_data(self.data)
        now = datetime.now()
        filename = f"{self.ticker.ticker}_{now.strftime('%Y%m%d_%H%M')}.json"
        file_path = self.storage_path / filename
        with open(file_path, "w") as f:
            json.dump(cleaned_data, f, indent=4, default=self.json_serializer)
        logging.info(f"Les données ont été enregistrées dans {file_path}")
        return file_path

    def execute(self):
        yf.enable_debug_mode()
        self.fetch_all_data()
        return self.save_data()