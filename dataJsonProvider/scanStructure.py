import os

def print_directory_structure(startpath):
    """
    Affiche l'arborescence des dossiers et fichiers à partir du répertoire donné.

    :param startpath: Chemin du répertoire de départ.
    """
    script_name = os.path.basename(__file__)
    previous_level = -1  # Pour suivre le niveau précédent et insérer des espaces correctement

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''

        # Affichage du dossier courant
        print(f"{indent}{os.path.basename(root)}/")

        # Affichage des fichiers
        subindent = '│   ' * level + '├── '
        for f in files:
            if f != script_name:  # Ignorer le fichier du script
                print(f"{subindent}{f}")

        # Insérer une ligne vide après chaque dossier de niveau 1 (avant de passer au prochain dossier de même niveau)
        if previous_level == 1 and level == 1:
            print("│   ")

        previous_level = level

# Chemin du répertoire de départ
startpath = "."  # Change ce chemin pour un autre répertoire si nécessaire

# Appel de la fonction pour afficher l'arborescence
print_directory_structure(startpath)
