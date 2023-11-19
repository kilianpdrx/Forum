import pandas as pd
from math import *
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm

def numero_facture(texte):
    
    texte = "FACTURE N° " + texte
    # Définir le texte et sa position
    x, y = 320, 750  # Position du texte (et de l'encadré)
    
    # Ajouter le texte en gras
    c.setFillColor(colors.black)  # Texte en blanc pour plus de visibilité
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, texte)

def titre():
    # c.setFont("Helvetica-Bold", 16)
    # titre = "Note de frais GIE FORUM CENTRALESUPELEC"
    # c.drawCentredString(width / 2+80, height - 2 * cm, titre)


    logo = '/Users/kilianpouderoux/Documents/Forum/NDF/logo_forum.png'
    c.drawImage(logo, 1 * cm, height - 4.5 * cm, width=8 * cm, height=3 * cm, preserveAspectRatio=True, anchor='nw')

def date():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    texte = "Gif-sur-Yvette, le " + formatted_date
    c.setFont("Helvetica", 12)
    c.drawString(350, 650, texte)

def aff_adresse_gie():
    c.setFont("Helvetica", 12)
    a = adresse_gie.splitlines()
    i = 0
    for line in a:
        c.drawString(400, 600 - 14*i, line)
        i+=1

def aff_contact_gie():
    c.setFont("Helvetica", 12)
    a = contact_gie.splitlines()
    i = 0
    for line in a:
        c.drawString(400, 550 - 14*i, line)
        i+=1

def aff_trucs_legaux():
    c.setFont("Helvetica", 12)
    a = trucs_legaux.splitlines()
    i = 0
    for line in a:
        c.drawString(400, 510 - 14*i, line)
        i+=1

def milieu(nom, adresse):
    texte = "Note de frais à l’attention de :\n" + nom + "\n" + adresse
    a = texte.splitlines()
    c.setFont("Helvetica-Bold", 16)
    i = 0
    for line in a:
        c.drawString(50, 600 - 14*i, line)
        i+=1

def personne(nom, adresse):
    texte = nom + "\n" + adresse
    a = texte.splitlines()
    c.setFont("Helvetica", 10)
    i = 0
    for line in a:
        c.drawString(50, 600 - 12*i, line)
        i+=1

def milieu():
    texte = "A l’attention de :"
    a = texte.splitlines()
    c.setFont("Helvetica", 12)
    i = 0
    for line in a:
        c.drawString(50, 620 - 14*i, line)
        i+=1

def remarque(texte):
    texte = "Remarque: " + texte
    a = texte.splitlines()
    c.setFont("Helvetica", 12)
    i = 0
    for line in a:
        c.drawString(70, 420 - 14*i, line)
        i+=1

def bas():
    texte =  "GIE Forum CentraleSupélec, 3 rue Joliot Curie, 91190, Gif-sur-Yvette, Tél : 01 75 31 72 60"
    c.setFont("Helvetica", 8)
    c.drawString(50, 50, texte)

def table_presta(database):
    table_presta = Table(database)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.ReportLabLightBlue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table_presta.setStyle(style)
    colWidths = [10*cm, 2*cm, 4*cm, 3*cm]
    table_presta._argW = colWidths
    table_presta.wrapOn(c, width, height)
    table_presta.drawOn(c, 20, 360)  # Ajustez ces valeurs selon vos besoins

def table_TVA(total_HT, total_TVA, total):
    
    prix = [["TOTAL HT", str(total_HT) + " €"],["TOTAL TVA ", str(total_TVA)  + " €"],["TOTAL TTC", str(total)  + " €"]]
    
    table_TVA = Table(prix)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ])
    table_TVA.setStyle(style)
    colWidths = [3*cm, 3*cm]
    table_TVA._argW = colWidths
    table_TVA.wrapOn(c, width, height)
    table_TVA.drawOn(c, 390, 280)  # Ajustez ces valeurs selon vos besoins


adresse_gie = """3 Rue Joliot Curie 
Plateau du Moulon 
91190 Gif-sur-Yvette"""

contact_gie = """Tel : 01 75 31 72 60
Email : contact@forum-cs.fr"""

trucs_legaux = """N°SIRET : 524 920 220 00026                                                                                                  
N°TVA : FR10524920220 
Code APE : 82.30.Z"""


