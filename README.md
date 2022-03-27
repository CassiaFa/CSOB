# CSOB - Analyse de données

## Description

Projet réalisé dans le cadre de la formation Microsoft IA x Simplon - Brest +.

Ce projet consiste dans l'analyse statistique d'un jeu de données, ainsi que dans la création d'une base de données associée. L'organisation du projet est la suivante :

```
.
│   .gitignore
│   backup_bdd_vente_jeux.sql
│   Cahier_des_charges.pdf
│   connexion.py
│   Preparation_donnees_bdd.ipynb
│   README.md
│   Statistique.ipynb
│   vgsales.csv
│
├───CDC_latex
│   │   main.tex
│   │
│   └───Image
│       └───logo
│               logo_Isen.png
│               logo_microsoft.jpg
│               logo_simplon.png
│
├───CSV_2DB
│       annees.csv
│       consoles.csv
│       editeurs.csv
│       genres.csv
│       jeux.csv
│
└───mocodo_notebook
        sandbox.html
        sandbox.mcd
        sandbox.mld
        sandbox.svg
        sandbox_data_dict.md
        sandbox_mysql.sql
        sandbox_svg.py

```

On retrouve au premier niveau les 2 jupyter notebook, *Preparation_donnees_bdd* et *Satistique*, qui permettent respectivement de créer la base de données et de faire les statistiques. Le jeu de données utilisé *vgsales*, ainsi que le backup de la base de données, et le cahier des charges. Le fichier *README.md* contient une description du projet, et le fichier *Connexion* est le fichier qui permet la connexion à la base de données à partir de python.

Le dossier *mocodo_notebook* contient les fichiers nécessaires à la création du MCD et du MLD.

Le dossier *CDC_latex* contient le fichier *main.tex* qui permet de générer le cahier des charges.

Le dossier *CSV_2DB* contient les fichiers *annees.csv*, *consoles.csv*, *editeurs.csv*, *genres.csv*, *jeux.csv* qui contiennent les données du jeu de données, pour la création de la base de données.