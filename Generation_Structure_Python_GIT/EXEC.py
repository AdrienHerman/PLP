"""
Fichier d'exécution du code de génération des structures
HERMAN Adrien
29/11/2023
"""

# Modules de Python
import FreeCAD as App
from PySide import QtGui
import FreeCADGui, ImportGui, Part, Sketcher, math, os, sys, time

# Modules du Logiciel
path_soft = "/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Python/dev/Generation_Structure_Python_GIT/"
sys.path.append(path_soft + "bin/")
sys.path.append(path_soft + "bin/losange/")
from lecture_param import *
from plateaux_liants import *
from export_body import *
from opti_masse import *
from debug import *
from losange.losange import *

# Lecture des parmaètres du programme
[	lecture_param_ok,
	gen_losange_basic,
	gen_losange_grad,
	generation_plateaux_extremitees,
	ep_plateaux_extremitees,
	ep,
	dimlat_ep,
	dimlat_x,
	dimlat_y,
	optimisation_masse,
	objectif_masse,
	tolerance,
	nb_pas_max,
	correction_ep_par_pas,
	pourcentage_modification_correction,
	seuil_augmentation_correction,
	seuil_diminution_correction,
	rho,
	nb_losange_x_lb,
	nb_losange_y_lb,
	extrude,
	export,
	export_name,
	export_path,
	sketch_visible,
	semi_debug,
	debug,
	debug_current_folder] = lecture_param(path_soft + "config.txt")

if lecture_param_ok:
	# Effacer les consoles Python et la Vue Rapport
	mw=Gui.getMainWindow()
	c=mw.findChild(QtGui.QPlainTextEdit, "Python console")
	c.clear()
	r=mw.findChild(QtGui.QTextEdit, "Report view")
	r.clear()

	# Initialisation des variables
	volume_max = dimlat_x * dimlat_y * dimlat_ep * 1e-3					# Volume maximal calculé (cm^3)
	temps_debut = time.time()											# Calcul de la durée d'exécution
	doc = FreeCAD.newDocument()											# Création d'un nouveau document FreeCAD
	file_debug = create_file_debug(path_soft + debug_current_folder)	# Création du fichier de débogage

	if gen_losange_basic:
		masse, pas_final, ep_finale, porosite = opti_masse(	
				doc,
				"Body_Losange",
				"Pad_Losange",
				["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
				"Sketch_Losange",
				["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
				gen_losange,
				file_debug,
				wdebug,
				debug,
				tolerance,
				nb_pas_max,
				[0 for i in range(nb_pas_max)],
				ep,
				0,
				correction_ep_par_pas,
				pourcentage_modification_correction,
				seuil_augmentation_correction,
				seuil_diminution_correction,
				objectif_masse,
				rho,
				volume_max,
				nb_losange_x_lb,
				nb_losange_y_lb,
				dimlat_ep,
				dimlat_x,
				dimlat_y,
				ep_plateaux_extremitees,
				semi_debug,
				debug,
				sketch_visible,
				extrude,
				"Sketch_Losange",
				["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
				"Body_Losange",
				"Pad_Losange",
				["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
				gen_plateaux,
				generation_plateaux_extremitees,
				export_body,
				wdebug)

	elif gen_losange_grad:
		pass

	# Affichage du graphe de convergeance
	affichage_calculs_masse(masse, objectif_masse, tolerance, pas_final, ep_finale, porosite, file_debug)

	# Exportation en step de la pièce
	export_body(doc, "Body_Losange", export, path_soft + export_path, export_name, debug, wdebug, file_debug)

	# Fin du programme
	wdebug("\n\n---------------------\n", file_debug)
	wdebug("--- Fin Programme ---\n", file_debug)
	wdebug("---------------------\n", file_debug)

	# Calcul de la durée d'exécution
	temps_fin = time.time()
	duree_exec = temps_fin - temps_debut
	if duree_exec >= 60:	# Conversion en minute si nécessaire
		duree_exec_min = int(duree_exec / 60)
		duree_exec_sec = round(duree_exec % 60, 0)
		wdebug("Temps d'exécution: {0}min {1}s\n".format(duree_exec_min, duree_exec_sec), file_debug)
	else:
		wdebug("Temps d'exécution: {0}s\n".format(round(duree_exec, 0)), file_debug)

	# Fermeture du fichier de déboggage
	if file_debug != None and debug:
		file_debug.close()

else:
	print("La lecture des paramètres ne s'est pas terminée correctement !")