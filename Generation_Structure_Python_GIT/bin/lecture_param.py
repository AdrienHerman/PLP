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
	generation_plateaux = None
	ep_plateaux = None
	ep = None
	dimlat_ep = None
	dimlat_x = None
	dimlat_y = None
	# 	Géométrie des losanges "basic"
	nb_losange_x_lb = None
	nb_losange_y_lb = None
	nom_pad_losange = None
	nom_sketch_losange = None

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
			if lignes[i][1] == "False":		gen_losange_basic = False
			elif lignes[i][1] == "True":	gen_losange_basic = True
			else:	print("lecture_param\nCommande inconnue pour gen_losange_basic")
		elif lignes[i][0] == "gen_losange_grad":
			if lignes[i][1] == "False":		gen_losange_grad = False
			elif lignes[i][1] == "True":	gen_losange_grad = True
			else:	print("lecture_param\nCommande inconnue pour gen_losange_grad")

		# Géométrie
		if lignes[i][0] == "generation_plateaux":
			if lignes[i][1] == "False":		generation_plateaux = False
			elif lignes[i][1] == "True":	generation_plateaux = True
			else:	print("lecture_param\nCommande inconnue pour generation_plateaux")
		elif lignes[i][0] == "ep_plateaux":
			try:
				ep_plateaux = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans ep_plateaux n'est pas correct !
							\n     ep_plateaux={0}""".format(lignes[i][1]))
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

		# Géométrie des losanges "basic"
		if lignes[i][0] == "nb_losange_x_lb":
			try:
				nb_losange_x_lb = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans nb_losange_x_lb n'est pas correct !
							\n     nb_losange_x_lb={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nb_losange_y_lb":
			try:
				nb_losange_y_lb = float(lignes[i][1])
			except:
				print("""	lecture_param\nLe type de données entrée dans nb_losange_y_lb n'est pas correct !
							\n     nb_losange_y_lb={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nom_pad_losange":
			nom_pad_losange = str(lignes[i][1])
		elif lignes[i][0] == "nom_sketch_losange":
			nom_sketch_losange = str(lignes[i][1])

	# Traitement des données non définies
	return_nok = [False for i in range(13)]	# Liste à retourner si la lecture des parmaètres ne s'est pas terminée correctement
	# 	Traitement du nombre de fonctions de génération
	if gen_func.count(True) > 1:
		print("lecture_param\nIl y a trop de fonctions de génération de strucutres sélectionnées !")
		return return_nok
	elif gen_func.count(True) == 0:
		print("lecture_param\nIl n'y a pas de fonction de génération de strucutres sélectionnées !")
		return return_nok

	# 	Traitement des variables de géométrie générale
	if generation_plateaux == None:
		print("lecture_param\ngeneration_plateaux n'est pas définie !")
		return return_nok
	elif ep_plateaux == None:
		print("lecture_param\nep_plateaux n'est pas définie !")
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

	# 	Traitement des variables concernant la géométrie des losanges "basic"
	if gen_losange_basic == True:
		if nb_losange_x_lb == None:
			print("lecture_param\nnb_losange_x_lb n'est pas définie !")
			return return_nok
		elif nb_losange_y_lb == None:
			print("lecture_param\nnb_losange_y_lb n'est pas définie !")
			return return_nok
		elif nom_pad_losange == None:
			print("lecture_param\nnom_pad_losange n'est pas définie !")
			return return_nok
		elif nom_sketch_losange == None:
			print("lecture_param\nnom_sketch_losange n'est pas définie !")
			return return_nok

	return 	[	True,
				gen_losange_basic,
				gen_losange_grad,
				generation_plateaux,
				ep_plateaux,
				ep,
				dimlat_ep,
				dimlat_x,
				dimlat_y,
				nb_losange_x_lb,
				nb_losange_y_lb,
				nom_pad_losange,
				nom_sketch_losange]