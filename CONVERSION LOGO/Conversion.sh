#!/bin/bash
# script shell pour automatiser la conversion des logo SVG fournis par les entreprises vers le
# format PNG pour ensuite les recadrer et finalement faire les badges
# on utilise la bibliothèque rsvg-convert pour passer de SVG à PNG, elle est installée via homebrew

# Chemin vers le répertoire contenant les fichiers SVG
input_dir="/Users/kilianpouderoux/Desktop/FORUM/LOGO_SVG"

# Chemin vers le répertoire de sortie pour les fichiers PNG
output_dir="/Users/kilianpouderoux/Desktop/FORUM/LOGO_PNG"

# Hauteur souhaitée pour les fichiers PNG
height="1024"

# Vérifiez si le répertoire de sortie existe, sinon, créez-le
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Boucle à travers tous les fichiers SVG dans le répertoire d'entrée
for svg_file in "$input_dir"/*.svg; do
    if [ -f "$svg_file" ]; then
    # Obtenez le nom de base du fichier (sans extension)
    base_name=$(basename "$svg_file" .svg)

    # Chemin de sortie du fichier PNG
    png_output="$output_dir/$base_name.png"

    # Convertir le fichier SVG en PNG en utilisant rsvg-convert
    /opt/homebrew/bin/rsvg-convert -h "$height" "$svg_file" > "$png_output"

    echo "Converti $svg_file en $png_output"
    fi
done

# répertoire final où les images converties et rognées seront stockées
final_dir="/Users/kilianpouderoux/Desktop/FORUM/LOGO_PNG_CROP"

# Appel du script Python
python /Users/kilianpouderoux/Desktop/FORUM/crop.py "$output_dir" "$final_dir"

echo "Script Python terminé."


echo "Conversion terminée."
