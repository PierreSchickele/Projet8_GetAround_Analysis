# GetAround Analysis

Ce projet est une étude complète autour de la plateforme de location de voitures GetAround. Il comprend :
- Une **analyse des retards** lors des locations de véhicules.
- Un **modèle de machine learning** pour prédire le prix d'une location.
- Un **dashboard interactif** pour visualiser les résultats.
- Une **API FastAPI** pour exposer le modèle de prédiction.

## Structure du projet

```
getaround/
    1-api/         # API FastAPI pour la prédiction de prix
    2-dashboard/   # Dashboard Streamlit pour l'analyse des retards
    docker-compose.yaml
get_around_delay_analysis.xlsx   # Données d'analyse des retards
get_around_pricing_project.csv  # Données pour le machine learning
README.md
deploy.txt         # Instructions de déploiement
```

## Fonctionnalités

- **Analyse exploratoire** des données de location et des retards.
- **Modélisation** : XGBoost pour la prédiction du prix de location.
- **API** : Endpoint `/predict` pour obtenir une prédiction à partir de caractéristiques d'une location.
- **Dashboard** : Visualisation des retards et accès à l'API.

## Installation

1. **Cloner le dépôt**
   ```sh
   git clone https://github.com/PierreSchickele/Projet8_GetAround_Analysis.git
   cd Projet8_GetAround_Analysis
   ```

2. **Variables d'environnement**
   - Créez un fichier `.env` dans `getaround/2-dashboard/` avec :
     ```
     PORT=8501
     API_URL=<url_de_votre_api>
     MAPBOX_ACCESS_TOKEN=<votre_token_mapbox>
     ```

3. **Lancer les services en local**
   - Avec Docker :
     ```sh
     docker-compose build
     docker-compose up
     ```
   - Ou manuellement :
     ```sh
     cd getaround/1-api
     docker build -t getaround-api .
     docker run -p 4000:4000 -e PORT=4000 getaround-api
     cd ../2-dashboard
     docker build -t getaround-dash .
     docker run -p 8501:8501 -e PORT=8501 getaround-dash
     ```

## Utilisation

- Accédez au dashboard sur [http://localhost:8501](http://localhost:8501)
- L'API est disponible sur [http://localhost:4000/docs](http://localhost:4000/docs) pour la documentation interactive.

## Déploiement

Des instructions détaillées sont disponibles dans [deploy.txt](deploy.txt).

## Données

- [get_around_delay_analysis.xlsx](get_around_delay_analysis.xlsx) : Analyse des retards.
- [get_around_pricing_project.csv](get_around_pricing_project.csv) : Données pour la prédiction de prix.
