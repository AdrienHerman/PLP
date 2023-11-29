"""
Exportation du modèle 3D
HERMAN Adrien
04/10/2023
"""

# Importation des modules Python
import FreeCADGui, ImportGui, os

def export_body(doc=None,
				nom_body_losange="Body_Losange",
				export=True,
				export_path=os.getcwd(),
				export_name = "/export",
				debug=True,
				file_debug=None):
	"""
	Exportation du modèle 3D
	
	-----------
	Variables :
	-----------
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		nom_body_losange -> Nom de la pièce
		export -> Exporter en step la pièce = True
		export_path -> Chemin vers la pièce à exporter (avec le nom_de_la_piece.step)
		export_name -> Nom d'exportation de la pièce
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
				debug_current_folder -> Générer le fichier de déboggage dans
			le dossier "debug" du répertoire courrant si True, sinon
			Générer le fichier de déboggae dans le dossier indiqué dans la variable
		file_debug -> Fichier de déboggage (ouvert)
	"""

	# Importation de modules Python
	import sys

	# Importation des modules du logiciel
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/")
	#sys.path.append("C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python")
	from debug import wdebug

	if export:
		import Mesh

		if hasattr(Mesh, "exportOptions"):
			options = Mesh.exportOptions(export_path + "/" + export_name + ".stl")
			Mesh.export([doc.getObject(nom_body_losange)], export_path + "/" + export_name + ".stl", options)
		else:
			Mesh.export([doc.getObject(nom_body_losange)], export_path + "/" + export_name + ".stl")
		"""
		try:
			ImportGui.export([doc.getObject(nom_body_losange)], export_path + "/" + export_name + ".stl")

			if file_debug != None and debug:
				wdebug("Exportation du modèle 3D : {0}\n".format(export_path + "/" + export_name + ".stl"), file_debug)

		except:
			if file_debug != None and debug:
				wdebug("L'exportation du modèle 3D à échoué : {0}\n".format(export_path + "/" + export_name + ".stl"), file_debug)
		"""