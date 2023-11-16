"""Ce code c'est pour faire le planning personnalisé en affichant une perm par feuille, et pour la première seulement ca affiche le planning de la journée"""


import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame

# Chargement des données de description
description_perms = {"Respo Stands Café": """Bien vérifier que tous les stands sont clean, bien ravitaillés. En cas de besoin, appeler ou aller à la cuisine pour le dire au respo 2a ravitaillement""",
"Respo Production Café": """Tuto dispo sur le drive pour les cafés
Vérifier que du café tourne TOUT LE TEMPS""",
"Respo Accueil Entreprises": """BIEN AVOIR LU LE DESCRIPTIF DETAILLE OBLIGATOIREMENT""",
"Respo 2A Ramassage Moquette Restante": """""",
"Respo Sécu/Secouristes": """""",
"Respo GDL": """""",
"Respo Plantes": """""",
"Respo Moquettes": """""",
"Respo Vestiaires": """BIEN AVOIR LU LE DESCRIPTIF DETAILLE OBLIGATOIREMENT""",
"Respo Audiovisuel": """""",
"Respo Accueil Étudiant": """""",
"Respo Navettes": """""",
"Respo Distribution Petit Dej": """""",
"Respo Café Rencontre": """""",
"Respo Conférence": """Force à toi, prend une tisane pour Guigui""",
"Respo Réception Dej Étudiant": """""",
"Respo SU": """Respo SU""",
"Respo Trésorerie": """Faites nous de la moulah""",
"Respo 2A Ramassage Moquette Restante": """""",
"Distribution Petit Dej": """Lieu de rdv: cuisine (vers le stand café en zone conseil)

Descriptif: 
la premiere chose a faire le matin -> allumer les percos en cuisine!!! 

Aider la boulangerie à sortir les viennoiseries et les monter en zone Production/Santé (il y aura des chariots) vers la cuisine (en haut de la zone Conseil). 

Se répartir en 3 groupes: chaque groupe préparent 2 stands cafés en jus+viennoiseries.""",
"Ravitaillement Stand": """Lieu de rdv: En cuisine (au niveau du stand café en haut de Zone Conseil)

Respos: 7h - 9h Thibault, 9h - 12h Antoine Marquis, 12h - 14h Paul-Aim, 14 - 17h Elie 

Descriptif:
Rester en cuisine, le respo a un talkie et vous dira ce qu’il faut amener et à quel stand café quand il manque un truc.

Revenir en cuisine après

Ramener les thermos vides en cuisine""",
"Accueil Entreprises": """Lieu de rdv: niveau 0 du Palais des Congrès (borne accueil)

Besoin de: tel chargé, ordi chargé

Respos: 8h-11h: Allan, 11h-14h: Christelle, 14h-17h: Guido

Descriptif: LIRE OBLIGATOIREMENT LE DESCRIPTIF DÉTAILLÉ SUR DOCS FORMATIONS
L’intervenant a un QR code: vous le scannez, ça vous renvoie vers un sheet où vous cochez leur nom. Si le badge est imprimé (d’après le sheet), l’intervenant peut monter au forum. Sinon, il avance vers la borne, où le badge sera imprimé.

Sans QR code: une autre file est dédiée

Si l’intervenant n’est pas sur le sheet: appelez un 2a""",
"Orientation Intervenants": """Lieu de rdv: haut de l’escalator (à côté du vestiaire intervenant)

Descriptif: 
Toujours au moins une personne en haut de l’escalator (les intervenants patientent s’il n’y a plus qu’un seul staffeur). 

Leur demander s’ils veulent passer au vestiaire. Si oui, les accompagner (VESTIAIRE ENTREPRISE, PAS ÉTUDIANT).

Leur demander ensuite leur entreprise, les y emmener grâce au plan""",
"Audiovisuel": """""",
"Navettes Agora": """Lieu de rdv: Agora

Besoin de: tel chargé

Respo: Julien

Descriptif: 
Checker que l’étudiant a sa carte CS (leur ID pour les doctorants), cocher les noms sur le sheet, leur mettre un bracelet, leur donner un plan (et brochure s'ils en ont pas eu)

Leur parler de la restauration étudiante

Avant de monter dans le bus, qqn checke que l’étudiant a un bracelet + tenue correcte.""",
"Navettes PDC": """Lieu de rdv: Au QG pour récupérer la liste des gens qui doivent être présents dans chaque navette de retour. 

Respo: Julien

Descriptif: Checker que les gens qui rentrent sont sur la liste, les navettes partent max à 17h15. Pas besoin de scanner QR code mais il faut cocher sur sheet les gens présents.""",
"Accueil Étudiant Navette": """Lieu de rdv: niveau 0 du PdC (bornes accueil étudiant)

Besoin de: tel chargé, ordi chargé

Respos: 8h-12h: Lea // 12h-14h00: Louis // 14h00-17h00: Fernando

Descriptif: 
Rester branché sur groupe whatsapp avec respo navette + respo accueil. Il y aura un message quand une navette arrive. 

Aller à la rencontre de la navette, vérifier que tout le monde a bracelet+plan

Demander au respo accueil étudiant s’il y a trop de monde aux bornes d'accueil: 

Si oui, les faire patienter dans le bus.

Sinon, les faire rentrer par porte Paris, leur indiquer le vestiaire, sans que DES EXTES NE SE RAJOUTENT AU GROUPE.""",
"Accueil Étudiant Desk": """Lieu de rdv: niveau 0 du PdC, aux bornes d’accueil

Besoin de: telephone chargé, ordi chargé

Respos: 8h-12h: Lea // 12h-14h00: Louis // 14h00-17h00: Fernando

Descriptif: 
Contrôle identité étudiant (carte CS / liste alumni /…), leur donner un bracelet, un plan: Les seuls élèves autorisés sont les élèves et anciens des écoles CentraleSupélec, Centrale Paris et Supélec

Leur parler de la restauration étudiante, leur indiquer accès.""",
"Vestiaire": """Lieu de rdv: Vestiaire étudiant, Foyer du grand amphi “étage 0,5”

Respos: Corentin 7h30-10h, Elie 10h-13h, Kilian 13h-15h30, Marceau 15h30-18h

Descriptif: LIRE OBLIGATOIREMENT DESCRIPTIF DÉTAILLÉ 
8 files: chaque file = un intervalle de tickets (1ère file = tickets du 1 à 150, 2ème file = 151 à 300, etc) Chaque ticket se divise facilement en 3 bouts: B1, B2, B3. 

Étudiant arrive, te donne sac et manteau. Tu poses le manteau sur le cintre, le sac dans le carton au pied du cintre. B1 reste sur le cintre, tu agrafes B2 au sac et tu donnes B3 à l’étudiant. 

Tu dis à l’étudiant de faire la même file pour récupérer ses affaires. 

Pour récupérer affaires: étudiant va dans la même file, te donne B3 et tu lui demandes à quoi ressemblent manteau + sac.""",
"Stand Café 1": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif:
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 2": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 3": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 4": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 5": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 6": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Stand Café 7": """Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 

Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone

Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 

Garder le stand propre et joli (sans déchets)

S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.

ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!""",
"Respo Ravitaillement": """Lieu de rdv: En cuisine (haut Zone Conseil)

Respo de Perm : Thibault 7 - 9h, Antoine Marquis 9 - 12h, Paul-Aim 12 - 14h, Elie 14 - 17h 
Besoin de: Papier + stylo

Descriptif: Tu as un talkie, dès qu’un stand café a besoin de qqc, tu le notes sur une feuille en papier, le chariot est préparé en cuisine, dès qu’un 1 1A arrive, il emmène le chariot, tu barres sur la feuille.

Un thermos qui part = rappeler au 1A de ramener le thermos vide qui est remplacé!""",
"Audiovisuel": """Lieu de rdv: QG

Respos: Elisa (pour les trucs rencontre), Gab // Karina // Geliot 

Descriptif: 
Appeler à 9h pour les café rencontre du matin: rdv 9h45 devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente 

Appeler à 15h pour les cafés rencontre du matin: rdv 15h45 devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente

Appeler à 11h30 (resp. 12h30) pour les dej rencontre: rdv 12h15 (resp. 13h15) devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente 

Etat des lieux du matos audiovisuel + support MywayForum""",
"Production Café": """Lieu de rdv: en cuisine

Descriptif: Faire du café, le mode d’emploi est sur le drive, dans Log 2023 -> J-2, J-1, jour J -> Descriptif de perm (page 29)""",
"Restauration Étudiante Construction": """Lieu de Rdv: Zone restauration rapide (Passy = Zone Construction /// Ternes = Finance, selon votre planning!)

Besoin de: Lydia Pro, tel chargé

Descriptif: 
Vente de repas aux étudiants: grâce au QR code billetterie

Vente de repas aux intervenants: grâce aux TPE à partir de 11h30 

Pour le staffeur au bout de la file étudiante: tu scannes leur QR achat et tu écris un W si cest un wrap, C pour cesar, v pr salade vg, rien pour sándwich. 

Pour le staffeur qui sert la nourriture : tu regardes le bracelet avant de servir. 

Vente de repas aux intervenants: tu leur demandes leur tickets de caisse et tu leurs sers ce qu’ils demandent""",
"Restauration Étudiante Energie": """Lieu de Rdv: Zone restauration rapide (Passy = Zone Construction /// Ternes = Finance, selon votre planning!)

Besoin de: Lydia Pro, tel chargé

Descriptif: 
Vente de repas aux étudiants: grâce au QR code billetterie

Vente de repas aux intervenants: grâce aux TPE à partir de 11h30 

Pour le staffeur au bout de la file étudiante: tu scannes leur QR achat et tu écris un W si cest un wrap, C pour cesar, v pr salade vg, rien pour sándwich. 

Pour le staffeur qui sert la nourriture : tu regardes le bracelet avant de servir. 

Vente de repas aux intervenants: tu leur demandes leur tickets de caisse et tu leurs sers ce qu’ils demandent""",
"Distribution Restauration Start Up": """Lieu de rdv: vous êtes normalement déjà ensemble et avez réceptionné les pack bouffes

Descriptif: 
Vérifier que contenu de chaque sac = description etiquette sac (sinon: les échanger avec des repas ds les frigos pour que les packs soient corrects)

Les livrer sur les stands SU + livrer repas à la sécu et secouristes""",
"Vente et achat de repas": """Lieu de rdv: Que Coco est concerné, à 10h en Salle Passy pour se brancher avec Elisa et Hyatt""",
"Vérification Packs SU": """Lieu de Rdv: Cuisine (vers le haut de la zone Conseil)

Descriptif: 
Réceptionner bouffe SU en gare de livraison""",
"Café Rencontre": """Lieu de rdv: Salle Dej/Café Rencontre Passy, (en haut à gauche du plan)

Descriptif: Checkez identité de chaque étudiant à l’entrée""",
"Déjeuner Rencontre": """Lieu de rdv: Salle Dej/Café Rencontre Passy, (en haut à gauche du plan)

Descriptif: 
Checkez identité de chaque étudiant à l’entrée

Renfort à Elisa et Corentin si besoin pour les repas Hyatt""",
"QDS Energie": """Lieu de rdv: Point information en Energie (en bas à gauche du plan)

Descriptif: Vous êtes en binôme (un fait remplir le QDS sur la tablette, l’autre démarche des étudiants). Si l’étudiant répond, vous lui donnez un cookie.""",
"QDS Construction": """Lieu de rdv: Point information en Construction (en haut à droite du plan)

Descriptif: Vous êtes en binôme (un fait remplir le QDS sur la tablette, l’autre démarche des étudiants). Si l’étudiant répond, vous lui donnez un cookie.""",
"Point Info / QDS Energie": """Lieu de rdv: Point information Energie (en bas à gauche du plan)

Descriptif: Vous êtes en binôme (un fait remplir le QDS sur la tablette, l’autre démarche des étudiants). Si l’étudiant répond, vous lui donnez un cookie. 
Des intervenants viendront peut-être acheter des repas restauration rapide au TPE: Leur dire qu’ils doivent garder leur ticket! Restez attentifs TOUT LE TEMPS sur whatsapp aux instructions de Loik pour gérer les stocks""",
"Point Info / QDS Construction": """Lieu de rdv: Point information en Construction (en haut à droite du plan)

Descriptif: Vous êtes en binôme (un fait remplir le QDS sur la tablette, l’autre démarche des étudiants). Si l’étudiant répond, vous lui donnez un cookie. Des intervenants viendront peut-être acheter des repas restauration rapide au TPE: Restez attentifs TOUT LE TEMPS sur whatsapp aux instructions de Loik pour gérer les stocks""",
"Ravitaillement Bombonne/Carafes": """Lieu de rdv: En cuisine (vers le stand café en haut de la zone conseil)

Descriptif: Un 2A avec un talkie vous dira quelles fontaines à eau sont à changer avec une nouvelle bonbonne à eau, un tuto pour vous montrer comment faire sera dispo en cuisine.""",
"Impression Documents QG": """Lieu de Rdv: bah… le QG

Besoin de: ordi chargé

Descriptif: Imprimez les docs dont on a besoin (ayez les templates des badges prêts, whatsapp ouvert)""",
"Réception Dej Étudiant": """Lieu de rdv: QG

Descriptif: Aller chercher commande et remplir les frigos des 2 zones restauration rapide""",
"Restauration Intervenant": """Lieu de rdv: Salle dej/café rencontre (en haut à gauche du plan)

Descriptif: Réguler l’entrée des intervenants, gérer les soucis de type échange de menu, etc.""",

}

