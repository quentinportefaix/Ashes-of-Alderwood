# 🗡️ L'Héritage des Cendres - Ashes of Alderwood
![WhatsApp Image 2026-01-24 at 17 50 34](https://github.com/user-attachments/assets/c2642a51-cce4-4771-a82c-37495422f9b0)


Jeu d'aventure textuel (Text-Based RPG) développé en Python, où vous incarnez le dernier survivant du village d'Alderwood, détruit par les armées de Morgrath.

# 📖 Guide Utilisateur

# 🎮 Présentation du Jeu

L'Héritage des Cendres est un jeu de rôle narratif en ligne de commande se déroulant dans un univers médiéval-fantastique sombre. 

Cinq ans après la destruction de votre village, votre quête de vengeance commence - mais le chemin est semé d'embûches, de choix moraux et d'alliés inattendus.

# 🌍 Univers & Scénario

Acte 1 – La Fuite : Échapper à la destruction du village en flammes

Acte 2 – L'Entraînement : 5 ans plus tard, choisir votre voie et vous préparer au combat

Acte 3 – La Vengeance (à venir) : Affronter Morgrath dans son antre

# L'histoire est portée par :

Des PNJ complexes (mentors, alliés, ennemis)

Un système de quêtes scénarisées

Des choix de gameplay influençant les combats et l'histoire

# 🏆 Conditions de Victoire / Défaite

# Victoire : ![WhatsApp Image 2026-01-24 at 18 29 09](https://github.com/user-attachments/assets/c7d4e8dd-0574-4d02-b131-82981b1cadab)


✅ Terminer la quête "La Chute du Roi Démon"

✅ Vaincre Morgrath dans un combat épique

✅ Survivre aux épreuves finales

# Défaite :
![WhatsApp Image 2026-01-24 at 18 29 09 (1)](https://github.com/user-attachments/assets/98c240e0-e9c2-40fd-b891-52946880a9a3)


❌ Points de vie à zéro

❌ Choix narratifs mortels (sauter par la fenêtre, affronter prématurément)

❌ Échec dans les combats clés

# 🧙‍♂️ Le Personnage Joueur

Votre personnage possède :

Points de vie : 50 PV maximum

Inventaire : Armes, armures, objets

# Voie de combat à choisir :

ARC → Précision et coups critiques

ÉPÉE → Force et dégâts constants

MAGIE → Puissance et effets spéciaux

# ⚔️ Système de Combat

Tour par tour avec dégâts calculés selon votre voie

Équipement influençant les dégâts et la défense

Effets spéciaux : brûlure magique, esquive, coup critique

Combat contre Morgrath en deux phases avec pouvoir caché

# 📜 Système de Quêtes

5 quêtes principales avec :

Narration immersive et objectifs progressifs

Récompenses : XP, or, objets

Progression automatique d'une quête à l'autre

Journal de quêtes accessible via commande

# ⌨️ Commandes Disponibles

# Navigation

Commande	Alias	Description

go <direction>	aller	Se déplacer

back	retour	Revenir en arrière

history	historique	Voir l'historique

# Observation

Commande	Alias	Description

look	observer	Observer la pièce

check	inventaire, stats	Voir inventaire/stats

# Interaction

Commande	Alias	Description

take <objet>	prendre	Prendre un objet

drop <objet>	poser	Déposer un objet

talk <pnj>	parler	Parler à un PNJ

fight <ennemi>	combattre	Combattre un ennemi

# Développement

Commande	Alias	Description

choose <voie>	choisir	Choisir sa voie (arc/épée/magie)

quests	quetes, journal	Voir les quêtes

debug	-	Mode développeur

# Utilitaires

Commande	Alias	Description

help	aide	Afficher l'aide

quit	quitter	Quitter le jeu

# Directions acceptées : 
N, S, E, O, PORTE, FENETRE, GAUCHE, DROITE, CONTINUER, RETOUR, FORET, ENTRAINEMENT, VENGEANCE, VALLEE, etc.

# ▶️ Installation et Lancement
Prérequis
Python 3.7 ou supérieur

Aucune bibliothèque externe requise

Installation
Téléchargez tous les fichiers du projet

Placez-les dans un même dossier

Assurez-vous que les fichiers suivants sont présents :

game.py (fichier principal)

player.py

room.py

actions.py

command.py

character.py

enemy.py

item.py

quest.py

Lancement du Jeu
bash
# Version console (recommandée)
python game.py
🎯 Comment Jouer
Démarrage : Le jeu commence automatiquement avec une introduction

Création du personnage : Entrez votre nom

Découverte : Explorez les pièces avec les commandes go

Progression : Suivez les quêtes et interagissez avec les PNJ

Choix stratégique : Utilisez choose pour sélectionner votre voie

Combat : Affrontez les ennemis avec fight

Final : Atteignez l'antre de Morgrath pour l'affrontement final

# 👨‍💻 Guide Développeur

📁 Structure des Fichiers

text

Ashes-of-Alderwood/

├── game.py          # Moteur principal du jeu

├── player.py        # Classe du joueur

├── room.py          # Système de pièces

├── actions.py       # Toutes les actions du jeu

├── command.py       # Système de commandes

├── character.py     # PNJ et dialogues

├── enemy.py         # Système d'ennemis

├── item.py          # Objets et équipement

├── quest.py         # Système de quêtes

└── README.md        # Documentation

# 🧱 Architecture du Code

Diagramme de Classes

<img width="4704" height="6133" alt="deepseek_mermaid_20260125_eb18d4" src="https://github.com/user-attachments/assets/458ad916-fbbe-44bb-ab94-5d95e01701a1" />




