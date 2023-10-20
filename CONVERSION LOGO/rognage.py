# -*- coding: utf-8 -*-

""" 
Ce code a pour but d'automatiser le rognage des logo png qui ont préalablement été convertis du format SVG
vers le format PNG via le scipt shell.
Cela permet ensuite de pouvoir ensuite les utiliser directement avec les différents générateurs de badges.
Ce fichier python est directement appelé depuis le script shell, en lui précisant via la ligne de commande 
les différents dossiers à utiliser

Le rognage de l'image est fait via la librairie Pillow et la fonction getbox()

"""


import argparse
from PIL import Image
import os

# Créez un objet ArgumentParser
parser = argparse.ArgumentParser(description='Script de recadrage d\'images.')

# # Ajoutez des arguments de ligne de commande pour les dossiers d'entrée et de sortie
parser.add_argument('input_dir', type=str, help='Chemin vers le répertoire d\'entrée contenant les fichiers PNG')
parser.add_argument('output_dir', type=str, help='Chemin vers le répertoire de sortie pour les images recadrées')

# # Analysez les arguments de la ligne de commande
args = parser.parse_args()

input_dir="/Users/kilianpouderoux/Desktop/FORUM/LOGO_PNG"

# Chemin vers le répertoire de sortie pour les fichiers PNG
output_dir="/Users/kilianpouderoux/Desktop/FORUM/LOGO_CROP"

# Vérifiez si le répertoire de sortie existe, sinon, créez-le
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Liste tous les fichiers dans le répertoire d'entrée
files = os.listdir(args.input_dir)

problemes = []

# Boucle à travers tous les fichiers du répertoire d'entrée
for file in files:
    if file.endswith(".png"):  # Assurez-vous que le fichier est une image PNG
        # Chemin complet du fichier d'entrée
        input_path = os.path.join(args.input_dir, file)

        # Charger l'image avec Pillow
        try:
            img = Image.open(input_path)
            # recadrage de l'image
            cropped_img = img.crop(img.getbbox())
            # Enregistrez l'image recadrée dans le répertoire de sortie avec le même nom
            output_path = os.path.join(args.output_dir, file)
            cropped_img.save(output_path)
        except:
            problemes.append(file)

    else: print("Erreur avec le fichier " + file + "pas le bon format")

print("Problemes avec les logos suivants : ")
for elt in problemes:
    print(elt)