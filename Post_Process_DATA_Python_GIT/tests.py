"""
Corps principal
HERMAN Adrien
21/11/2023
"""

# Modules de Python

# Modules du Logiciel
from lecture_param import lecture_param
from lecture_ecriture_donnees import *


superposer_courbes, nom_fichier, nom_dossier, calc_temps, enregistrer_donnees, nom_enregistrement = lecture_param()
lignes = lire_fichier_csv_oscilo(nom_fichier)
unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes)
print(unite_F, unite_dep, echantillonage, date, heure)