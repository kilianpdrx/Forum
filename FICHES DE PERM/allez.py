import pandas as pd
from math import *
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet




description_perms = {"Distribution Petit Dej":
    """Lieu de rdv: Entrée située devant la place de la porte Maillot (niveau 0)
    Respos: Louis [2A] et Axel [1A]
    Descriptif: 
    - Aider la boulangerie à sortir les viennoiseries et les monter en zone Production/Santé (il y aura des chariots) vers la cuisine (en haut de la zone Conseil). 
    - Se répartir en 3 groupes: chaque groupe preparent 2 stands cafés en jus+viennoiseries.""",
    "Ravitaillement Stand Café":"""Lieu de rdv: En cuisine (au niveau du stand café en haut de Zone Conseil)
    Respos: 7h - 9h Thibault, 9h - 12h Antoine Marquis, 12h - 14h Paul-Aim, 14 - 17h Elie 
    Descriptif:
    - Rester en cuisine, le respo a un talkie et vous dira ce qu’il faut amener et à quel stand café quand il manque un truc.
    - Revenir en cuisine après
    - Ramener les thermos vides en cuisine""",
    "Accueil Entreprises":"""Lieu de rdv: niveau 0 du Palais des Congrès (borne accueil)

Besoin de: tel chargé, ordi chargé

Respos: 8h-11h: Allan, 11h-14h: Christelle, 14h-17h: Guido

Descriptif: LIRE OBLIGATOIREMENT LE DESCRIPTIF DÉTAILLÉ SUR DOCS FORMATIONS
L’intervenant a un QR code: vous le scannez, ça vous renvoie vers un sheet où vous cochez leur nom. Si le badge est imprimé (d’après le sheet), l’intervenant peut monter au forum. Sinon, il avance vers la borne, où le badge sera imprimé.
Sans QR code: une autre file est dédiée
Si l’intervenant n’est pas sur le sheet: appelez un 2a
""",
    "Orientation Intervenants":"""Lieu de rdv: haut de l’escalator (à côté du vestiaire intervenant)

Descriptif: 
Toujours au moins une personne en haut de l’escalator (les intervenants patientent s’il n’y a plus qu’un seul staffeur). 
Leur demander s’ils veulent passer au vestiaire. Si oui, les accompagner (VESTIAIRE ENTREPRISE, PAS ÉTUDIANT).
Leur demander ensuite leur entreprise, les y emmener grâce au plan
""",
    "Navettes Agora":"""Lieu de rdv: Agora

Besoin de: tel chargé

Respo: Julien

Descriptif:  
Checker que l’étudiant a sa carte CS (leur ID pour les doctorants), cocher les noms sur le sheet, leur mettre un bracelet, leur donner un plan (et brochure s'ils en ont pas eu)
Leur parler de la restauration étudiante
Avant de monter dans le bus, qqn checke que l’étudiant a un bracelet + tenue correcte.
""",
    "Navettes PDC":"""Lieu de rdv: Au QG pour récupérer la liste des gens qui doivent être présents dans chaque navette de retour. 

Respo: Julien

Descriptif: Checker que les gens qui rentrent sont sur la liste, les navettes partent max à 17h15. Pas besoin de scanner QR code mais il faut cocher sur sheet les gens présents.
""",
    "Accueil étudiants navettes":"""Lieu de rdv: niveau 0 du PdC (bornes accueil étudiant)

Besoin de: tel chargé, ordi chargé

Respos: 8h-12h: Lea // 12h-14h00: Louis // 14h00-17h00: Fernando

Descriptif: 
Rester branché sur groupe whatsapp avec respo navette + respo accueil. Il y aura un message quand une navette arrive. 
Aller à la rencontre de la navette, vérifier que tout le monde a bracelet+plan
Demander au respo accueil étudiant s’il y a trop de monde aux bornes d'accueil: 
Si oui, les faire patienter dans le bus.
Sinon, les faire rentrer par porte Paris, leur indiquer le vestiaire, sans que DES EXTES NE SE RAJOUTENT AU GROUPE.""",
    "Accueil étudiant (desk/borne)":"""Lieu de rdv: niveau 0 du PdC, aux bornes d’accueil

Besoin de: telephone chargé, ordi chargé

Respos: 8h-12h: Lea // 12h-14h00: Louis // 14h00-17h00: Fernando

Descriptif: 
Contrôle identité étudiant (carte CS / liste alumni /…), leur donner un bracelet, un plan: Les seuls élèves autorisés sont les élèves et anciens des écoles CentraleSupélec, Centrale Paris et Supélec
Leur parler de la restauration étudiante, leur indiquer accès.
""",
    "Vestiaire":"""Lieu de rdv: Vestiaire étudiant, Foyer du grand amphi “étage 0,5”

Respos: Corentin 7h30-10h,  Elie 10h-13h, Kilian 13h-15h30, Marceau 15h30-18h

Descriptif de perm: LIRE OBLIGATOIREMENT DESCRIPTIF DÉTAILLÉ 
8 files: chaque file = un intervalle de tickets (1ère file = tickets du 1 à 150, 2ème file = 151 à 300, etc) Chaque ticket se divise facilement en 3 bouts: B1, B2, B3. 
Étudiant arrive, te donne sac et manteau. Tu poses le manteau sur le cintre, le sac dans le carton au pied du cintre. B1 reste sur le cintre, tu agrafes B2 au sac et tu donnes B3 à l’étudiant. 
Tu dis à l’étudiant de faire la même file pour récupérer ses affaires. 
Pour récupérer affaires: étudiant va dans la même file, te donne B3 et tu lui demandes à quoi ressemblent manteau + sac. 
""",
    "Stand Café":"""Lieu de rdv: Le stand café auquel vous êtes assigné
Respo de la perm : Alix 8h-10h, Kilian 10h-12h, Jamyang 12h-14h30, Leo Michel 14h30-17h

Besoin de: Gants 

Descriptif de perm: 
Le STAND NE RESTE PAS SANS SURVEILLANCE. 
Servir les intervenants (eux ils ne le font en aucun cas): s’ils ont des questions détaillées, dirigez-les vers les respos zone
Servir étudiants: un seul café dans la journée: mettre une croix sur leur bracelet/vérifier s’ils en ont déjà. 
Garder le stand propre et joli (sans déchets)
S’il manque des choses (biscuits, jus, etc): prévenir le ravitaillement sur le canal 3, en anticipant pour qu’aucun stand ne manque de rien.
ATTENTION: Vous êtes respos aussi du ravitaillement des bonbonnes à eau proches du stand!
""",
    "Ravitaillement [Descriptif pour le Respo 2A]":"""Lieu de rdv: En cuisine (haut Zone Conseil)

Respo de Perm : Thibault 7 - 9h, Antoine Marquis 9 - 12h, Paul-Aim 12 - 14h, Elie 14 - 17h   
Besoin de: Papier + stylo

Descriptif: Tu as un talkie, dès qu’un stand café a besoin de qqc, tu le notes sur une feuille en papier, le chariot est préparé en cuisine, dès qu’un 1 1A arrive, il emmène le chariot, tu barres sur la feuille.

Un thermos qui part = rappeler au 1A de ramener le thermos vide qui est remplacé!
""",
    "Audiovisuel":"""Lieu de rdv: QG

Respos:  Elisa (pour les trucs rencontre), Gab // Karina // Geliot 

Descriptif de perm: 
Appeler à 9h pour les café rencontre du matin: rdv 9h45 devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente 
Appeler à 15h pour les cafés rencontre du matin: rdv 15h45 devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente
Appeler à 11h30 (resp. 12h30) pour les dej rencontre: rdv 12h15 (resp. 13h15) devant salle Passy aux élèves concernés. Pas de rep 30min avant: liste attente 
Etat des lieux du matos audiovisuel + support MywayForum
""",
    "Production café":"""Lieu de rdv: en cuisine

Descriptif de perm: Faire du café, le mode d’emploi est sur le drive, dans Log 2023 -> J-2, J-1, jour J -> Descriptif de perm (page 29
""",
    "Restauration rapide":"""Lieu de Rdv: Zone restauration rapide (Passy = Zone Construction ///  Ternes = Finance, selon votre planning!)

Besoin de: Lydia Pro, tel chargé

Descriptif: 
Vente de repas aux étudiants: grâce au QR code billetterie
Vente de repas aux intervenants: grâce aux TPE à partir de 11h30 
Pour le staffeur au bout de la file étudiante: tu scannes leur QR achat  et tu écris SV si salade, S si sandwich sur le bracelet. 
Pour le staffeur qui sert la nourriture : tu regardes le bracelet avant de servir. 
Vente de repas aux intervenants: tu leur demandes leur tickets de caisse et tu leurs sers ce qu’ils demandent""",
    "Distribution Restauration Start Up":"""Lieu de rdv: vous êtes normalement déjà ensemble et avez réceptionné les pack bouffes

Descriptif: 
Vérifier que contenu de chaque sac = description etiquette sac (sinon: les échanger avec des repas ds les frigos pour que les packs soient corrects)
Les livrer sur les stands SU + livrer repas à la sécu et secouristes
""",
    "Vérification Restauration StartUp":"""Lieu de Rdv: Cuisine (vers le haut de la zone Conseil)

Descriptif: 
Réceptionner bouffe SU en gare de livraison
""",
    "Café Rencontre":"""Lieu de rdv: Salle Dej/Café Rencontre Passy, (en haut à gauche du plan)

Descriptif: Checkez identité de chaque étudiant à l’entrée
""",
    "Déjeuner Rencontre":"""Lieu de rdv: Salle Dej/Café Rencontre Passy, (en haut à gauche du plan)

Descriptif: 
Checkez identité de chaque étudiant à l’entrée
Renfort à Elisa et Corentin si besoin pour les repas Hyatt
""",
    "QG":"""Lieu de rdv: bah…le QG

Descriptif de perm: Aller au QG pour aider à n’importe quelle perm en rush (sans que ça soit le zoo autour de Clémence)
""",
    "QDS":"""Lieu de rdv: Point information (lequel? regardez votre planning)

Descriptif: Vous êtes en binôme (un fait remplir le QDS sur la tablette, l’autre démarche des étudiants). Si l’étudiant répond, vous lui donnez un cookie.
""",
    "Conférence":"""Lieu de rdv: Devant le vestiaire étudiant, à l’étage “0,5”

Descriptif: Orienter les gens vers la conf (Fondateur de BlablaCar), leur en parler. L’entrée est devant le vestiaire étudiant.
""",
    "Impressions documents QG":"""Lieu de Rdv: QG

Besoin de: ordi chargé

Descriptif: Imprimez les docs dont on a besoin (ayez les templates des badges prêts, whatsapp ouvert)
""",
    "Réception Dej Étudiant":"""Lieu de rdv: QG

Descriptif: Aller chercher commande et remplir les frigos des 2 zones restauration rapide

""",
    "Restauration Intervenant":"""Lieu de rdv: Salle dej/café rencontre (en haut à gauche du plan)

Descriptif de perm: Réguler l’entrée des intervenants, gérer les soucis de type échange de menu, etc.
""",
    "Point Info / QDS 1":"""Lieu de rdv: point info (lequel? Ça depende de votre planning!)

Descriptif: 
De 11h30 à 14h: vente de restauration rapide par TPE aux intervenants (ils doivent garder leur ticket de caisse!!)
Rediriger les gens
A partir de 15h: Faire remplir QDS en echange de cookies, parler du concours
""",
    "Désinstallation Plantes":""" """,
    "Préparation Palettes":""" """,
    "Ramassage Moquette Restante":"""""",
    "Ravitaillement Bombonne/Carafes":""" """,
    "[GIF] Déchargement Camion + Soute":""" """,
    "Zone":""" nsm"""
    }



