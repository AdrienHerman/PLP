"""
Génération d'une structure lattice à base de losanges
et à gradients d'épaisseur
HERMAN Adrien
10/10/2023
"""

def grad_ep(	ep=0.4,
				doc=None,
				file_debug=None,
				nb_couches=3,
				nb_losange_par_couche=[2,3,2],
				dimlat_par_couche=[40/7*2,40/7*3,40/7*2],
				ep_par_couche=[1,0.5,0.5,1],
				nom_sketch_par_couche=["Sketch_Losange1","Sketch_Losange2","Sketch_Losange3"],
				nom_pad_par_couche=["Pad_Losange1","Pad_Losange2","Pad_Losange3"],
				dimlat_x=40,
				dimlat_ep=40,
				nb_losange_x=[7,4,7],
				nom_sketch_plateaux=["Sketch_Plateaux1","Sketch_Plateaux2","Sketch_Plateaux3","Sketch_Plateaux4"],
				nom_pad_plateaux=["Pad_Plateaux1","Pad_Plateaux2","Pad_Plateaux3","Pad_Plateaux4"],
				nom_body_losange="Body_Losange",
				ep_plateaux=[1,0.5,0.5,1],
				gen_plateaux=None,
				gen_losange=None,
				sketch_visible=False,
				extrude=True,
				semi_debug=False,
				debug=False):
	"""
	Construire un gradient d'épaisseur dans la hauteur du losange
	Couches de losanges d'épaisseur de parois différentes

	-----------
	Variables :
		ep -> Épaisseur de référence pour les parois des différentes couches de la structure lattice
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		file_debug -> Fichier de déboggage (ouvert)
		nb_couches : Nombre de couches différentes à générer
		nb_losange_par_couche : Liste des nombre de losange à générer pour chaque couche
		dimlat_par_couche : Liste des dimensions y de chaque couches
		ep_par_couche : Liste de tous les facteurs d'épaisseur à chaque couche (facteur * ep)
		nom_sketch_par_couche : Liste de tous les noms d'esquisses
		nom_pad_par_couche -> Nom de tous les pad des losanges pour chaque couche
		dimlat_x -> Dimension de la zone de construction
		dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		nb_losange_x -> Nombre de losanges sur la distance x
		nom_sketch_plateaux -> Nom de l'esquisse de définition des plateaux
		nom_body_losange -> Nom de la pièce
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
		gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		extrude -> Réaliser l'extrusion = True
		semi_debug -> Tracer les lignes de construction
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
	-----------
	"""

	if doc == None: FreeCAD.newDocument()						# Création du document
	posy = 0 													# Position y de l'origine des esquisses à créer
	sketches = []												# Liste contenant toutes les esquisses des losanges
	body = doc.addObject('PartDesign::Body', nom_body_losange)	# Créer un body

	for no_couche in range(nb_couches):
		# Création de l'esquisse de la couche
		sketches.append(doc.addObject("Sketcher::SketchObject", nom_sketch_par_couche[no_couche]))
		sketches[no_couche].Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))

		# Génération de la structure sur le couche no_couche
		gen_losange(	ep * ep_par_couche[no_couche],
						doc,
						file_debug,
						nb_losange_x[no_couche],
						nb_losange_par_couche[no_couche],
						dimlat_ep,
						dimlat_x,
						dimlat_par_couche[no_couche],
						0,
						semi_debug,
						debug,
						sketch_visible,
						False,
						nom_sketch_par_couche[no_couche],
						nom_sketch_plateaux[no_couche],
						nom_body_losange,
						nom_pad_par_couche[no_couche],
						nom_pad_plateaux[no_couche],
						None,
						sketches[no_couche])

		# Incrément de la position y dans le repère
		posy += dimlat_par_couche[no_couche]

	# Extrusion des l'esquisses & Génération des plateaux
	if extrude:
		# Extrusion de chaque couches
		for no_couche in range(nb_couches):
			body.newObject('PartDesign::Pad', nom_pad_par_couche[no_couche])									# Créer un Pad
			doc.getObject(nom_pad_par_couche[no_couche]).Profile = sketches[no_couche]							# Mettre l'esquisse dans le pad
			doc.getObject(nom_pad_par_couche[no_couche]).Length = dimlat_ep										# Définir la longueur d'extrustion
			doc.getObject(nom_pad_par_couche[no_couche]).ReferenceAxis = (sketches[no_couche], ['N_Axis'])		# Définir la direction d'extrusion
			doc.recompute()																						# Lancer les calculs
			sketches[no_couche].Visibility = sketch_visible														# Affichage de l'esquisse après l'extrusion
			if file_debug != None and debug:
				wdebug("Extrusion de la structure : Couche no {0}\n".format(no_couche), file_debug)

		# Génération des plateaux liants les extrémités
		gen_plateaux(	nb_couches,
						ep_plateaux,
						dimlat_x,
						dimlat_par_couche,
						dimlat_ep,
						sketch_visible,
						nom_body_losange,
						doc,
						nom_sketch_plateaux,
						nom_pad_plateaux,
						debug,
						file_debug)


