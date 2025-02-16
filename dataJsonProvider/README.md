# Data Json Provider

Ce projet est conçu pour récupérer, nettoyer et stocker les données financières pour un ticker donné à l'aide de la bibliothèque `yfinance`. Le projet est divisé en trois scripts principaux :

1. **`generateData.py`** : Script principal qui orchestre la récupération et le nettoyage des données.
2. **`fetchData.py`** : Script de récupération des données financières.
3. **`cleanData.py`** : Script de nettoyage des données financières.

## Structure du Projet

./
├── README.md
├── generateData.py
├── memory/                  # Stockage des fichiers JSON
│   ├── full/                # Données brutes récupérées
│   │   ├── GOOG_20250216_0118.json
│   │   ├── AMD_20250216_0121.json
│   ├── cleaned/             # Données nettoyées
│   │   ├── GOOG_20250216_0118_cleaned.json
│   │   ├── AMD_20250216_0121_cleaned.json
├── dataCleaner/             # Scripts de nettoyage des données
│   ├── cleanData.py
│   ├── __pycache__/
├── dataFetcher/             # Scripts de récupération des données
│   ├── fetchData.py
│   ├── __pycache__/



## Fonctionnement

### 1. `generateData.py`

Ce script est le point d'entrée du projet. Il prend un symbole de ticker en argument et orchestre la récupération et le nettoyage des données.

```sh
python generateData.py <ticker_symbol>
2. fetchData.py
Ce script récupère les données financières pour un ticker donné à l'aide de la bibliothèque yfinance. Les données récupérées sont stockées dans un fichier JSON dans le dossier memory/full.

3. cleanData.py
Ce script nettoie les données financières récupérées par fetchData.py. Les données nettoyées sont stockées dans un fichier JSON dans le dossier memory/cleaned.

Utilisation
Installer les dépendances :

pip install -r requirements.txt
Exécuter le script principal :

python generateData.py <ticker_symbol>
Remplacez <ticker_symbol> par le symbole du ticker pour lequel vous souhaitez récupérer les données (par exemple, AMD).

Exemple
Pour récupérer et nettoyer les données financières pour le ticker AMD :

python generateData.py AMD
Les fichiers JSON générés seront stockés dans les dossiers memory/full et memory/cleaned.

Contributions
Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une pull request pour toute suggestion ou correction.