for key in description_perms.keys():
    lignes = description_perms[key].splitlines()
    lignes_modifiees = [ligne + "<br />\n" for ligne in lignes]
    description_perms[key] = '\n'.join(lignes_modifiees)


def titre():
    logo = '/Users/kilianpouderoux/Documents/Forum/NDF/logo_forum.png'
    c.drawImage(logo, 1 * cm, height - 4.5 * cm, width=8 * cm, height=3 * cm, preserveAspectRatio=True, anchor='nw')
    

def personne(nom, adresse):
    texte = nom + "\n" + adresse
    a = texte.splitlines()
    c.setFont("Helvetica", 10)
    i = 0
    for line in a:
        c.drawString(50, 600 - 12*i, line)
        i+=1
        
        
def table_presta(database):
    table_presta = Table(database)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.ReportLabLightBlue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table_presta.setStyle(style)
    colWidths = [3*cm, 9*cm]
    rowHeights = 35*[0.55*cm]
    rowHeights[0] = 1.2*cm
    table_presta._argW = colWidths
    table_presta._argH= rowHeights
    
    table_presta.wrapOn(c, width, height)
    table_presta.drawOn(c, 120, 100)  # Ajustez ces valeurs selon vos besoins




def essai_table(database):
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.wordWrap = 'CJK'  # Permettre le word wrap
    largeur = 12*cm
    # Convertir les données en Paragraphs et estimer la hauteur de chaque ligne
    rowHeights = []
    for i, row in enumerate(database):
        max_height = 0
        for j, cell in enumerate(row):
            para = Paragraph(cell, styleN)
            database[i][j] = para
            # Calcule la largeur et la hauteur requises
            w, h = para.wrap(largeur, 0*cm)  # Largeur de la colonne et hauteur arbitraire
            max_height = max(max_height, h)
        rowHeights.append(max_height+12)  # Ajouter un peu de marge pour chaque ligne



    # Style de la table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'LTR')
    ])

    # Création de la table avec les hauteurs de ligne ajustées
    table = Table(database, colWidths=[7*cm, largeur], rowHeights=rowHeights, style=style)
    table.hAlign = 'LEFT'
    

    # Dessin de la table sur le canvas
    table.wrapOn(c, A4[0], A4[1])
    table.drawOn(c, 20, 100)  # Ajustez la position Y selon vos besoins