# on modifie le texte en rajoutant des balises html pour les line break et le texte en gras
for key in description_perms.keys():
    lignes = description_perms[key].splitlines()
    lignes_modifiees = [ligne + "<br />\n" for ligne in lignes]
    description_perms[key] = '\n'.join(lignes_modifiees)
    description_perms[key] = description_perms[key].replace("Descriptif:", "<b>Descriptif:</b>")
    description_perms[key] = description_perms[key].replace("Lieu de rdv:", "<b>Lieu de rdv</b>")
    description_perms[key] = description_perms[key].replace("Besoin de:", "<b>Besoin de:</b>")

    
# Charger les données depuis un fichier CSV
try:
    db = pd.read_csv("data.csv", sep=';', dtype=str)
except FileNotFoundError:
    print("La database est introuvable")
    quit()

# Styles
styles = getSampleStyleSheet()
styleN = styles["Normal"]
title_style = styles['Title']
nom = "" # pour avoir le nom parce que le callback de cette fonction prend pas d'argumentgs

# Fonction pour créer une table
def create_table(data, colWidths):
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            data[i][j] = Paragraph(cell, styleN)

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.ReportLabLightBlue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 1),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    return Table(data, colWidths=colWidths, style=table_style)

def creation_table_perms():
    liste_de = []
    toutdata = []
    
    for perm in liste_tr[1:]:  # Exclure l'en-tête

        perm_name = perm[1].text

        if perm_name in description_perms.keys():
            if perm_name not in liste_de:
                
                liste_de.append(perm_name)
                description = description_perms[perm_name]
                data_description = [perm_name, description]
                toutdata.append(data_description)
        elif perm_name == '0':
            pass
        else:
            if perm_name not in liste_de:
                liste_de.append(perm_name)
                description = "Allez voir le guide"
                data_description = [perm_name, description]
                toutdata.append(data_description)

    rajouter = ["<b>Nom de la perm</b>", "<b>Description</b>"]
    toutdata.insert(0,rajouter)
    a_mettre = create_table(toutdata, colWidths=[7*cm, 12*cm])
    elements.append(a_mettre)
    elements.append(Spacer(1, 12))


