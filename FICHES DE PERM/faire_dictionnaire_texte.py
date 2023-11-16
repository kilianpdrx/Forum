"""Pour faire la string modifiée dans le format dictionnaire"""


import pandas as pd

try:
    db = pd.read_csv("les perms.csv", sep=';', dtype=str)
except FileNotFoundError:
    print("La database est introuvable")
    quit()
    


result_str = ""
for index, row in db.iterrows():
    nom_perm = row['nom']
    desc_perm = row['des'] if pd.notnull(row['des']) else ''
    result_str += f'"{nom_perm}": """{desc_perm}""",\n'
    

fin = open("fino.txt", "w")
fin.write(result_str)