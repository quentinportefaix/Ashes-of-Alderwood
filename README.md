🗡️ L'Héritage des Cendres - Ashes of Alderwood

Jeu d'aventure textuel (Text-Based RPG) développé en Python, où vous incarnez le dernier survivant du village d'Alderwood, détruit par les armées de Morgrath.

📖 Guide Utilisateur

🎮 Présentation du Jeu

L'Héritage des Cendres est un jeu de rôle narratif en ligne de commande se déroulant dans un univers médiéval-fantastique sombre. 

Cinq ans après la destruction de votre village, votre quête de vengeance commence - mais le chemin est semé d'embûches, de choix moraux et d'alliés inattendus.

🌍 Univers & Scénario

Acte 1 – La Fuite : Échapper à la destruction du village en flammes

Acte 2 – L'Entraînement : 5 ans plus tard, choisir votre voie et vous préparer au combat

Acte 3 – La Vengeance (à venir) : Affronter Morgrath dans son antre

L'histoire est portée par :

Des PNJ complexes (mentors, alliés, ennemis)

Un système de quêtes scénarisées

Des choix de gameplay influençant les combats et l'histoire

🏆 Conditions de Victoire / Défaite

Victoire :

Terminer la quête "La Chute du Roi Démon"

Vaincre Morgrath dans un combat épique

Survivre aux épreuves finales

Défaite :

Points de vie à zéro

Choix narratifs mortels (sauter par la fenêtre, affronter prématurément)

Échec dans les combats clés

🧙‍♂️ Le Personnage Joueur

Votre personnage possède :

Points de vie : 50 PV maximum

Inventaire : Armes, armures, objets

Voie de combat à choisir :

ARC → Précision et coups critiques

ÉPÉE → Force et dégâts constants

MAGIE → Puissance et effets spéciaux

⚔️ Système de Combat

Tour par tour avec dégâts calculés selon votre voie

Équipement influençant les dégâts et la défense

Effets spéciaux : brûlure magique, esquive, coup critique

Combat contre Morgrath en deux phases avec pouvoir caché

📜 Système de Quêtes

5 quêtes principales avec :

Narration immersive et objectifs progressifs

Récompenses : XP, or, objets

Progression automatique d'une quête à l'autre

Journal de quêtes accessible via commande

⌨️ Commandes Disponibles

Navigation

Commande	Alias	Description

go <direction>	aller	Se déplacer

back	retour	Revenir en arrière

history	historique	Voir l'historique

Observation

Commande	Alias	Description

look	observer	Observer la pièce

check	inventaire, stats	Voir inventaire/stats

Interaction

Commande	Alias	Description

take <objet>	prendre	Prendre un objet

drop <objet>	poser	Déposer un objet

talk <pnj>	parler	Parler à un PNJ

fight <ennemi>	combattre	Combattre un ennemi

Développement

Commande	Alias	Description

choose <voie>	choisir	Choisir sa voie (arc/épée/magie)

quests	quetes, journal	Voir les quêtes

debug	-	Mode développeur

Utilitaires

Commande	Alias	Description

help	aide	Afficher l'aide

quit	quitter	Quitter le jeu

Directions acceptées : N, S, E, O, PORTE, FENETRE, GAUCHE, DROITE, CONTINUER, RETOUR, FORET, ENTRAINEMENT, VENGEANCE, VALLEE, etc.

▶️ Installation et Lancement
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

👨‍💻 Guide Développeur

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

🧱 Architecture du Code

Diagramme de Classes

classDiagram
    class Game {
        +Player player
        +dict rooms
        +dict commands
        +QuestManager quest_manager
        +bool finished
        +int turn_count
        +setup()
        +play()
        +process_command()
        +update_game_state()
    }

    class Player {
        +str name
        +Room current_room
        +list history
        +dict stats
        +int health
        +dict inventory
        +str chosen_path
        +move()
        +attack()
        +defend()
        +choose_path()
    }

    class Room {
        +str name
        +str description
        +dict exits
        +dict inventory
        +dict enemies
        +dict characters
        +get_long_description()
        +add_item()
        +remove_item()
    }

    class Command {
        +str command_word
        +str help_string
        +function action
        +int number_of_parameters
    }

    class Actions {
        +go()
        +quit()
        +help()
        +fight()
        +talk()
        +choose()
        +take()
        +drop()
    }

    class Character {
        +str name
        +str description
        +Room current_room
        +list dialogue_lines
        +str character_type
        +get_dialogue()
        +move()
    }

    class Enemy {
        +str name
        +int health
        +int max_health
        +int base_damage
        +str enemy_type
        +take_damage()
        +calculate_damage()
        +drop_loot()
    }

    class Item {
        +str name
        +str description
        +str item_type
        +int value
        +float weight
    }

    class Weapon {
        +int damage_bonus
        +str weapon_type
        +int magic_bonus
        +int critical_chance
    }

    class Armor {
        +int defense_bonus
        +str armor_type
        +int dodge_penalty
        +int magic_resistance
    }

    class Quest {
        +str quest_id
        +str title
        +str description
        +list objectives
        +dict reward
        +start()
        +complete_objective()
        +complete_quest()
    }

    class QuestManager {
        +Player player
        +dict all_quests
        +list active_quests
        +list completed_quests
        +start_quest()
        +complete_objective()
        +check_quest_triggers()
    }

    Game --> Player : contient
    Game --> Room : contient
    Game --> Command : utilise
    Game --> QuestManager : contient
    Player --> Room : référence
    Player --> Item : possède
    Room --> Character : contient
    Room --> Enemy : contient
    Actions --> Game : manipule
    QuestManager --> Quest : gère
    Weapon --|> Item : hérite
    Armor --|> Item : hérite



