# smart building data explorer

Projet de préparation, nettoyage et exploration d'un jeu de données Smart Building.

## Objectif

L'objectif de cet atelier est de préparer un jeu de données tabulaires destiné à une future utilisation en Machine Learning.

Le travail porte notamment sur :

* l'exploration des données ;
* le traitement des incohérences ;
* la gestion des valeurs manquantes ;
* la détection et la suppression des doublons ;
* l'analyse des distributions ;
* l'étude des corrélations ;
* la séparation des variables explicatives et de la cible ;
* le preprocessing avec Scikit-learn ;
* l'exportation du dataset nettoyé.

## Organisation

```text
atelier_prepa_donnees_tab/
│
├── notebooks/
│   └── atelier_prepa_donnees_tab.ipynb
├── exports/
│   └── smart_building_cleaned.csv
├── app/
│   └── smart_building_explorer.py
└── README.md
```

## Notebook

Le notebook contient une progression étape par étape + les différentes opérations de préparation des données.

## Smart Building Explorer

Une petite interface graphique Python accompagne le projet.

Elle permet notamment de :

* charger un fichier CSV ;
* consulter rapidement les données ;
* visualiser quelques indicateurs ;
* explorer les variables numériques et catégorielles ;
* visualiser les distributions ;
* consulter les corrélations ;
* basculer entre un mode clair et un mode sombre.

L'application a été conçue comme un **outil complémentaire d'exploration**, indépendant du notebook.

Elle peut également être réutilisée avec d'autres jeux de données tabulaires.

## Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Tkinter
* Jupyter Notebook

## Lancement

Depuis le dossier app/ du projet :

```bash
python smart_building_explorer.py
```

Puis sélectionner un fichier CSV depuis l'interface.

## Résultat

Le dataset nettoyé est exporté dans :

```text
exports/smart_building_cleaned.csv
```
