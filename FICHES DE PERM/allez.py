import pandas as pd
from math import *
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm


def titre():
    # c.setFont("Helvetica-Bold", 16)
    # titre = "Note de frais GIE FORUM CENTRALESUPELEC"
    # c.drawCentredString(width / 2+80, height - 2 * cm, titre)


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
    table_presta = Table(modif2)
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
    colWidths = [12*cm, 3*cm, 3*cm]
    table_presta._argW = colWidths
    table_presta.wrapOn(c, width, height)
    table_presta.drawOn(c, 50, 360)  # Ajustez ces valeurs selon vos besoins


try:
    db = pd.read_csv("data.csv", sep=';', dtype=str)
except FileNotFoundError:
    print("La database est introuvable")
    quit()



for col in db.columns:
    

    modif = [db["mardi 21/11"].tolist(), db[col].tolist()]
    nom = col
    print(nom)

    # # on prend juste les colonnes utiles pour le pdf
    # modif = row[['Prestation', 'Quantite', 'Prix unitaire HT']]


    # # récupération des données et calcul des prix à afficher
    # prix_HT = round(int(modif['Prix unitaire HT']),2)
    # taux_TVA = round(float(row["TVA"]),2)
    # quantite = float(row["Quantite"])
    # num_fact = row["Numero"]
    
    # total_HT = round(quantite*prix_HT,2)
    # total_TVA = round(taux_TVA/100*total_HT,2)
    # total = round(total_HT + total_TVA,2)


    # # on met sous le bon format pour afficher
    # modif['Prix unitaire HT'] = modif['Prix unitaire HT'] + " €"
    # modif2 = [modif.index.tolist()] + [modif.values.tolist()]

    # # définition du document
    output_file = "essai.pdf"
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4



    # # affichage sur le canvas
    # titre()
    # date()
    # aff_trucs_legaux()
    # aff_contact_gie()
    # aff_adresse_gie()
    # milieu()
    # personne(row["Destinataire"], "1 rue Joliot Curie\n91190 Gif-sur-Yvette")
    # numero_facture(str(num_fact))
    # bas()
    # table_presta(modif2)
    # table_TVA(modif2)


    # # Sauvegarder le PDF
    # try: 
    #     c.save()
    #     print("Génération de "+ output_file + " terminée")
    # except:
    #     print("Problème lors de la création du fichier pdf : " + output_file)