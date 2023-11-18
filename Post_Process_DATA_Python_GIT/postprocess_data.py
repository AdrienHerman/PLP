"""
Affichage dans un graphique les données d'expérimentation F=f(eps)
en traitant le début et la fin de l'impact.
HERMAN Adrien
13/11/2023
"""

# Paramètres
taux_agmentation = 0.6 				# Recherche d'une augmentation de X% entre chaque pas pour connaître l'endroit de l'impact
nb_pas_avant_agmentation = 2		# Nombre de pas à prendre en compte avant le début d'impact trouvé
temps_impact = 15					# Temps d'impact à garder sur le grpahe (ms)
echantillonage = 0.15				# Temps d'échantillonage souhaité (ms)
fileName = "STRUCT_5_03.CSV"		# Nom & Chmein du/des fichier(s) de données
folderName = "DATA/6/"				# Nom du dossier contenant toutes les données
interdiction_rollback = True 		# Enlever toutes les données qui reviennent en arrière pour le déplacement
rollback_action = 1 				# 0 = Supprimer les données [NE FONCITONNE PAS BIEN] / 1 = Remplacer les données par les précédentes
traitement_echantillonnage = False 	# Activer le traitement des données (échantillonage moins gros que celui original)
traitement_debut = True				# Activer le traitement des données pour le début d'impact
tare_deplacement = True				# Activer le décalage du déplacement par rapport au début d'impact
superposer_courbes = True 			# Superposer les courbes provenant des données dans le dossier DATA
graphe_vitesse = False				# Afficher le graphe de vitesse
calcul_energie = True 				# Calculer l'énergie par intégration numérique avec la méthode de Simpson (Newton-Cotes pour 3 points) -> J
facteur_force = 1 					# Factueur multiplicateur du vecteur force (pour le mettre dans la bonne unité) -> N
facteur_deplacements = 1e-3 		# Facteur multiplicateur du vecteur déplacement (pour le mettre dans la bonne unité) -> m

# Dépasser 19mm => Tampon

# Modules de Python
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import integrate
import os

def lire_fichier(fileName):
	# Ouverture du fichier de DATA et lecture
	file = open(fileName, "r")
	lignes = file.readlines()
	file.close()
	for i in range(len(lignes)):	lignes[i] = lignes[i].split(',')

	return lignes

def en_tete(lignes):
	# Traitement des données d'en-tête
	unite_F = list(lignes[6][1])
	while '"' in unite_F:	unite_F.remove('"')
	while ' ' in unite_F:	unite_F.remove(' ')
	while '\n' in unite_F:	unite_F.remove('\n')
	unite_F = ''.join(unite_F)
	unite_eps = list(lignes[6][2])
	while '"' in unite_eps:	unite_eps.remove('"')
	while ' ' in unite_eps:	unite_eps.remove(' ')
	while '\n' in unite_eps:	unite_eps.remove('\n')
	unite_eps = ''.join(unite_eps)
	resolution = list(lignes[7][1])
	while '"' in resolution:	resolution.remove('"')
	while ' ' in resolution:	resolution.remove(' ')
	while '\n' in resolution:	resolution.remove('\n')
	resolution = ''.join(resolution)
	resolution = 1 / float(resolution)
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

	return unite_F, unite_eps, resolution, date, heure

def data(lignes):
	# Traitement des données F=f(eps)
	F = []
	eps = []

	for i in range(16, len(lignes)):
		F.append(float(lignes[i][1]))
		eps.append(float(lignes[i][2]))
	
	return F, eps

def rollback(interdiction_rollback, rollback_action, F, eps):
	# Supprimer les données où le déplacement revient en arrière
	if interdiction_rollback:
		i = 1

		while True:
			if i > len(eps) - 1:	break
			if eps[i] > 0 and eps[i] > 0:
				if eps[i] < eps[i - 1]:
					if rollback_action == 0:
						del eps[i]
						del F[i]
					elif rollback_action == 1:
						eps[i] = eps[i - 1]
						i += 1
					else:
						print("!!!\nERREUR : Action inconnue pour le traitement du rollback\nrollback_action = {0}\n!!!".format(rollback_action))
						break
				else:
					i += 1
			else:
				i += 1

	return F, eps

def recherche_debut_impact(traitement_debut, F, eps, taux_agmentation, nb_pas_avant_agmentation, temps_impact, resolution, fileName):
	# Recherche du début de l'impact
	if traitement_debut:
		max_F = 0
		maxi_F = 0

		for i in range(len(F)):
			if F[i] > max_F * (1 + taux_agmentation) and maxi_F != 0:	break
			if F[i] > max_F:
				max_F = F[i]
				maxi_F = i

		if i < len(F) and i - nb_pas_avant_agmentation > 0:
			del F[0 : i - nb_pas_avant_agmentation]
			del eps[0 : i - nb_pas_avant_agmentation]
			nb_pas_apres_impact = nb_pas_avant_agmentation + int((temps_impact * 1e-3) / resolution)
			del F[nb_pas_apres_impact + 1 :]
			del eps[nb_pas_apres_impact + 1 :]

			return F, eps
		else:
			print("!!!\nERREUR : Début de l'impact non trouvé\n{0}\n!!!".format(fileName))

			return None, None
	else:
		return F, eps

