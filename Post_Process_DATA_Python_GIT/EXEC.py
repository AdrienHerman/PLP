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
	dep_max,
	calculer_energie,
	fact_force,
	fact_dep,
	taux_augmentation,
	nb_pas_avant_augmentation,
	afficher_dep_tmps,
	afficher_F_tmps,
	afficher_F_dep,
	afficher_sep] = lecture_param()

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
	if recherche_deb_impact != None and taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact == True:
		F, dep, tmps = recherche_debut_impact(	F=F,
												dep=dep,
												tmps=tmps,
												taux_augmentation=taux_augmentation,
												nb_pas_avant_augmentation=nb_pas_avant_augmentation,
												fileName=nom_fichier)
	elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact == True:
		print("La vairiable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")

	# Tarrage du déplacement et du temps
	if tarrage_dep != None and tarrage_dep == True and recherche_deb_impact == True:
		dep = tare_dep(dep=dep)
	if tarrage_tmps != None and tarrage_tmps == True and recherche_deb_impact == True:
		tmps = tare_tmps(tmps=tmps)
	
	# Suppression des données après la fin de l'impact
	impact_text = ""

	if detect_fin_essai != None and detect_fin_essai == True and sppr_rollback == True and recherche_deb_impact == True and tarrage_dep == True:
		F, dep, tmps, impact = fin_essai(F=F, dep=dep, tmps=tmps)

		if impact == True:
			impact_text = " / Stop impacteur"
		elif impact == False:
			impact_text = " / Énergie totalement absobée"

	elif sppr_rollback != True or recherche_deb_impact != True or tarrage_dep != True:
		print("Les paramètres sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")

	# Calcul de l'énergie
	if calculer_energie != None and calculer_energie == True:
		energie_impact = energie(F=F, dep=dep, fact_force=fact_force, fact_dep=fact_dep)

	# Enregistrement des données traitées
	if enregistrer_data != None and enregistrer_data == True:
		enregistrer_donnees(	F=F,
								dep=dep,
								tmps=tmps,
								calc_temps=calc_temps,
								filePath=dossier_enregistrement + nom_enregistrement + ".txt",
								unite_F=unite_F,
								unite_dep=unite_dep,
								echantillonage=echantillonage,
								date=date,
								heure=heure)

	# Création des trois graphes dans une figure
	if afficher_sep != None and afficher_sep == True:
		figs = [0, 0, 0]
		axs = [0, 0, 0]

		for i in range([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True)):
			figs[i], axs[i] = plt.subplots()

	elif afficher_sep != None and afficher_sep == False:
		fig, axs = plt.subplots([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True), 1)

	if afficher_sep != None:
		i = 0

		if afficher_dep_tmps != None and afficher_dep_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			if calculer_energie:
				titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text
			else:
				titre = "Énergie Calculée = Désactivé" + impact_text

			graphe(	data_x=[tmps],
					data_y=[dep],
					fig=fig,
					ax=ax,
					label_x="Temps (ms)",
					label_y="Déplacement (mm)",
					fileName=[nom_fichier],
					titre=titre)
			i += 1

		if afficher_F_tmps != None and afficher_F_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			if afficher_dep_tmps == None or afficher_dep_tmps == False:
				if calculer_energie:
					titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text
				else:
					titre = "Énergie Calculée = Désactivé" + impact_text

			graphe(	data_x=[tmps],
					data_y=[F],
					label_x="Temps (ms)",
					label_y="Force (F)",
					titre=titre,
					fig=fig,
					ax=ax,
					fileName=[nom_fichier])
			i += 1

		if afficher_F_dep != None and afficher_F_dep == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			if (afficher_dep_tmps == None or afficher_dep_tmps == False) and (afficher_F_tmps == None or afficher_F_tmps == False):
				if calculer_energie:
					titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text
				else:
					titre = "Énergie Calculée = Désactivé" + impact_text

			graphe(	data_x=[dep],
					data_y=[F],
					label_x="Déplacement (mm)",
					label_y="Force (F)",
					titre=titre,
					fig=fig,
					ax=ax,
					fileName=[nom_fichier])

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
	if recherche_deb_impact != None and taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact == True:
		for i in range(len(F)):
			F[i], dep[i], tmps[i] = recherche_debut_impact(	F=F[i],
															dep=dep[i],
															tmps=tmps[i],
															taux_augmentation=taux_augmentation,
															nb_pas_avant_augmentation=nb_pas_avant_augmentation,
															fileName=fichiers[i])
	elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact == True:
		print("La vairiable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")

	# Tarrage du déplacement et du temps
	if tarrage_dep != None and tarrage_dep == True and recherche_deb_impact == True:
		dep = [tare_dep(dep=d) for d in dep]
	
	if tarrage_tmps != None and tarrage_tmps == True and recherche_deb_impact == True:
		tmps = [tare_tmps(tmps=t) for t in tmps]

	# Suppression des données après la fin de l'impact
	impact_text = ""

	if detect_fin_essai != None and detect_fin_essai == True and sppr_rollback == True and recherche_deb_impact == True and tarrage_dep == True:
		impact = [True for i in range(len(F))]
		for i in range(len(F)):
			F[i], dep[i], tmps[i], impact[i] = fin_essai(	F=F[i],
															dep=dep[i],
															tmps=tmps[i])
		
		if True in impact and False in impact:
			impact_text = " / " + str(impact.count(True)) + " stop impacteur & " + str(impact.count(False)) + " totalement absobées"
		elif True in impact:
			impact_text = " / Stop impacteur"
		else:
			impact_text = " / Énergie totalement absobée"

	elif sppr_rollback != True or recherche_deb_impact != True or tarrage_dep != True:
		print("Les paramètres sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")

	# Calcul de l'énergie de chaque courbes
	if calculer_energie != None and calculer_energie == True:
		energie_impact = [energie(	F=F[i],
									dep=dep[i],
									fact_force=fact_force,
									fact_dep=fact_dep) for i in range(len(F))]
		energie_moyenne = 0
		for e in energie_impact:	energie_moyenne += e
		energie_moyenne /= len(energie_impact)

	# Enregistrement des données traitées
	if enregistrer_data != None and enregistrer_data == True:
		fichiers_enregistrement = []
		for i in range(len(fichiers)):
			fichiers_enregistrement.append(fichiers[i].split(".")[0])

		for i in range(len(F)):
			enregistrer_donnees(F=F[i],
								dep=dep[i],
								tmps=tmps[i],
								calc_temps=calc_temps,
								filePath=dossier_enregistrement + fichiers_enregistrement[i] + ".txt",
								unite_F=en_tetes[i][0],
								unite_dep=en_tetes[i][1],
								echantillonage=en_tetes[i][2],
								date=en_tetes[i][3],
								heure=en_tetes[i][4])

	# Création des trois graphes dans une figure

	if afficher_sep != None and afficher_sep == True:
		figs = [0, 0, 0]
		axs = [0, 0, 0]

		for i in range([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True)):
			figs[i], axs[i] = plt.subplots()

	elif afficher_sep != None and afficher_sep == False:
		fig, axs = plt.subplots([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True), 1)

	if afficher_sep != None:
		i = 0

		if afficher_dep_tmps != None and afficher_dep_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
				titre = "Énergie Moyenne Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			graphe(	data_x=tmps,
					data_y=dep,
					fig=fig,
					ax=ax,
					label_x="Temps (ms)",
					label_y="Déplacement (mm)",
					fileName=[nom_fichier],
					titre=titre)
			i += 1

		if afficher_F_tmps != None and afficher_F_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]

				if afficher_dep_tmps == None or afficher_dep_tmps == False:
					titre = "Énergie Moyenne Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text
				else:
					titre = ""
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			graphe(	data_x=tmps,
					data_y=F,
					label_x="Temps (ms)",
					label_y="Force (F)",
					titre=titre,
					fig=fig,
					ax=ax,
					fileName=[nom_fichier])
			i += 1

		if afficher_F_dep != None and afficher_F_dep == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]

				if (afficher_dep_tmps == None or afficher_dep_tmps == False) and (afficher_F_tmps == None or afficher_F_tmps == False):
					titre = "Énergie Moyenne Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text
				else:
					titre = ""
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			graphe(	data_x=dep,
					data_y=F,
					label_x="Déplacement (mm)",
					label_y="Force (F)",
					titre=titre,
					fig=fig,
					ax=ax,
					fileName=[nom_fichier])

try:
	if afficher_sep != None:
		i = 0

		if afficher_dep_tmps != None and afficher_dep_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			fig.set_figheight(6)
			fig.set_figwidth(10)

			i += 1

		if afficher_F_tmps != None and afficher_F_tmps == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			fig.set_figheight(6)
			fig.set_figwidth(10)

			i += 1

		if afficher_F_dep != None and afficher_F_dep == True:
			if afficher_sep == True:
				fig = figs[i]
				ax = axs[i]
			else:
				if type(axs) == tuple:
					ax = axs[i]
				else:
					ax = axs

			fig.set_figheight(6)
			fig.set_figwidth(10)

	if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) != 0:
		plt.subplots_adjust(left=0.075, right=0.975, top=0.94, bottom=0.08, hspace=0.36, wspace=0.2)
		plt.show()

except:
	print("Impossible de redimensionner et/ou d'afficher le graphique !")