# pour les header des pages
def header(canvas, doc):
    canvas.saveState()
    # Insérer l'image du logo
    canvas.drawImage('/Users/kilianpouderoux/Documents/Forum/NDF/logo_forum.png', 10, A4[1] - 3*cm - 1*cm, width=8*cm, height=3*cm)

    # Textes pour l'en-tête
    text_header_1 = "Planning pour " + nom  # Texte en gras
    text_header_2 = "Mardi 21/11/2023 au Palais des Congrès"  # Texte normal
    taille_texte = 12  # Taille de la police pour le texte

    # Définir et calculer la largeur du premier texte (en gras)
    canvas.setFont("Helvetica-Bold", taille_texte)
    text_width_1 = canvas.stringWidth(text_header_1, "Helvetica-Bold", taille_texte)

    # Définir et calculer la largeur du deuxième texte (normal)
    canvas.setFont("Helvetica", taille_texte)
    text_width_2 = canvas.stringWidth(text_header_2, "Helvetica", taille_texte)

    # Position x pour aligner à droite
    x_text = A4[0] - doc.rightMargin - max(text_width_1, text_width_2)

    # Position y pour les deux lignes de texte
    y_text_1 = A4[1] - 3*cm - 1*cm
    y_text_2 = y_text_1 - 1.5 * taille_texte  # Décaler vers le bas pour la deuxième ligne

    # Dessiner la première ligne de texte (en gras)
    canvas.setFont("Helvetica-Bold", taille_texte)
    canvas.drawString(x_text, y_text_1, text_header_1)

    # Dessiner la deuxième ligne de texte (normale)
    canvas.setFont("Helvetica", taille_texte)
    canvas.drawString(x_text, y_text_2, text_header_2)

    canvas.restoreState()




