"""
Lecture des paramètres
HERMAN Adrien
21/11/2023
"""

def lecture_param(path_config="config.txt"):
	"""
	Lecture des paramètres

	-----------
	Variables :
		- path_config : Chemin vers le fichier de configuration
	-----------
	"""

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
			else:	print("Commande inconnue pour superposer_courbes")
		elif lignes[i][0] == "nom_fichier":
			nom_fichier = lignes[i][1]
		elif lignes[i][0] == "nom_dossier":
			nom_dossier = lignes[i][1]
		elif lignes[i][0] == "calc_temps":
			if lignes[i][1] == "False":		calc_temps = False
			elif lignes[i][1] == "True":	calc_temps = True
			else:	print("Commande inconnue pour calc_temps")
		elif lignes[i][0] == "enregistrer_data":
			if lignes[i][1] == "False":		enregistrer_data = False
			elif lignes[i][1] == "True":	enregistrer_data = True
			else:	print("Commande inconnue pour enregistrer_data")
		elif lignes[i][0] == "nom_enregistrement":
			nom_enregistrement = lignes[i][1]
		elif lignes[i][0] == "dossier_enregistrement":
			dossier_enregistrement = lignes[i][1]

	if superposer_courbes == None:
		print("superposer_courbes est non défini")
	elif nom_fichier == None:
		print("nom_fichier est non défini")
	elif nom_dossier == None:
		print("nom_dossier est non défini")
	elif calc_temps == None:
		print("calc_temps est non défini")
	elif enregistrer_data == None:
		print("enregistrer_data est non défini")
	elif nom_enregistrement == None:
		print("nom_enregistrement est non défini")
	elif dossier_enregistrement == None:
		print("dossier_enregistrement est non défini")

	return 	[superposer_courbes,
			nom_fichier,
			nom_dossier,
			calc_temps,
			enregistrer_data,
			nom_enregistrement,
			dossier_enregistrement]