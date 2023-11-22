"""
Lecture des données expérimentales provenant de
l'oscilloscope du LAMIH
HERMAN Adrien
18/11/2023
"""

def lire_fichier_csv_oscilo(filePath=None):
	"""
	Ouverture et lecture des données d'un fichier .csv provenant
	de l'osciloscope du LAMIH.

	-----------
	Variables :
		- filePath : Chemin vers le fichier
		- file : Objet fichier
		- lignes : Liste contenant toutes les lignes du fichier
	-----------
	"""

	try:
		file = open(filePath, "r")
		lignes = file.readlines()
		file.close()

		for i in range(len(lignes)):
			lignes[i] = lignes[i].split(',')

		return lignes
	except:
		print("Impossible de lire le fichier :\n     filePath={0}".format(filePath))

		return []

def lire_fichier_txt_python(filePath=None):
	"""
	Ouverture et lecture des données d'un fichier .txt provenant
	du traitement des données faites sur Python.

	-----------
	Variables :
		- filePath : Chemin vers le fichier
		- file : Objet fichier
		- lignes : Liste contenant toutes les lignes du fichier
	-----------
	"""
	F = []
	dep = []
	tmps = []

	try:
		file = open(filePath, "r")
		lignes = file.readlines()
		file.close()

		for i in range(len(lignes)):
			lignes[i] = lignes[i].split(',')

		if len(lignes[3]) == 3:	# Les données de temps sont enregistrées
			try:
				for i in range(3, len(lignes)):
					F.append(float(lignes[i][0]))
					dep.append(float(lignes[i][1]))
					tmps.append(float(lignes[i][2]))

				return F, dep, tmps, lignes[0], lignes[1], lignes[2]

			except:
				print("Le fichier n'a pas une mise en forme correcte ou ses données ne sont pas au bon format")

				return [], [], [], "", "", .0
		else:					# Les données de temps ne sont pas enregistrées
			try:
				for i in range(3, len(lignes)):
					F.append(float(lignes[i][0]))
					dep.append(float(lignes[i][1]))

				return F, dep, [], lignes[0], lignes[1], lignes[2]

			except:
				print("Le fichier n'a pas une mise en forme correcte ou ses données ne sont pas au bon format")

				return [], [], [], "", "", .0
	except:
		print("Impossible de lire le fichier :\n     filePath={0}".format(filePath))

		return []

def lire_en_tete_csv_oscilo(lignes=[]):
	"""
	Lecture des données d'en-tête du fichier .csv provenant
	de l'osciloscope du LAMIH.

	-----------
	Variables :
		- lignes : Liste contenant toutes les lignes du fichier
		- unite_F : Lecture de l'unité de la force paramétrée dans l'osciloscope
		- unite_dep : Lecture de l'unité de déplacement paramétrée dans l'osciloscope
		- echantillonage : Temps d'échantillonnage en ms paramétré dans l'osciloscope
		- date : Date de l'essai renseignée par l'osciloscope
		- heure : Heure de l'essai renseignée par l'osciloscope
	-----------
	"""

	if type(lignes) == list and lignes != []:
		unite_F = list(lignes[6][1])
		while '"' in unite_F:	unite_F.remove('"')
		while ' ' in unite_F:	unite_F.remove(' ')
		while '\n' in unite_F:	unite_F.remove('\n')
		unite_F = ''.join(unite_F)
		unite_dep = list(lignes[6][2])
		while '"' in unite_dep:	unite_dep.remove('"')
		while ' ' in unite_dep:	unite_dep.remove(' ')
		while '\n' in unite_dep:	unite_dep.remove('\n')
		unite_dep = ''.join(unite_dep)
		echantillonage = list(lignes[7][1])
		while '"' in echantillonage:	echantillonage.remove('"')
		while ' ' in echantillonage:	echantillonage.remove(' ')
		while '\n' in echantillonage:	echantillonage.remove('\n')
		echantillonage = ''.join(echantillonage)
		echantillonage = 1 / float(echantillonage)
		date = list(lignes[13][1])
		while '"' in date:	date.remove('"')
		while ' ' in date:	date.remove(' ')
		while '\n' in date:	date.remove('\n')
		date = ''.join(date)
		heure = list(lignes[14][1])
		while '"' in heure:	heure.remove('"')
		while ' ' in heure:	heure.remove(' ')
		while '\n' in heure:	heure.remove('\n')
		heure = ''.join(heure)

		return unite_F, unite_dep, echantillonage, date, heure
	else:
		print("La variable contenant les données du fichier .csv est vide ou du mauvais type\n     lignes={0}".format(lignes))

		return "", "", .0, "", ""

