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
	superposer_courbes = None
	nom_fichier = None
	nom_dossier = None
	calc_temps = None
	enregistrer_data = None
	nom_enregistrement = None
	dossier_enregistrement = None

	# Stockage des données
	file = open(path_config, "r")
	lignes = file.readlines()
	file.close()

	# Parsing des données
	for i in range(len(lignes)):
		lignes[i] = lignes[i].split(":")

	# Traitement des données
	for i in range(len(lignes)):
		if lignes[i][0] == "#":	continue
		
		if lignes[i][0] == "superposer_courbes":
			if lignes[i][1] == "False":		superposer_courbes = False
			elif lignes[i][1] == "True":	superposer_courbes = True
			else:	print("lecture_param\nCommande inconnue pour superposer_courbes")
		elif lignes[i][0] == "nom_fichier":
			nom_fichier = lignes[i][1]
		elif lignes[i][0] == "nom_dossier":
			nom_dossier = lignes[i][1]
		elif lignes[i][0] == "calc_temps":
			if lignes[i][1] == "False":		calc_temps = False
			elif lignes[i][1] == "True":	calc_temps = True
			else:	print("lecture_param\nCommande inconnue pour calc_temps")
		elif lignes[i][0] == "enregistrer_data":
			if lignes[i][1] == "False":		enregistrer_data = False
			elif lignes[i][1] == "True":	enregistrer_data = True
			else:	print("lecture_param\nCommande inconnue pour enregistrer_data")
		elif lignes[i][0] == "nom_enregistrement":
			nom_enregistrement = lignes[i][1]
		elif lignes[i][0] == "dossier_enregistrement":
			dossier_enregistrement = lignes[i][1]

	if superposer_courbes == None:
		print("lecture_param\nsuperposer_courbes est non défini")
	elif nom_fichier == None:
		print("lecture_param\nnom_fichier est non défini")
	elif nom_dossier == None:
		print("lecture_param\nnom_dossier est non défini")
	elif calc_temps == None:
		print("lecture_param\ncalc_temps est non défini")
	elif enregistrer_data == None:
		print("lecture_param\nenregistrer_data est non défini")
	elif nom_enregistrement == None:
		print("lecture_param\nnom_enregistrement est non défini")
	elif dossier_enregistrement == None:
		print("lecture_param\ndossier_enregistrement est non défini")

	return 	[superposer_courbes,
			nom_fichier,
			nom_dossier,
			calc_temps,
			enregistrer_data,
			nom_enregistrement,
			dossier_enregistrement]