def numero_facture(texte):
    
    texte = "Planning pour " + texte
    # Définir le texte et sa position
    x, y = 250, 730  # Position du texte (et de l'encadré)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, texte)

def date():
    texte = "Mardi 21/11/2023 au Palais des Congrès "
    c.setFont("Helvetica", 12)
    c.drawString(260, height, texte)
    
def bas():
    texte =  "Si vous rencontrez un problème, appelez Clémence HAXAIRE au 06 24 54 13 34"
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, texte)

def bas2():
    texte =  "Amusez vous bien et force à vous, purrrrr"
    c.setFont("Helvetica", 8)
    c.drawString(50, 40, texte)


try:
    db = pd.read_csv("data.csv", sep=';', dtype=str)
except FileNotFoundError:
    print("La database est introuvable")
    quit()

liste_horaire = db["mardi 21/11"].tolist()

for col in db.columns[1:]:
    
    noms_cols = ["Horaire", "Staff"]
    liste_staff = db[col].tolist()
    liste_tr = [list(pair) for pair in zip(liste_horaire, liste_staff)]
    liste_tr.insert(0,noms_cols)
    nom = col

    # # définition du document
    output_file = str(nom) + ".pdf"
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4



    titre()
    date()
    numero_facture(col)
    bas()
    bas2()
    table_presta(liste_tr)
    
    
    liste_perms_trie = [] # le nom des perms
    liste_descriptif_inst = [] # la description des perms
    
    for i in range(0,len(db[col])):
        val = db[col][i]
        if val != 0:
            if val not in liste_perms_trie:
                print(val)
    
    
    
    for i in db[col]:
        if i != '0':
            
            if i not in liste_perms_trie:
                if "Stand Café" in i:
                    liste_descriptif_inst.append(description_perms["Stand Café"])
                    liste_perms_trie.append("Stand Café")
                elif "Zone" in i:
                    liste_descriptif_inst.append(description_perms["Zone"])
                    liste_perms_trie.append("Zone")
                else:
                    liste_perms_trie.append(i)
                    liste_descriptif_inst.append(description_perms[i])
            

    
    coucou = [list(pair) for pair in zip(liste_perms_trie, liste_descriptif_inst)]
    rajouter = ["Nom de la perm", "Description"]
    coucou.insert(0,rajouter)



    
    taille_sous_tableau = 6
    sous_tableaux = [coucou[i:i + taille_sous_tableau] for i in range(0, len(coucou), taille_sous_tableau)]

    for elt in sous_tableaux:
        c.showPage()
        essai_table(elt)    

    # Sauvegarder le PDF
    try: 
        c.save()
        print("Génération de "+ output_file + " terminée")
    except:
        print("Problème lors de la création du fichier pdf : " + output_file)
    
        