def rev_echantillonage(traitement_echantillonnage, echantillonage, F, eps):
	# Révision de l'échantillonage
	if traitement_echantillonnage:
		nb_pas_echantillonage = int(1 / echantillonage)
		F1 = []
		eps1 = []
		i = 0

		while True:
			if i * nb_pas_echantillonage >= len(F) - 1:	break
			F1.append(F[i * nb_pas_echantillonage])
			eps1.append(eps[i * nb_pas_echantillonage])
			i += 1

		return F1, eps1
	else:
		return F, eps

def tare_eps(eps, tare_deplacement, traitement_debut):
	# Tare du déplacement
	if tare_deplacement and traitement_debut:
		for i in range(1, len(eps)):
			eps[i] -= eps[0]
		eps[0] = 0

	return eps

def calc_v(eps):
	# Calcul de la vitesse
	V = []
	for i in range(len(eps) - 1):
		V.append((eps[i + 1] - eps[i]) / resolution)

	return V

def mult_vecteur(vect, fact):
	# Multiplier tous les éléments d'une liste par un facteur
	for i in range(len(vect)):
		vect[i] *= fact

	return vect

def energie(calcul_energie, F, eps, facteur_force, facteur_deplacements, afficher=""):
	# Calcul de l'énergie par intégration numérique avec la méthode de Simpson (Newton-Cotes pour 3 points)
	if calcul_energie:
		res = integrate.simps(mult_vecteur(F,facteur_force), mult_vecteur(eps, facteur_deplacements))
		if afficher != "":	print(afficher + str(res))

		return res

def graphe(F, eps, fileName, couleurs=['b','g','r','c','m','y','k'], type_lignes=['-','--',':','-.']):
	# Affichage du graphe
	fig, ax = plt.subplots()
	ax.set_title("")
	ax.set_xlabel("Déplacement ({0})".format(unite_eps))
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_ylabel("Force ({0})".format(unite_F))
	for i in range(len(F)):
		ax.plot(eps[i], F[i], couleurs[i % len(couleurs)] + type_lignes[(i // len(couleurs)) % len(type_lignes)], label=fileName[i])
	ax.legend()
	plt.grid()

	return plt

if superposer_courbes:
	# Parsing de tous les fichiers du dossier DATA
	fileNames = [f for f in os.listdir(folderName) if os.path.isfile(os.path.join(folderName, f))]
	for i in range(len(fileNames)):
		if not ".CSV" in fileNames[i] and i < len(fileNames):
			del fileNames[i]
		elif i >= len(fileNames):
			break

	F = []
	eps = []
	entetes = []
	if graphe_vitesse:	V = []
	k = 0
	fileNames_temp = fileNames.copy()

	for i in range(len(fileNames)):
		lignes = lire_fichier(folderName + fileNames[i])
		unite_F, unite_eps, resolution, date, heure = en_tete(lignes)
		entetes.append([unite_F, unite_eps, resolution, date, heure])
		F_temp, eps_temp = data(lignes)
		F_temp, eps_temp = rollback(interdiction_rollback, rollback_action, F_temp, eps_temp)
		F_temp, eps_temp = recherche_debut_impact(traitement_debut, F_temp, eps_temp, taux_agmentation, nb_pas_avant_agmentation, temps_impact, entetes[k][2], fileNames[i])
		if F_temp != None and eps_temp != None:
			F_temp, eps_temp = rev_echantillonage(traitement_echantillonnage, echantillonage, F_temp, eps_temp)
			eps.append(tare_eps(eps_temp, tare_deplacement, traitement_debut))
			F.append(F_temp)
			energie_res = energie(calcul_energie, F[k], eps[k], facteur_force, facteur_deplacements, fileNames[i] + ": ")
			if graphe_vitesse:
				V.append(calc_v(eps_temp))
			k += 1
		else:
			fileNames_temp.remove(fileNames[i])

	fileNames = fileNames_temp
	pltF = graphe(F, eps, fileNames)
	if graphe_vitesse:
		pltV = graphe(V, [[i for i in range(len(F[j]) - 1)] for j in range(len(fileNames))], fileNames)
		pltF.show()
		pltV.show()
	else:
		pltF.show()
else:
	# N'afficher que le graphe d'une seule courbes
	lignes = lire_fichier(folderName + fileName)
	unite_F, unite_eps, resolution, date, heure = en_tete(lignes)
	F, eps = data(lignes)
	F, eps = rollback(interdiction_rollback, rollback_action, F, eps)
	F, eps = recherche_debut_impact(traitement_debut, F, eps, taux_agmentation, nb_pas_avant_agmentation, temps_impact, resolution, fileName)
	if F != None and eps != None:
		F, eps = rev_echantillonage(traitement_echantillonnage, echantillonage, F, eps)
		eps = tare_eps(eps, tare_deplacement, traitement_debut)
		energie_res = energie(calcul_energie, F, eps, facteur_force, facteur_deplacements)
		pltF = graphe([F], [eps], [fileName])
		if graphe_vitesse:
			V = calc_v(eps)
			pltV = graphe([V], [[i for i in range(len(F) - 1)]], [fileName])
			pltF.show()
			pltV.show()
		else:
			pltF.show()