# Créer le PDF pour chaque colonne du CSV
for col in db.columns[1:]:
    output_file = str(col) + ".pdf"
    nom = col
    doc = BaseDocTemplate(output_file, pagesize=A4)

    # Définir les marges et la taille de la zone de contenu
    marge_haut = 4*cm  # Ajustez cette marge pour l'en-tête
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - marge_haut, id='normal')
    template = PageTemplate(id='OneCol', frames=frame, onPage=header)
    doc.addPageTemplates([template])
    elements = []


    # Création de la première table (planning)
    noms_cols = ["<b>Horaire</b>", "<b>Staff</b>"]
    liste_horaire = db["mardi 21/11"].tolist()
    liste_staff = db[col].tolist()
    liste_tr = [list(pair) for pair in zip(liste_horaire, liste_staff)]
    liste_tr.insert(0, noms_cols)

    elements.append(create_table(liste_tr, colWidths=[7*cm, 12*cm]))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())
    
    liste_de = [] # la liste de toutes les perms de la personne
    toutdata = [] # pour joindre les infos, on va créer la table à partir de ça
    
    # création de la table de description des perms
    for perm in liste_tr[1:]:
        perm_name = perm[1].text
        # Ajouter un titre  
        titre = perm_name

        if perm_name in description_perms.keys():
            if perm_name not in liste_de:
                elements.append(Paragraph(titre, title_style))
                elements.append(Spacer(1, 12))
                
                liste_de.append(perm_name)
                description = description_perms[perm_name]
                elements.append(Paragraph(description, styleN))
                elements.append(Spacer(1, 12))

                # Ajouter un saut de page après chaque ensemble d'éléments, sauf pour la dernière page
                if perm != liste_tr[-1]:
                    elements.append(PageBreak())
                
        elif perm_name == '0':
            pass
        else:
            if perm_name not in liste_de:
                elements.append(Paragraph(titre, title_style))
                elements.append(Spacer(1, 12))
                
                liste_de.append(perm_name)
                description = "Allez voir le guide"
                elements.append(Paragraph(description, styleN))
                elements.append(Spacer(1, 12))

                # Ajouter un saut de page après chaque ensemble d'éléments, sauf pour la dernière page
                if perm != liste_tr[-1]:
                    elements.append(PageBreak())
                

        

        # Ajouter une image
        # chemin_image = perm["chemin_image"]  # Assurez-vous que le chemin est correct
        # image = Image(chemin_image, width=200, height=200)  # Ajustez les dimensions selon vos besoins
        # elements.append(image)

        # Ajouter un espace avant de passer à la page suivante
        

    chemin_image = "/Users/kilianpouderoux/Documents/Forum/FICHES DE PERM/clemsou.png"  # Remplacez par le chemin de votre image
    image = Image(chemin_image, width=300, height=300)  # Ajustez les dimensions selon vos besoins
    elements.append(image)
    
    # Création du PDF
    try:
        doc.build(elements)
        print("Génération de " + output_file + " terminée")
    except Exception as e:
        print("Problème lors de la création du fichier PDF : " + output_file)
        print(str(e))
    break