def lire_contenu_csv_oscillo(lignes=[]):
	"""
	Lecture des données de l'expériences (à partir de la
	ligne 16 du fichier .csv provenant de l'osciloscope du LAMIH)

	-----------
	Variables :
		- lignes : Liste contenant toutes les lignes du fichier
		- F : Vecteur force
		- dep : Vecteur déplacement
	-----------
	"""

	if type(lignes) == list and lignes != []:
		try:
			F = []
			dep = []

			for i in range(16, len(lignes)):
				F.append(float(lignes[i][1]))
				dep.append(float(lignes[i][2]))
			
			return F, dep

		except:
				print("Le fichier n'a pas une mise en forme correcte ou ses données ne sont pas au bon format")

				return [], []
	else:
		print("La variable contenant les données du fichier .csv est vide ou du mauvais type\n     lignes={0}".format(lignes))

		return [], []

def calc_temps_essai(dep=[], echantillonage=.0):
	"""
	Calcul du vecteur temps de l'essai à partir du temps d'échantillonage
	et des données de déplacement.

	-----------
	Variables :
		- dep : Vecteur déplacement
		- echantillonage : Temps d'échantillonnage en ms paramétré dans l'osciloscope (s)
		- tmps : Vecteur temps (ms)
	-----------
	"""

	if type(dep) != list or type(echantillonage) != float:
		print("Les types des arguments ne sont pas correctes.\n     type(dep)={0}\n     type(echantillonage)={1}".format(type(dep), type(echantillonage)))

		return []

	if dep != [] and echantillonage != 0:
		tmps = []

		for i in range(len(dep)):
			tmps.append(echantillonage * 1e3 * i)

		return tmps
	else:
		print("Les données de déplacement ou d'échantillonage sont inexistantes.\n     dep={0}\n     echantillonage={1}".format(dep, echantillonage))

		return []

def enregistrer_donnees(F=[], dep=[], tmps=[], calc_temps=True, filePath="", unite_F="", unite_dep="", echantillonage=.0, date="", heure=""):
	"""
	Enregistrer les données lues des fichiers .csv provenant de
	l'osciloscope du LAMIH.

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
		- tmps : Vecteur temps (ms)
		- calc_temps : Valeur booléenne pour le calcul ou non du vecteur temps
		- filePath : Chemin vers le fichier à enregistrer (Attention si le fichier existe cela l'écrasera)
		- unite_F : Lecture de l'unité de la force paramétrée dans l'osciloscope
		- unite_dep : Lecture de l'unité de déplacement paramétrée dans l'osciloscope
		- echantillonage : Temps d'échantillonnage en ms paramétré dans l'osciloscope
		- date : Date de l'essai renseignée par l'osciloscope
		- heure : Heure de l'essai renseignée par l'osciloscope
	-----------
	"""

	string_file = date + "\n" + heure + "\n" + str(echantillonage) + "\n"

	if type(dep) != list or type(F) != list or type(tmps) != list or type(calc_temps) != bool or type(filePath) != str or type(unite_F) != str or type(unite_dep) != str or type(echantillonage) != float or type(date) != str or type(heure) != str:
		print("""Les types des arguments ne sont pas correctes.\n
				     type(dep)={0}\n
				     type(echantillonage)={1}\n
				     type(tmps)={2}\n
				     type(calc_temps)={3}\n
				     type(filePath)={4}\n
				     type(unite_F)={5}\n
				     type(unite_dep)={6}\n
				     type(echantillonage)={7}\n
				     type(date)={8}\n
				     type(heure)={9}\n""".format(	type(dep),
				     								type(echantillonage),
				     								type(tmps),
				     								type(calc_temps),
				     								type(filePath),
				     								type(unite_F),
				     								type(unite_dep),
				     								type(echantillonage),
				     								type(date),
				     								type(heure)))

		return False

	if len(F) != len(dep) or len(dep) != len(tmps):
		print("Les vecteurs de données doivent avoir la même longueur.\n     len(F)={0}\n     len(dep)={1}\n     len(tmps)={2}".format(len(F), len(dep), len(tmps)))

		return False

	if F != [] and dep != []:
		if calc_temps == True:
			if tmps != []:
				string_file += unite_F + "," + unite_dep + "," + "ms\n"

				for i in range(len(F)):
					string_file += str(F[i]) + "," + str(dep[i]) + "," + str(tmps[i]) + "\n"
			else:
				print("Le vecteur temps est vide.\n     tmps={0}".format(tmps))

				return False

		else:
			string_file += unite_F + "," + unite_dep + "\n"

			for i in range(len(F)):
				string_file += str(F[i]) + "," + str(dep[i]) + "\n"

		try:
			file = open(filePath, "w")
			file.write(string_file)
			file.close()
		except:
			print("L'enregistrement du fichier à échoué. Le chemin est peut-être incorrect.\n     filePath={0}".format(filePath))

			return False

		return True
	else:
		print("Les vecteurs force et/ou déplacement sont vides.\n     F={0}\n     dep={1}".format(F, dep))

		return False