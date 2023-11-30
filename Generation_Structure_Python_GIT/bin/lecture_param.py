"""
Lecture des paramètres
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import os

def lecture_param(path_config="config.txt"):
	"""
	Lecture des paramètres

	-----------
	Variables :
		- path_config : Chemin vers le fichier de configuration
	-----------
	"""

	# Récupération du dossier contenant le fichier
	path = path_config.split("/")
	del path[len(path) - 1]
	path = '/'.join(path)

	if path != "":
		if not (path_config.split("/")[len(path_config.split("/")) - 1] in os.listdir(path)):
			print("lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}".format(path_config))

			return []
	else:
		if not (path_config in os.listdir()):
			print("lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}".format(path_config))

			return []

	# Variables
	# ATTENTION : À l'ajout de variable, ne pas oublier d'actualiser
	# le nombre de variables à retourner !
	#	Fonctions de génération
	gen_losange_basic = None
	gen_losange_grad = None
	gen_func = [None for i in range(2)]
	#	Géométrie générale
	generation_plateaux_extremitees = None
	ep_plateaux_extremitees = None
	ep = None
	dimlat_ep = None
	dimlat_x = None
	dimlat_y = None
	# 	Partie optimisation de la masse
	optimisation_masse = None
	objectif_masse = None
	tolerance = None
	nb_pas_max = None
	correction_ep_par_pas = None
	pourcentage_modification_correction = None
	seuil_augmentation_correction = None
	seuil_diminution_correction = None
	rho = None
	# 	Géométrie des losanges "basic"
	nb_losange_x_lb = None
	nb_losange_y_lb = None
	nom_pad_losange_basic = None
	nom_sketch_losange_basic = None
	#	Partie exploitation du modèle 3D
	extrude = None 
	export = None 
	export_name = None 
	export_path = None 
	sketch_visible = None
	# 	Partie noms des objets
	nom_body_losange = None
	nom_sketch_plateaux = None
	nom_pad_plateaux = None
	# 	Partie Débogage
	semi_debug = None 
	debug = None 
	debug_current_folder = None

	# Stockage des données
	file = open(path_config, "r")
	lignes = file.readlines()
	file.close()

	# Parsing des données
	for i in range(len(lignes)):
		lignes[i] = lignes[i].split(":")

	# Traitement des données
	for i in range(len(lignes)):
		# Commentaire
		if lignes[i][0] == "#":	continue
		
		# Fonctions de génération des structures
		if lignes[i][0] == "gen_losange_basic":
			if lignes[i][1] == "False":
				gen_losange_basic = False
				gen_func[0] = False
			elif lignes[i][1] == "True":
				gen_losange_basic = True
				gen_func[0] = True
			else:	print("lecture_param\nCommande inconnue pour gen_losange_basic")
		elif lignes[i][0] == "gen_losange_grad":
			if lignes[i][1] == "False":
				gen_losange_grad = False
				gen_func[1] = False
			elif lignes[i][1] == "True":
				gen_losange_grad = True
				gen_func[1] = True
			else:	print("lecture_param\nCommande inconnue pour gen_losange_grad")

		# Géométrie
		if lignes[i][0] == "generation_plateaux_extremitees":
			if lignes[i][1] == "False":		generation_plateaux_extremitees = False
			elif lignes[i][1] == "True":	generation_plateaux_extremitees = True
			else:	print("lecture_param\nCommande inconnue pour generation_plateaux_extremitees")
		elif lignes[i][0] == "ep_plateaux_extremite":
			try:
				ep_plateaux_extremitees = [float(lignes[i][1].split(",")[j]) for j in range(len(lignes[i][1].split(",")))]
			except:
				print("""	lecture_param\nLe type de données entrée dans ep_plateaux_extremitees n'est pas correct !
							\n     ep_plateaux_extremitees
		={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "ep":
			try:
				ep = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans ep n'est pas correct !
							\n     ep={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "dimlat_ep":
			try:
				dimlat_ep = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans dimlat_ep n'est pas correct !
							\n     dimlat_ep={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "dimlat_x":
			try:
				dimlat_x = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans dimlat_x n'est pas correct !
							\n     dimlat_x={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "dimlat_y":
			try:
				dimlat_y = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans dimlat_y n'est pas correct !
							\n     dimlat_y={0}""".format(lignes[i][1]))

		# Partie optimisation de la masse
		if lignes[i][0] == "optimisation_masse":
			if lignes[i][1] == "False":		optimisation_masse = False
			elif lignes[i][1] == "True":	optimisation_masse = True
			else:	print("lecture_param\nCommande inconnue pour optimisation_masse")
		elif lignes[i][0] == "objectif_masse":
			try:
				objectif_masse = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans objectif_masse n'est pas correct !
							\n     objectif_masse={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "tolerance":
			try:
				tolerance = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans tolerance n'est pas correct !
							\n     tolerance={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nb_pas_max":
			try:
				nb_pas_max = int(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans nb_pas_max n'est pas correct !
							\n     nb_pas_max={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "correction_ep_par_pas":
			try:
				correction_ep_par_pas = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans correction_ep_par_pas n'est pas correct !
							\n     correction_ep_par_pas={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "pourcentage_modification_correction":
			try:
				pourcentage_modification_correction = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans pourcentage_modification_correction n'est pas correct !
							\n     pourcentage_modification_correction={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "seuil_augmentation_correction":
			try:
				seuil_augmentation_correction = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans seuil_augmentation_correction n'est pas correct !
							\n     seuil_augmentation_correction={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "seuil_diminution_correction":
			try:
				seuil_diminution_correction = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans seuil_diminution_correction n'est pas correct !
							\n     seuil_diminution_correction={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "rho":
			try:
				rho = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans rho n'est pas correct !
							\n     rho={0}""".format(lignes[i][1]))

		# Géométrie des losanges "basic"
		if lignes[i][0] == "nb_losange_x_lb":
			try:
				nb_losange_x_lb = int(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans nb_losange_x_lb n'est pas correct !
							\n     nb_losange_x_lb={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nb_losange_y_lb":
			try:
				nb_losange_y_lb = int(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans nb_losange_y_lb n'est pas correct !
							\n     nb_losange_y_lb={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nom_pad_losange_basic":
			nom_pad_losange_basic = str(lignes[i][1])
		elif lignes[i][0] == "nom_sketch_losange_basic":
			nom_sketch_losange_basic = str(lignes[i][1])

		# Partie exploitation du modèle 3D
		if lignes[i][0] == "extrude":
			if lignes[i][1] == "False":		extrude = False
			elif lignes[i][1] == "True":	extrude = True
			else:	print("lecture_param\nCommande inconnue pour extrude")
		elif lignes[i][0] == "export":
			if lignes[i][1] == "False":		export = False
			elif lignes[i][1] == "True":	export = True
			else:	print("lecture_param\nCommande inconnue pour export")
		elif lignes[i][0] == "export_name":
			export_name = str(lignes[i][1])
		elif lignes[i][0] == "export_path":
			export_path = str(lignes[i][1])
		elif lignes[i][0] == "sketch_visible":
			if lignes[i][1] == "False":		sketch_visible = False
			elif lignes[i][1] == "True":	sketch_visible = True
			else:	print("lecture_param\nCommande inconnue pour sketch_visible")

		# Partie noms des objets
		if lignes[i][0] == "nom_body_losange":
			nom_body_losange = str(lignes[i][1])
		elif lignes[i][0] == "nom_sketch_plateaux":
			nom_sketch_plateaux = str(lignes[i][1])
		elif lignes[i][0] == "nom_pad_plateaux":
			nom_pad_plateaux = str(lignes[i][1])

		# Partie Débogage
		if lignes[i][0] == "semi_debug":
			if lignes[i][1] == "False":		semi_debug = False
			elif lignes[i][1] == "True":	semi_debug = True
			else:	print("lecture_param\nCommande inconnue pour semi_debug")
		elif lignes[i][0] == "debug":
			if lignes[i][1] == "False":		debug = False
			elif lignes[i][1] == "True":	debug = True
			else:	print("lecture_param\nCommande inconnue pour debug")
		elif lignes[i][0] == "debug_current_folder":
			debug_current_folder = str(lignes[i][1])

	# Traitement des données non définies
	return_ok = [	True,
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
				nom_pad_losange_basic,
				nom_sketch_losange_basic,
				extrude,
				export,
				export_name,
				export_path,
				sketch_visible,
				nom_body_losange,
				nom_sketch_plateaux,
				nom_pad_plateaux,
				semi_debug,
				debug,
				debug_current_folder]
	return_nok = [False for i in range(len(return_ok))]	# Liste à retourner si la lecture des parmaètres ne s'est pas terminée correctement

	# 	Traitement du nombre de fonctions de génération
	if gen_func.count(True) > 1:
		print("lecture_param\nIl y a trop de fonctions de génération de strucutres sélectionnées !")
		return return_nok
	elif gen_func.count(True) == 0:
		print("lecture_param\nIl n'y a pas de fonction de génération de strucutres sélectionnées !")
		return return_nok

	# 	Traitement des variables de géométrie générale
	if generation_plateaux_extremitees == None:
		print("lecture_param\ngeneration_plateaux_extremitees n'est pas définie !")
		return return_nok
	elif ep_plateaux_extremitees == None:
		print("lecture_param\nep_plateaux_extremite n'est pas définie !")
		return return_nok
	elif ep == None:
		print("lecture_param\nep n'est pas définie !")
		return return_nok
	elif dimlat_ep == None:
		print("lecture_param\ndimlat_ep n'est pas définie !")
		return return_nok
	elif dimlat_x == None:
		print("lecture_param\ndimlat_x n'est pas définie !")
		return return_nok
	elif dimlat_y == None:
		print("lecture_param\ndimlat_y n'est pas définie !")
		return return_nok

	# Partie optimisation de la masse
	if optimisation_masse == None:
		print("lecture_param\noptimisation_masse n'est pas définie !")
		return return_nok
	elif objectif_masse == None:
		print("lecture_param\nobjectif_masse n'est pas définie !")
		return return_nok
	elif tolerance == None:
		print("lecture_param\ntolerance n'est pas définie !")
		return return_nok
	elif correction_ep_par_pas == None:
		print("lecture_param\ncorrection_ep_par_pas n'est pas définie !")
		return return_nok
	elif pourcentage_modification_correction == None:
		print("lecture_param\npourcentage_modification_correction n'est pas définie !")
		return return_nok
	elif seuil_augmentation_correction == None:
		print("lecture_param\nseuil_augmentation_correction n'est pas définie !")
		return return_nok
	elif seuil_diminution_correction == None:
		print("lecture_param\nseuil_diminution_correction n'est pas définie !")
		return return_nok
	elif rho == None:
		print("lecture_param\nrho n'est pas définie !")
		return return_nok

	# 	Traitement des variables concernant la géométrie des losanges "basic"
	if gen_losange_basic == True:
		if nb_losange_x_lb == None:
			print("lecture_param\nnb_losange_x_lb n'est pas définie !")
			return return_nok
		elif nb_losange_y_lb == None:
			print("lecture_param\nnb_losange_y_lb n'est pas définie !")
			return return_nok
		elif nom_pad_losange_basic == None:
			print("lecture_param\nnom_pad_losange_basic n'est pas définie !")
			return return_nok
		elif nom_sketch_losange_basic == None:
			print("lecture_param\nnom_sketch_losange_basic n'est pas définie !")
			return return_nok
	
	# Partie exploitation du modèle 3D
	if extrude == None:
		print("lecture_param\nextrude n'est pas définie !")
		return return_nok
	elif export == None:
		print("lecture_param\nexport n'est pas définie !")
		return return_nok
	elif export_name == None:
		print("lecture_param\nexport_name n'est pas définie !")
		return return_nok
	elif export_path == None:
		print("lecture_param\nexport_path n'est pas définie !")
		return return_nok
	elif sketch_visible == None:
		print("lecture_param\nsketch_visible n'est pas définie !")
		return return_nok

	# Partie noms des objets
	if nom_body_losange == None:
		print("lecture_param\nnom_body_losange n'est pas définie !")
		return return_nok
	elif nom_sketch_plateaux == None:
		print("lecture_param\nnom_sketch_plateaux n'est pas définie !")
		return return_nok
	elif nom_pad_plateaux == None:
		print("lecture_param\nnom_pad_plateaux n'est pas définie !")
		return return_nok

	# Partie Débogage
	if semi_debug == None:
		print("lecture_param\nsemi_debug n'est pas définie !")
		return return_nok
	elif debug == None:
		print("lecture_param\ndebug n'est pas définie !")
		return return_nok
	elif debug_current_folder == None:
		print("lecture_param\ndebug_current_folder n'est pas définie !")
		return return_nok

	return 	return_ok