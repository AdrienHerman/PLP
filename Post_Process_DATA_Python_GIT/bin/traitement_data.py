"""
Traitement des données des expérimentations
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import scipy

def suppr_rollback(F=[], dep=[], tmps=[]):
	"""
	Supprimer l'effet de retour en arrière du déplacement.

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
		- tmps : Vecteur temps (ms)
	-----------
	"""

	if type(F) != list or type(dep) != list or type(tmps) != list:
		print("Les types des arguments ne sont pas correctes.\n     type(F)={0}\n     type(dep)={1}\n     type(tmps)={2}".format(type(F), type(dep), type(tmps)))

		return [], [], []

	if len(F) == 0 and (len(F) != len(dep) or len(dep) != len(tmps)):
		print("Les vecteurs d'entrée doivent-être de même longueur et non vides !")

		return [], [], []

	i = 1

	while True:
		if i > len(dep) - 1:	break

		if dep[i] > 0 and dep[i] > 0:
			if dep[i] < dep[i - 1]:
				del dep[i]
				del F[i]
				if tmps != []:	del tmps[i]

			else:
				i += 1
		else:
			i += 1

	return F, dep, tmps

def suppr_saut_force(F, taux_variation=0.05):
	"""
	Supprimer les instabilités de mesure de la force.

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
		- tmps : Vecteur temps (ms)
		- taux_variation :	Critère de variation entre chaque pas pour lisser la courbe
	-----------
	"""
	
	pass

def recherche_debut_impact(F=[], dep=[], tmps=[], taux_agmentation=0.3, nb_pas_avant_agmentation=1, fileName=""):
	"""
	Recherche du début de l'impact

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
		- tmps : Vecteur temps (ms)
		- taux_aumentation : 	Critère d'augmentation entre chaque pas pour détecter l'impact
								pas(i) >= pas(i-1) * (1 + taux_agmentation) => Impact
		- nb_pas_avant_agmentation : Nombre de pas retenus avant l'impact
		- fileName : Nom du fichier étudié (permet d'afficher sur quel fichier l'impact n'a pas été trouvé)
	-----------
	"""

	if type(F) != list or type(dep) != list or type(tmps) != list or type(taux_agmentation) != float or type(nb_pas_avant_agmentation) != int or type(fileName) != str:
		print("Les types des arguments ne sont pas correctes.\n     type(F)={0}\n     type(dep)={1}\n     type(tmps)={2}\n     type(taux_agmentation)={3}\n     type(nb_pas_avant_agmentation)={4}\n     type(fileName)={5}\n".format(type(F), type(dep), type(tmps), type(taux_agmentation), type(nb_pas_avant_agmentation), type(fileName)))

		return [], [], []

	if len(F) == 0 and (len(F) != len(dep) or len(dep) != len(tmps)):
		print("Les vecteurs d'entrée doivent-être de même longueur et non vides !")

		return [], [], []

	if taux_agmentation <= 0:
		print("Le taux d'augmentation doit être positif strict !")

		return F, dep, tmps

	if nb_pas_avant_agmentation < 0:
		print("Le nombre de pas avant augmentation doit être supérieur ou égal à 0 !")

		return F, dep, tmps

	# Stockage de la valeur max de F à chaque pas de recherche
	max_F = 0

	for i in range(len(F)):
		# Critère d'arrêt
		if F[i] > max_F * (1 + taux_agmentation) and i > 10:	break

		# Stockage d'un élément supérieur au max déjà trouvé
		if F[i] > max_F:
			max_F = F[i]

	if i < len(F) and i - nb_pas_avant_agmentation > 0:
		# Suppression des données avant impact
		del F[0 : i - nb_pas_avant_agmentation]
		del dep[0 : i - nb_pas_avant_agmentation]
		del tmps[0 : i - nb_pas_avant_agmentation]

		return F, dep, tmps

	else:
		print("!!! ERREUR : Début de l'impact non trouvé {0} !!!".format(fileName))

		return F, dep, tmps

def energie(F=[], dep=[]):
	"""
	Calcul de l'énergie d'impacten Joules en fonction de la force
	en Newton et du déplacment en milimètres.

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
	-----------
	"""

	if type(F) != list or type(dep) != list:
		print("Les types des arguments ne sont pas correctes.\n     type(F)={0}\n     type(dep)={1}".format(type(F), type(dep)))

		return [], []

	if len(F) == 0 and len(F) != len(dep):
		print("Les vecteurs d'entrée doivent-être de même longueur et non vides !")

		return F, dep

	dep_corrige = dep.copy()
	for i in range(len(dep_corrige)):	dep_corrige[i] *= 1e-3
	
	return scipy.integrate.simps(F, dep_corrige)

def tare_dep(dep=[]):
	"""
	Tare du déplacement après détection du début de l'impact
	(dep[0] = 0 / dep[i > 0] = dep[i] - dep[0]).

	-----------
	Variables :
		- dep : Vecteur déplacement
	-----------
	"""

	if type(dep) != list:
		print("Les types des arguments ne sont pas correctes.\n     type(dep)={1}".format(type(dep)))

		return []

	if len(dep) == 0:
		print("Le vecteur d'entrée doit-être non vide !")

		return dep

	dep0 = dep[0]

	for i in range(len(dep)):
		dep[i] -= dep0

	return dep

def tare_tmps(tmps=[]):
	"""
	Tare du temps après détection du début de l'impact
	(tmps[0] = 0 / tmps[i > 0] = tmps[i] - tmps[0]).

	-----------
	Variables :
		- tmps : Vecteur temps (ms)
	-----------
	"""

	if type(tmps) != list:
		print("Les types des arguments ne sont pas correctes.\n     type(tmps)={1}".format(type(tmps)))

		return []

	if len(tmps) == 0:
		print("Le vecteur d'entrée doit-être non vide !")

		return tmps

	tmps0 = tmps[0]

	for i in range(len(tmps)):
		tmps[i] -= tmps0

	return tmps

def fin_essai(F=[], dep=[], tmps=[], dep_max=19.0):
	"""
	Supprime les données à la fin de l'essai. La fin de
	l'essai est défini par déplacement max de l'impacteur,
	le déplacement max étant le moment où l'impacteur touche
	les tampons.

	-----------
	Variables :
		- F : Vecteur force
		- dep : Vecteur déplacement
		- tmps : Vecteur temps (ms)
		- dep_max : Déplacement max avant impact contre les tampons (mm)
					ATTENTION DOIT ÊTRE UN FLOAT
	-----------
	"""

	if type(F) != list or type(dep) != list or type(tmps) != list or type(dep_max) != float:
		print("Les types des arguments ne sont pas correctes.\n     type(F)={0}\n     type(dep)={1}\n     type(tmps)={2}\n     type(dep_max)={3}".format(type(F), type(dep), type(tmps), type(dep_max)))

		return [], [], []

	if len(F) == 0 and (len(F) != len(dep) or len(dep) != len(tmps)):
		print("Les vecteurs d'entrée doivent-être de même longueur et non vides !")

		return [], [], []

	impact = False

	if max(dep) >= dep_max:
		impact = True

	for i in range(len(dep)):
		if dep[i] >= dep_max:
			break

	del F[i:]
	del dep[i:]
	if tmps != []:	del tmps[i:]

	return F, dep, tmps, impact