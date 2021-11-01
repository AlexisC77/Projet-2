# Projet-2

bonjour! Ce document a pour objectif de vous expliquer comment utiliser ce programme de scraping!

Tout d'abord, assurer vous que python est installé sur votre appareil dans une version assez récente (supérieure à 3.4) ensuite, allez dans votre terminal et placez vous dans le dossier contenant le script et le fichier requirements.txt, et créer votre environnement virtuel (tapez "python -m venv env" si vous utilisez venv) ensuite, activez cette environnement (tapez "source env/bin/activate" si vous utilisez venv) puis installez les paquets python contenus dans le fichier requirements.txt (tapez "pip install -r requirements.txt")

vous pouvez maintenant éxécuter le programme en tapant "python scraping.py" ou en allez l'éxécuter manuellement directement dans python ou dans votre IDE, ce programme créera des dossiers pour chacunes des catégories du site contenant les images des livres et un fichier .csv contenant les information.

Attention à ne pas ouvrir les fichiers .csv avant que la catégories correspondante ne soit finit! (le programme vous en informera) Si toutefois cela vous arrive pas de panique et relancez le programme, si vous avez le moindre problème n'hésitez pas à me contacter au plus vite pour que nous corrigions cela dans les plus brefs delais.

Si vous avez un problème avec l'éxecution du code vous pouvez le relancez en modifiant la ligne numéro 8, celle ci contrôle la catégorie par laquel commence le programme, remplacez le nombre par le dernier nombre donné par le script pour recommencer depuis la dernière catégorie en cours, si vous souhaitez que le programme parcourt toutes les catégories rentrez le chiffre 1 à la place (chiffre par défault)

quand vous ouvrez le fichier .csv assurez vous que la virgule (",") est compris dans les séparateurs