if __name__ == "__main__":
	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math, os, sys, time

	# Effacer les consoles Python et la Vue Rapport
	from PySide import QtGui
	mw=Gui.getMainWindow()
	c=mw.findChild(QtGui.QPlainTextEdit, "Python console")
	c.clear()
	r=mw.findChild(QtGui.QTextEdit, "Report view")
	r.clear()

	# Importation des modules du logiciel
	#sys.path.append("C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python")
	#sys.path.append("C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python\Losange")
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/")
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/Losange/")
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/Optimisation Masse/")
	from debug import wdebug
	from debug import edebug
	from debug import create_file_debug
	from losange import gen_losange
	from plateaux_liants import gen_plateaux2
	from export_body import export_body
	from opti_masse import opti_masse
	from opti_masse import affichage_calculs_masse

	"""
	-----------
	Variables :
		ep -> Épaisseur de référence pour les parois des différentes couches de la structure lattice
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		file_debug -> Fichier de déboggage (ouvert)
		nb_couches : Nombre de couches différentes à générer
		nb_losange_par_couche : Liste des nombre de losange à générer pour chaque couche
		dimlat_par_couche_manuel : 	True = Entrée manuelle de épaisseurs de chaques couches
									False = Épaisseur des couches automatique
		dimlat_par_couche : Liste des dimensions y de chaque couches
		ep_par_couche : Liste de tous les facteurs d'épaisseur à chaque couche (facteur * ep)
		nom_sketch_par_couche : Liste de tous les noms d'esquisses
		nom_pad_par_couche -> Nom de tous les pad des losanges pour chaque couche
		dimlat_x -> Dimension de la zone de construction
		dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		nb_losange_x -> Nombre de losanges sur la distance x
		nom_sketch_plateaux -> Nom de l'esquisse de définition des plateaux
		nom_body_losange -> Nom de la pièce
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
		gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		extrude -> Réaliser l'extrusion = True
		semi_debug -> Tracer les lignes de construction
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		debug_current_folder -> Générer le fichier de déboggage dans
			le dossier "debug" du répertoire courrant si True, sinon
			Générer le fichier de déboggae dans le dossier indiqué dans la variable
	-----------
	"""
	# Document
	doc = FreeCAD.newDocument()

	# Déboggage
	semi_debug = False 										# Lignes de construction
	debug = False 											# Messages dans le terminal
	#debug_current_folder = "C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python\log"
	debug_current_folder = "/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/log/"
	file_debug = create_file_debug(debug_current_folder)

	# Paramètres
	#	Dimensions
	ep = 0.4 												# mm
	dimlat_x = 40											# mm
	dimlat_y = 40											# mm
	dimlat_ep = 40											# mm
	nb_losange_par_couche = [4, 4]
	nb_losange_x = [7, 7]
	dimlat_par_couche_manuel = False
	dimlat_par_couche = [13.3, 17.7, 8.8]					# mm
	ep_par_couche = [1, 0.3]					# % de ep
	ep_plateaux = [0.5, 0, 0.5]					# mm
	#	Optimisation de la masse
	objectif_masse = 18										# g
	tolerance = 1e-1										# g
	nb_pas_max = 70	
	correction_ep_par_pas = 1e-4 							# mm
	rho = 1.24												# g/cm^3
	pourcentage_modification_correction = 0.1				# %
	seuil_augmentation_correction = 0.2						# g
	seuil_diminution_correction = 0.2 						# g
	#	Noms des objets
	num_auto_sketch = True
	num_auto_pad = True
	nom_sketch_par_couche = ["Sketch_Losange1","Sketch_Losange2","Sketch_Losange3"]
	nom_pad_par_couche = ["Pad_Losange1","Pad_Losange2","Pad_Losange3"]
	nom_sketch_plateaux = ["Sketch_Plateaux1", "Sketch_Plateaux2", "Sketch_Plateaux3", "Sketch_Plateaux4"]
	nom_pad_plateaux = ["Pad_Plateaux1", "Pad_Plateaux2", "Pad_Plateaux3", "Pad_Plateaux4"]
	nom_body_losange = "Body_Losange"
	#	Options de sortie
	sketch_visible = False
	extrude = True
	export = True
	export_path = "/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/"
	export_name = "/losange"
	#	Auto-Calculé
	nb_couches = len(nb_losange_par_couche)
	if dimlat_par_couche_manuel:
		dimlat_y = 0
		for dimlat in dimlat_par_couche:	dimlat_y += dimlat
	volume_max = dimlat_x * dimlat_y * dimlat_ep * 1e-3
	temps_debut = time.time()

	# 	Génération des dimensions y de chaque couches
	if not dimlat_par_couche_manuel:
		nb_losange_y = 0
		for nb_losange in nb_losange_par_couche:	nb_losange_y += nb_losange
		dimlat_par_couche = [nb_losange_par_couche[i] / nb_losange_y * dimlat_y for i in range(nb_couches)]

	# Nom des esquisses
	if num_auto_sketch:
		nom_sketch_par_couche = ["Sketch_Losange" + str(i + 1) for i in range(nb_couches)]
		nom_sketch_plateaux = ["Sketch_Plateaux" + str(i + 1) for i in range(nb_couches + 1)]

	# Nom des pad
	if num_auto_pad:
		nom_pad_par_couche = ["Pad_Losange" + str(i + 1) for i in range(nb_couches)]
		nom_pad_plateaux = ["Pad_Plateaux" + str(i + 1) for i in range(nb_couches + 1)]

	# Vérification des données utilisateur
	if len(ep_par_couche) != nb_couches:
		edebug("Les paramètres sur les épaisseurs des couches ne sont pas tous / trop définis", file_debug)
	elif len(dimlat_par_couche) != nb_couches:
		edebug("Les paramètres sur les dimensions y des couches ne sont pas tous / trop définis", file_debug)
	elif len(nom_sketch_par_couche) != nb_couches:
		edebug("Les paramètres sur les noms des esquisses des couches ne sont pas tous / trop définis", file_debug)
	elif len(nom_sketch_plateaux) != nb_couches + 1:
		edebug("Les paramètres sur les noms des esquisses des plateaux ne sont pas tous / trop définis", file_debug)
	elif len(nom_pad_plateaux) != nb_couches + 1:
		edebug("Les paramètres sur les noms des pad des plateaux ne sont pas tous / trop définis", file_debug)
	elif len(nom_pad_par_couche) != nb_couches:
		edebug("Les paramètres sur les noms des pad des couches ne sont pas tous / trop définis", file_debug)
	elif len(ep_plateaux) != nb_couches + 1:
		edebug("Les paramètres sur les épaisseur des plateaux ne sont pas tous / trop définis", file_debug)
	else:
		masse, pas_final, ep_finale, porosite = opti_masse(	doc,
															nom_body_losange,
															nom_pad_par_couche,
															nom_pad_plateaux,
															nom_sketch_par_couche,
															nom_sketch_plateaux,
															file_debug,
															grad_ep,
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
															nb_couches,
															nb_losange_par_couche,
															dimlat_par_couche,
															ep_par_couche,
															nom_sketch_par_couche,
															nom_pad_par_couche,
															dimlat_x,
															dimlat_ep,
															nb_losange_x,
															nom_sketch_plateaux,
															nom_pad_plateaux,
															nom_body_losange,
															ep_plateaux,
															gen_plateaux2,
															gen_losange,
															sketch_visible,
															extrude,
															semi_debug,
															debug)

		# Affichage du graphe de convergeance
		affichage_calculs_masse(masse, objectif_masse, tolerance, pas_final, ep_finale, porosite, file_debug)

		# Exportation en step de la pièce
		export_body(doc, nom_body_losange, export, export_path, export_name, debug, file_debug)

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