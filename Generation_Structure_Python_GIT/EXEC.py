"""
Fichier d'exécution du code de génération des structures
HERMAN Adrien
29/11/2023
"""

# Modules de Python

# Modules du Logiciel
from bin.lecture_param import *

# Lecture des parmaètres du programme
[	lecture_param_ok,
	gen_losange_basic,
	gen_losange_grad] = lecture_param()

if lecture_param_ok:
	pass

else:
	print("La lecture des paramètres ne s'est pas terminée correctement !")