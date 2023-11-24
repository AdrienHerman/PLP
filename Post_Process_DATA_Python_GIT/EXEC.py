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

# Lecture des parmaètres du programme
[	superposer_courbes,
	nom_fichier,
	nom_dossier,
	calc_temps,
	enregistrer_data,
	nom_enregistrement,
	dossier_enregistrement,
	sppr_rollback,
	recherche_deb_impact,
	tarrage_dep,
	tarrage_tmps,
	detect_fin_essai,
	calculer_energie] = lecture_param()

if superposer_courbes != None and superposer_courbes == False:	# Si on affiche qu'un seul fichier de données
	# Lecture du fichier
	lignes = lire_fichier_csv_oscilo(filePath=nom_fichier)
	unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes=lignes)

	# Lecture du contenu du fichier
	F, dep = lire_contenu_csv_oscillo(lignes=lignes)

	# Calcul de temps de l'essai
	if calc_temps != None and calc_temps == True:
		tmps = calc_temps_essai(dep=dep, echantillonage=echantillonage)

	# Suppression du rollback
	if sppr_rollback != None and sppr_rollback == True:
		F, dep, tmps = suppr_rollback(F=F, dep=dep, tmps=tmps)

	# Recherche du début de l'impact
	if recherche_deb_impact != None and recherche_deb_impact == True:
		F, dep, tmps = recherche_debut_impact(F=F, dep=dep, tmps=tmps, taux_agmentation=0.8, nb_pas_avant_agmentation=1, fileName=nom_fichier)
	
	# Tarrage du déplacement et du temps
	if tarrage_dep != None and tarrage_dep == True :	dep = tare_dep(dep=dep)
	if tarrage_tmps != None and tarrage_tmps == True :	tmps = tare_tmps(tmps=tmps)
	
	# Suppression des données après la fin de l'impact
	if detect_fin_essai != None and detect_fin_essai == True:	F, dep, tmps, impact = fin_essai(F=F, dep=dep, tmps=tmps)
	if impact == True:
		impact_text = " / Stop impacteur"
	elif impact == False:
		impact_text = " / Énergie totalement absobée"
	else:
		impact_text = ""

	# Calcul de l'énergie
	if calculer_energie != None and calculer_energie == True:	energie_impact = energie(F=F, dep=dep)

	# Enregistrement des données traitées
	if enregistrer_data != None and enregistrer_data == True:
		enregistrer_donnees(F=F, dep=dep, tmps=tmps, calc_temps=calc_temps, filePath=dossier_enregistrement + nom_enregistrement + ".txt", unite_F=unite_F, unite_dep=unite_dep, echantillonage=echantillonage, date=date, heure=heure)

	# Création des trois graphes dans une figure
	fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
	graphe(data_x=[tmps], data_y=[dep], fig=fig, ax=ax1, label_x="Temps (ms)", label_y="Déplacement (mm)", fileName=[nom_fichier], titre="Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text)
	graphe(data_x=[tmps], data_y=[F], label_x="Temps (ms)", label_y="Force (F)", fig=fig, ax=ax2, fileName=[nom_fichier])
	graphe(data_x=[dep], data_y=[F], label_x="Déplacement (mm)", label_y="Force (F)", fig=fig, ax=ax3, fileName=[nom_fichier])

elif superposer_courbes != None and superposer_courbes == True:	# Si on affiche les fichiers de données d'un dossier
	# Lecture des fichiers
	fichiers = liste_fichier_dossier(path=nom_dossier, fileType=".csv")
	lignes = [lire_fichier_csv_oscilo(filePath=nom_dossier + f) for f in fichiers]
	en_tetes = [lire_en_tete_csv_oscilo(lignes=l) for l in lignes]

	# Lecture des contenus des fichiers
	F = [lire_contenu_csv_oscillo(lignes=l)[0] for l in lignes]
	dep = [lire_contenu_csv_oscillo(lignes=l)[1] for l in lignes]

	# Calcul des temps des essais
	if calc_temps != None and calc_temps == True:
		tmps = [calc_temps_essai(dep=dep[i], echantillonage=en_tetes[i][2]) for i in range(len(dep))]

	# Suppression du rollback
	if sppr_rollback != None and sppr_rollback == True:
		for i in range(len(F)):	F[i], dep[i], tmps[i] = suppr_rollback(F=F[i], dep=dep[i], tmps=tmps[i])

	# Recherche du début de l'impact
	for i in range(len(F)):	F[i], dep[i], tmps[i] = recherche_debut_impact(F=F[i], dep=dep[i], tmps=tmps[i], taux_agmentation=0.7, nb_pas_avant_agmentation=1, fileName=fichiers[i])
	
	# Tarrage du déplacement et du temps
	dep = [tare_dep(dep=d) for d in dep]
	tmps = [tare_tmps(tmps=t) for t in tmps]

	# Suppression des données après la fin de l'impact
	impact = [True for i in range(len(F))]
	for i in range(len(F)):	F[i], dep[i], tmps[i], impact[i] = fin_essai(F=F[i], dep=dep[i], tmps=tmps[i])
	if True in impact and False in impact:
		impact_text = str(impact.count(True)) + " stop impacteur & " + str(impact.count(False)) + " totalement absobées"
	elif True in impact:
		impact_text = "Stop impacteur"
	else:
		impact_text = "Énergie totalement absobée"

	# Calcul de l'énergie de chaque courbes
	energie_impact = [energie(F=F[i], dep=dep[i]) for i in range(len(F))]
	energie_moyenne = 0
	for e in energie_impact:	energie_moyenne += e
	energie_moyenne /= len(energie_impact)

	# Enregistrement des données traitées
	if enregistrer_data != None and enregistrer_data == True:
		fichiers_enregistrement = []
		for i in range(len(fichiers)):	fichiers_enregistrement.append(fichiers[i].split(".")[0])
		for i in range(len(F)):	enregistrer_donnees(F=F[i], dep=dep[i], tmps=tmps[i], calc_temps=calc_temps, filePath=dossier_enregistrement + fichiers_enregistrement[i] + ".txt", unite_F=en_tetes[i][0], unite_dep=en_tetes[i][1], echantillonage=en_tetes[i][2], date=en_tetes[i][3], heure=en_tetes[i][4])

	# Création des trois graphes dans une figure
	fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
	graphe(data_x=tmps, data_y=dep, fig=fig, ax=ax1, label_x="Temps (ms)", label_y="Déplacement (mm)", fileName=fichiers, titre="Énergie Moyenne Calculée = " + str(round(energie_moyenne, 2)) + " J / " + impact_text)
	graphe(data_x=tmps, data_y=F, label_x="Temps (ms)", label_y="Force (F)", fig=fig, ax=ax2, fileName=fichiers)
	graphe(data_x=dep, data_y=F, label_x="Déplacement (mm)", label_y="Force (F)", fig=fig, ax=ax3, fileName=fichiers)

try:
	plt.subplots_adjust(left=0.075, right=0.975, top=0.94, bottom=0.08, hspace=0.36, wspace=0.2)
	fig.set_figheight(6)
	fig.set_figwidth(10)
	plt.show()
except:
	print("Impossible de redimensionner et/ou d'afficher le graphique !")