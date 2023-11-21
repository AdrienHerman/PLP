"""
Traitement des données des expérimentations
HERMAN Adrien
21/11/2023
"""

def suppr_rollback(F, dep, tmps=[]):
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

	if len(F) != 0 and (len(F) != len(dep) or len(dep) != len(tmps)):
		print("Les vecteurs d'entrée doivent-être de même longueur et non vides !")

		return [], [], []

	i = 1

	while True:
		if i > len(dep) - 1:	break
		if dep[i] > 0 and dep[i] > 0:
			if dep[i] < dep[i - 1]:
				if rollback_action == 0:
					del dep[i]
					del F[i]
			else:
				i += 1
		else:
			i += 1

	return F, dep, tmps