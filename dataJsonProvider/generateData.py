import sys
from dataFetcher.fetchData import FetchData
from dataCleaner.cleanData import CleanData

def generate_data(ticker_symbol):
    """
    Génère les données financières pour un ticker donné en récupérant les données
    et en les nettoyant.

    Arguments:
    - ticker_symbol (str): Le symbole du ticker pour lequel récupérer les données.

    Fonctionnement:
    1. Récupérer les données financières pour le ticker donné.
    2. Nettoyer les données récupérées.
    3. Écrire les données nettoyées dans un fichier JSON.
    """
    # Récupérer les données
    fetch_data = FetchData(ticker_symbol)
    file_path = fetch_data.execute()

    # Nettoyer les données
    clean_data = CleanData(file_path)
    clean_data.execute()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generateData.py <ticker_symbol>")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    generate_data(ticker_symbol)