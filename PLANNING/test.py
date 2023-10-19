# a améliorer : le perm max par personne, faire les range de valeurs avec des variable pour pas changer à la main

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import copy
import numpy as np
import pandas as pd


# Authentification
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/kilianpouderoux/Desktop/FORUM/planning-bp2023-e39bcaf9e87c.json', scope)
client = gspread.authorize(creds)

# Ouvrir le Google Sheet
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1DOQUunYUbUmvxStN0vJnJ21EriGaKTDxW_7QJn1Eto0/edit#gid=199087720').worksheet('Mercredi 04/10')

# Récupérer les disponibilités
range_availability = 'A318:L472'
availability = sheet.range(range_availability)

# Créer des listes pour stocker les personnes disponibles par créneau horaire
nombre_creneaux = 11
available_people = {i: [] for i in range(1, nombre_creneaux+1)}

# Compter le nombre de créneaux assignés à chaque personne
assigned_counts = {}

# pour compter le nombre de perms par personne
for cell in availability:
    person_name = cell.value
    if person_name not in assigned_counts:
        assigned_counts[person_name] = 0
assigned_counts_2A = {cle: valeur for cle, valeur in assigned_counts.items() if "[2A]" in cle}
assigned_counts_1A = {cle: valeur for cle, valeur in assigned_counts.items() if "[2A]" not in cle}




# on remplit le dictionnaire par colonne avec les disponibilités par colonne
for row in range(0, len(availability), nombre_creneaux+1):
    person_name = availability[row].value
    for col in range(1, nombre_creneaux+1):
        cell_value = availability[row+col].value
        if cell_value == 'OUI':
            available_people[col].append(person_name)



# Lire toutes les données du planning en une seule fois
range_perms = 'B2:L157'
taille_data = 156 # on fait ligne bas - ligne haut + 1 (exemple B2:U151 : 151 - 2 + 1 = 150)

all_data_base = sheet.range(range_perms) # préciser le range des perms
new_data = np.array(all_data_base)
all_data = new_data.reshape(taille_data, nombre_creneaux) # on passe en numpy pour modifier les valeurs plus simplement

exporter = np.empty((taille_data, nombre_creneaux), dtype='U200')
exporter.fill("")

column_a_data = sheet.col_values(1)[1:taille_data+1] # Récupérer les valeurs de la colonne A (les perms)
updated_cells = []



for col in range(0,nombre_creneaux):
    available_for_this_col = copy.deepcopy(available_people[col+1])
    available_for_this_col_2A = [person for person in available_for_this_col if '[2A]' in person] # on sépare en groupes de 1A et 2A disponibles
    available_for_this_col_1A = [person for person in available_for_this_col if '[2A]' not in person]


    for row in range(0,taille_data):
        cell = all_data[row][col]
        if cell.value != '0':  # Si la cellule doit être remplie
            if '[2A]' in column_a_data[row]: # si le nom de la perm a le tag [2A] dedans, on ne remplit ces perms qu'avec des 2A
                if len(available_for_this_col_2A) !=0:
                    
                    # on essaye de remplir les perms de manière équitable pour que tout le monde aie à peu près le même nombre de perms
                    inst = {cle: valeur for cle, valeur in assigned_counts_2A.items() if cle in available_for_this_col_2A}
                    min_val = min(inst.values())
                    noms_min_valeur = [nom for nom, valeur in inst.items() if valeur == min_val]
                    person = random.choice(noms_min_valeur)
                    
                    cell_value = person
                    available_for_this_col_2A.remove(person)
                    assigned_counts_2A[person]+=1
                else:
                    person="PAS ASSEZ" # si il n'y a pas assez de monde
                    cell_value = person
                    
            else: # si le nom de la perm n'a pas le tag [2A] dedans, on ne remplit ces perms qu'avec des 1A
                if len(available_for_this_col_1A) !=0:
                    
                    # on essaye de remplir les perms de manière équitable pour que tout le monde aie à peu près le même nombre de perms
                    inst = {cle: valeur for cle, valeur in assigned_counts_1A.items() if cle in available_for_this_col_1A}
                    min_val = min(inst.values())
                    noms_min_valeur = [nom for nom, valeur in inst.items() if valeur == min_val]
                    person = random.choice(noms_min_valeur)
                    
                    cell_value = person
                    available_for_this_col_1A.remove(person)
                    assigned_counts_1A[person]+=1
                else:
                    person="PAS ASSEZ" # si il n'y a pas assez de monde
                    cell_value = person
                
            updated_cells.append(gspread.Cell(row + 2, col + 2, cell_value))
            exporter[row][col] = person




dataframe = pd.DataFrame(exporter)

# Spécifiez le nom du fichier Excel de sortie
nom_fichier_excel = 'essai.xlsx'

# Exportez le DataFrame vers un fichier Excel
dataframe.to_excel(nom_fichier_excel, index=False) 



# Mettez à jour la feuille de calcul avec les cellules mises à jour
sheet.update_cells(updated_cells)
print("Planning mis à jour!")

