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


def numero_facture(texte):
    
    texte = "Planning pour " + texte
    # Définir le texte et sa position
    x, y = 250, 730  # Position du texte (et de l'encadré)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, texte)

def date():
    texte = "Mardi 21/11/2023 au Palais des Congrès "
    c.setFont("Helvetica", 12)
    c.drawString(260, 710, texte)
    
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


    # Sauvegarder le PDF
    try: 
        c.save()
        print("Génération de "+ output_file + " terminée")
    except:
        print("Problème lors de la création du fichier pdf : " + output_file)
        