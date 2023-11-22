"""
Corps principal
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import matplotlib.pyplot as plt

# Modules du Logiciel
from bin.lecture_param import *
from bin.lecture_ecriture_donnees import *
from bin.afficher_data import *
from bin.traitement_data import *

superposer_courbes, nom_fichier, nom_dossier, calc_temps, enregistrer_data, nom_enregistrement, dossier_enregistrement = lecture_param()
lignes = lire_fichier_csv_oscilo(nom_fichier)
unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes)
F, dep = lire_contenu_csv_oscillo(lignes)
tmps = calc_temps_essai(dep, echantillonage)
F, dep, tmps = suppr_rollback(F, dep, tmps)
F, dep, tmps = recherche_debut_impact(F=F, dep=dep, tmps=tmps, taux_agmentation=0.5, nb_pas_avant_agmentation=1, fileName=nom_fichier)
dep = tare_dep(dep)
tmps = tare_tmps(tmps)
F, dep, tmps, impact = fin_essai(F=F, dep=dep, tmps=tmps)
energie_impact = energie(F=F, dep=dep)
enregistrer_donnees(F=F, dep=dep, tmps=tmps, calc_temps=calc_temps, filePath=dossier_enregistrement + nom_enregistrement + ".txt", unite_F=unite_F, unite_dep=unite_dep, echantillonage=echantillonage, date=date, heure=heure)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
graphe(data_x=[tmps], data_y=[dep], fig=fig, ax=ax1, label_x="Temps (ms)", label_y="Déplacement (mm)", fileName=[nom_fichier], titre="Énergie Calculée = " + str(round(energie_impact, 2)) + " J / Impact sur les tampons : " + str(impact))
graphe(data_x=[tmps], data_y=[F], label_x="Temps (ms)", label_y="Force (F)", fig=fig, ax=ax2, fileName=[nom_fichier])
graphe(data_x=[dep], data_y=[F], label_x="Déplacement (mm)", label_y="Force (F)", fig=fig, ax=ax3, fileName=[nom_fichier])
plt.subplots_adjust(left=0.075, right=0.975, top=0.94, bottom=0.08, hspace=0.36, wspace=0.2)
fig.set_figheight(6)
fig.set_figwidth(10)
plt.show()