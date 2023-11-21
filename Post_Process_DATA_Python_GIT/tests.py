"""
Corps principal
HERMAN Adrien
21/11/2023
"""

# Modules du Logiciel
from lecture_param import *
from lecture_ecriture_donnees import *
from afficher_data import *
from traitement_data import *

superposer_courbes, nom_fichier, nom_dossier, calc_temps, enregistrer_data, nom_enregistrement, dossier_enregistrement = lecture_param()
lignes = lire_fichier_csv_oscilo(nom_fichier)
unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes)
F, dep = lire_contenu_csv_oscillo(lignes)
tmps = calc_temps_essai(dep, echantillonage)
F, dep, tmps = suppr_rollback(F, dep, tmps)
enregistrer_donnees(F=F, dep=dep, tmps=tmps, calc_temps=calc_temps, filePath=dossier_enregistrement + nom_enregistrement + ".txt", unite_F=unite_F, unite_dep=unite_dep, echantillonage=echantillonage, date=date, heure=heure)

plt = graphe([tmps], [dep], "Temps (ms)", "Déplacement (mm)", xlim_inf=0, xlim_sup=1)
if plt != None:	plt.show()

plt = graphe([tmps], [F], "Temps (ms)", "Force (F)", xlim_inf=0, xlim_sup=1)
if plt != None:	plt.show()

plt = graphe([dep], [F], "Déplacement (mm)", "Force (F)")
if plt != None:	plt.show()