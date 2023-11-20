# -*- coding: utf-8 -*-

""" 
Ce code a pour but d'automatiser la création des badges staffeurs et membres pour les événements.
Pour le BP ou le Forum il suffit juste de changer le logo
Pour les staffeurs ou les membres faut juste changer la couleur dans le fichier base.html, donc faire 2 fichiers CSV : un pour le staff et un pour les membres
et les passer séparément dans le programme en changeant la couleur.

L'idée c'est, à partir d'un template HTML, de compléter des champs avec les noms et les roles de chacun.
Il y a donc le fichier base.html qui est le squelette du template dans lequel on va ensuite venir rajouter le contenu.
Le contenu généré se retrouve dans le fichier contenu.html qu'on va entièrement ajouter à l'intérieur du squelette pour avoir le contenu final.

Le template est une feuille A4 avec 10 badges dessus sur lesquels est inséré le logo du BP. Les paramètres modifiables sont indiqués dessus.

Pour les noms à rallonge (on te voit Paul-Aim) il faudra faire au cas par cas--> voir base.html.

Les modules utilisés sont jinja2 pour l'utilisation du HTML et pdfkit pour le pdf.

Attention à bien spécifier le chemin du logo BP ou du forum !!
Les noms, prénoms et rôle sont définis dans un fichier CSV

"""


import jinja2
import pdfkit
import pandas as pd
from math import *


# lecture des données à partir du tableau à 3 colonnes recensant nom, prénom et role des personnes

try:
    data = pd.read_excel("coucou.xlsx")
except FileNotFoundError:
    print("La database est introuvable")
    quit()

data["prenom"] = data["prenom"].str.capitalize()
data["nom"] = data["nom"].str.upper()
data["role"] = data["role"].str.capitalize()

for index, value in data["role"].items():
    if str(value) == "nan" or str(value) == "-":
        data.at[index, "role"] = "   "

nom_final = list(data["prenom"] + " " + data["nom"])
role_final = list(data["role"])

# definition de ce qu'on veut remplacer
tab_fin_nom = []
tab_fin_role = []
nb_groupes = ceil(len(nom_final)/10)

# séparation en groupes de 10
for i in range(0,nb_groupes):
    tab_fin_nom.append(nom_final[10*i:10*(i+1)])
    tab_fin_role.append(role_final[10*i:10*(i+1)])


# complétion du dernier groupe si il n'est pas de taille 10
if len(tab_fin_nom[-1]) != 10:
    tab_fin_nom[-1].extend((10-len(tab_fin_nom[-1]))*' ')
    tab_fin_role[-1].extend((10-len(tab_fin_role[-1]))*' ')


# remplissage du dictionnaire de contexte
concon = {}

for i in range(nb_groupes):
    for j in range(10):
        cle_nom = "nom" + str(10*i+j)
        cle_role = "role" + str(10*i+j)
        concon[cle_nom] = tab_fin_nom[i][j]
        concon[cle_role] = tab_fin_role[i][j]


# le template du contenu
# attention à bien vérfier le chemin du logo
text_template = """
    <tr>
        <td>
        <div class="rectangle">
            <p class="line1">{}</p>
            <p class="line2">{}</p>
            <img src="/Users/kilianpouderoux/Desktop/FORUM/Badges/BADGES_STAFF/logo_forum.png" alt="Be Prepared" style="height: 100px;">
        </div>
        </td>
        <td>
        <div class="rectangle">
            <p class="line1">{}</p>
            <p class="line2">{}</p>
            <img src="/Users/kilianpouderoux/Desktop/FORUM/Badges/BADGES_STAFF/logo_forum.png" alt="Be Prepared" style="height: 100px;">
        </div>
        </td>
    </tr>
"""

final_text = ""

# création du contenu
for i in range(nb_groupes):
    for j in range(0,9,2):
        nom0 = "{{{{nom{name}}}}}".format(name=10*i+j)
        role0 = "{{{{role{name}}}}}".format(name=10*i+j)
        nom1 = "{{{{nom{name}}}}}".format(name=10*i+j+1)
        role1 = "{{{{role{name}}}}}".format(name=10*i+j+1)
        final_text += text_template.format(nom0, role0, nom1, role1)



# on fait 2 remplacement: un pour créer le contenu et un autre pour insérer ce contenu dans le corps de base

# loading du template HTML
template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

# création du fichier html de contenu
with open('contenu.html', 'w') as fp:
    fp.write(final_text)

# les placeholder sont remplacés par les données du dictionnaire
html_template = 'contenu.html'
template = template_env.get_template(html_template)
contenu = template.render(concon)

# insertion du contenu dans le corps
new_con = {'contenu':contenu}
html_template = 'base.html'
template = template_env.get_template(html_template)
final_text = template.render(new_con)



# generation du PDF
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
filename = 'badges_finaux.pdf'

def generate_pdf_from_html():
    options = {
        'enable-local-file-access': None
    }
    pdfkit.from_string(final_text, filename, options=options, configuration=config, verbose=True)
        # si ca vous emmerde de voir le texte dans le terminal suffit de mettre verbose=False

generate_pdf_from_html()