# ouverture de la database
try:
    db = pd.read_excel("data.xlsx", dtype=str)
except FileNotFoundError:
    print("La database est introuvable")
    quit()


grouped_db = db.groupby('Numero')


for group_name, group_data in grouped_db:
    num_fact = group_name
    prestation_data = []
    texte_remarque = ""
    destinataire = group_data["Destinataire"].iloc[0]


    destinataire = destinataire[0]

    TVA_total = 0
    prix_total = 0
    HT_total = 0
    
    for index, row in group_data.iterrows():
        if row["Générer"] == "OUI":
            prestation_data.append([row['Prestation'], row['Quantite'], row["Prix unitaire HT"], row["TVA"]])
            
            texte_remarque = texte_remarque + "\n" + row["Remarque"]
            prix_HT = round(int(row['Prix unitaire HT']),2)
            taux_TVA = round(float(row["TVA"]),2)
            quantite = float(row["Quantite"])
            
            TVA_total += round(quantite*prix_HT*taux_TVA/100,2)
            HT_total += round(quantite*prix_HT,2)
        elif row["Générer"] == "NON":
            pass
        else:
            print("La valeur de la colonne Générer pour la ligne "+str(index+1)+" doit être OUI ou NON")
            quit()

        prix_total = TVA_total + HT_total
    if prestation_data != []:
        prestation_data.insert(0,['Prestation', 'Quantité', 'Prix unitaire HT €', 'TVA %'])

        output_file = str(db["Destinataire"][index]) +"_"+ str(num_fact) + ".pdf"
        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4
        
        titre()
        date()
        aff_trucs_legaux()
        aff_contact_gie()
        aff_adresse_gie()
        remarque(texte_remarque)
        milieu()
        personne(destinataire, "1 rue Joliot Curie\n91190 Gif-sur-Yvette")
        numero_facture(num_fact)
        bas()
        table_presta(prestation_data)
        table_TVA(HT_total, TVA_total, prix_total)
        
        try: 
            c.save()
            print("Génération de "+ output_file + " terminée")
        except:
            print("Problème lors de la création du fichier pdf : " + output_file)




# for index, row in db.iterrows():
#     faire = row["Générer"]
#     if faire == "OUI":
        
#         # on prend juste les colonnes utiles pour le pdf
#         modif = row[['Prestation', 'Quantite', 'Prix unitaire HT', 'TVA']]
#         texte_remarque = row["Remarque"]
#         num_fact = row["Numero"]

#         # récupération des données et calcul des prix à afficher
#         prix_HT = round(int(modif['Prix unitaire HT']),2)
#         taux_TVA = round(float(row["TVA"]),2)
#         quantite = float(row["Quantite"])

        
        
#         total_HT = round(quantite*prix_HT,2)
#         total_TVA = round(taux_TVA/100*total_HT,2)
#         total = round(total_HT + total_TVA,2)


#         # on met sous le bon format pour afficher
#         modif['Prix unitaire HT'] = modif['Prix unitaire HT'] + " €"
#         modif['TVA'] = modif['TVA'] + " %"

#         modif2 = [modif.index.tolist()] + [modif.values.tolist()]

#         # définition du document
#         output_file = str(db["Destinataire"][index]) +"_"+ str(num_fact) + ".pdf"
#         c = canvas.Canvas(output_file, pagesize=A4)
#         width, height = A4


#         # affichage sur le canvas
#         titre()
#         date()
#         aff_trucs_legaux()
#         aff_contact_gie()
#         aff_adresse_gie()
#         remarque(texte_remarque)
#         milieu()
#         personne(row["Destinataire"], "1 rue Joliot Curie\n91190 Gif-sur-Yvette")
#         numero_facture(str(num_fact))
#         bas()
#         table_presta(modif2)
#         table_TVA()


#         # Sauvegarder le PDF
#         try: 
#             c.save()
#             print("Génération de "+ output_file + " terminée")
#         except:
#             print("Problème lors de la création du fichier pdf : " + output_file)
#     elif faire == "NON":
#         pass
#     else:
#         print("La valeur de la colonne Générer pour la ligne "+str(index+1)+" doit être OUI ou NON")


