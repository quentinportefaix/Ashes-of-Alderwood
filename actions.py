# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

# Variable de debug
DEBUG = True # Mettre à False pour désactiver les messages de debug

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter can be any valid direction (N, S, E, O, U, D, PORTE, GAUCHE, etc.)

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "PORTE"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words and convert to uppercase
        direction_input = list_of_words[1].upper()
        
        # Map des directions variantes
        direction_map = {
            # Directions cardinales français/anglais
            "NORD": "N", "NORTH": "N",
            "SUD": "S", "SOUTH": "S", 
            "EST": "E", "EAST": "E",
            "OUEST": "O", "WEST": "O",
            # Directions verticales
            "HAUT": "U", "UP": "U", "MONTER": "U",
            "BAS": "D", "DOWN": "D", "DESCENDRE": "D",
            # Directions spéciales de notre jeu
            "PORTE": "PORTE", "DOOR": "PORTE",
            "FENETRE": "FENETRE", "WINDOW": "FENETRE",
            "GAUCHE": "GAUCHE", "LEFT": "GAUCHE",
            "DROITE": "DROITE", "RIGHT": "DROITE", 
            "CENTRE": "CENTRE", "CENTER": "CENTRE",
            "FUIR": "FUIR", "FLEE": "FUIR",
            "CONTINUER": "CONTINUER", "CONTINUE": "CONTINUER",
            "ENTRAINEMENT": "ENTRAINEMENT", "TRAINING": "ENTRAINEMENT",
            "FORET": "FORET", "FOREST": "FORET",
            "CLAIRIERE": "CLAIRIERE", "CLEARING": "CLAIRIERE",
            "VENGEANCE": "VENGEANCE", "REVENGE": "VENGEANCE",
            "PORTE": "PORTE", "GATE": "PORTE",
            "TUNNELS": "TUNNELS", "TUNNELS": "TUNNELS",
            "ENTRER": "ENTRER", "ENTER": "ENTRER",
            "SORTIR": "SORTIR", "EXIT": "SORTIR",
            "INFO": "INFO", "INFORMATION": "INFO",
            "ASSAUT": "ASSAUT", "ASSAULT": "ASSAUT",
            "INFILTRATION": "INFILTRATION", "INFILTRATE": "INFILTRATION",
            "PRISON": "PRISON", "JAIL": "PRISON",
            "TRESOR": "TRESOR", "TREASURE": "TRESOR",
            "LIBERER": "LIBERER", "FREE": "LIBERER",
            "PONT": "PONT", "BRIDGE": "PONT",
            "RIVIERE": "RIVIERE", "RIVER": "RIVIERE",
            "ANTRE": "ANTRE", "LAIR": "ANTRE",
            "VICTOIRE": "VICTOIRE", "VICTORY": "VICTOIRE",
            "MONTEE": "MONTEE", "ASCEND": "MONTEE",
            "COMBATTRE": "COMBATTRE", "FIGHT": "COMBATTRE",
            "RETOUR": "RETOUR", "BACK": "RETOUR"
        }
        
        # Convertir la direction en format standard
        direction = direction_map.get(direction_input, direction_input)
        
        # Vérifier si la direction est autorisée
        if direction not in game.allowed_directions:
            print(f"\nDirection '{direction_input}' non reconnue ou impossible.\n")
            print(f"Directions possibles depuis ici : {', '.join(game.player.current_room.exits.keys())}\n")
            return False

        # Vérifier si la direction existe dans les exits
        if direction not in game.player.current_room.exits:
            print(f"\nImpossible d'aller dans cette direction.\n")
            print(f"Directions possibles depuis ici : {', '.join(game.player.current_room.exits.keys())}\n")
            return False

        # Vérifier si la direction mène à une room None (game over ou chemin bloqué)
        if game.player.current_room.exits[direction] is None:
            if direction == "FENETRE":
                print("\n" + "="*50)
                print("GAME OVER")
                print("="*50)
                print("Vous sautez par la fenêtre et tombez de deux étages...")
                print("La chute vous brise les jambes. Des orcs vous achèvent au sol.")
                print("✗ Parfois, la bravoure n'est que de l'imprudence.")
                print("="*50)
                game.finished = True
            elif direction == "DROITE":
                print("\n" + "="*50)
                print("GAME OVER") 
                print("="*50)
                print("Vous tombez nez à nez avec un orc massif...")
                print("Sa hache s'abat sur vous avant même que vous puissiez réagir.")
                print("✗ L'observation avant l'action aurait été plus sage.")
                print("="*50)
                game.finished = True
            else:
                print(f"\nImpossible d'aller dans cette direction. Le chemin est bloqué.\n")
            return False

        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué à 'Ashes of Alderwood'. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\n" + "="*50)
        print("COMMANDES DISPONIBLES - Ashes of Alderwood")
        print("="*50)
        for command in game.commands.values():
            print(" " + str(command))
        print("\nDirections possibles :")
        print(" - Cardinales : N, S, E, O (ou NORD, SUD, EST, OUEST)")
        print(" - Verticales : U, D (ou HAUT, BAS, MONTER, DESCENDRE)") 
        print(" - Spéciales : PORTE, FENETRE, GAUCHE, DROITE, FUIR, etc.")
        print("\nNavigation :")
        print(" - 'back' pour revenir en arrière")
        print(" - 'history' pour voir votre parcours")
        print("\nInventaire :")
        print(" - 'look' pour observer la pièce")
        print(" - 'take <objet>' pour prendre un objet")
        print(" - 'drop <objet>' pour déposer un objet") 
        print(" - 'check' pour vérifier votre inventaire")
        print("\nCombat :")
        print(" - 'fight <ennemi>' pour attaquer un ennemi")
        print("\nInteraction :")
        print(" - 'talk <personnage>' pour parler à un PNJ")
        print("\nQuêtes :")
        print(" - 'quests' pour voir vos quêtes")
        print(" - 'start <quête>' pour démarrer une quête")
        if DEBUG:
            print(" - 'debug' pour les informations de développement")
        print("="*50)
        return True

    def back(game, list_of_words, number_of_parameters):
        """
        Revenir à la pièce précédente dans l'historique.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        
        # Vérifier si l'historique n'est pas vide
        if not player.history:
            print("\nVous êtes déjà au point de départ. Aucun historique de déplacement.\n")
            return False
        
        # Récupérer la dernière pièce visitée
        previous_room = player.history.pop()
        player.current_room = previous_room
        
        print(f"\nVous revenez sur vos pas...")
        print(previous_room.get_long_description())
        
        # Afficher l'historique mis à jour
        if player.history:
            print(player.get_history())
        else:
            print("\nVous êtes de retour au point de départ.\n")
            
        return True

    def history(game, list_of_words, number_of_parameters):
        """
        Afficher l'historique des pièces visitées.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(player.get_history())
        return True

    def look(game, list_of_words, number_of_parameters):
        """
        Observer attentivement la pièce actuelle.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        
        print(f"\n=== {current_room.name.upper()} ===")
        print(f"Description: {current_room.description}")
        print(f"\n{current_room.get_exit_string()}")
        
        # Afficher les objets dans la pièce
        if current_room.inventory:
            print(f"\n{current_room.get_items_string()}")
        else:
            print(f"\nIl n'y a rien d'intéressant ici.")
            
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        Prendre un objet dans la pièce actuelle.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        item_name = list_of_words[1].lower()
        
        # Vérifier si l'objet existe dans la pièce
        if item_name not in current_room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans cette pièce.")
            print(f"Objets disponibles: {', '.join(current_room.inventory.keys())}\n")
            return False
        
        # Prendre l'objet
        item = current_room.remove_item(item_name)
        player.add_item(item_name, item)
        
        print(f"\nVous avez pris : {item}")
        return True

    def drop(game, list_of_words, number_of_parameters):
        """
        Déposer un objet de votre inventaire dans la pièce actuelle.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        item_name = list_of_words[1].lower()
        
        # Vérifier si l'objet existe dans l'inventaire du joueur
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.")
            print(f"Votre inventaire: {', '.join(player.inventory.keys())}\n")
            return False
        
        # Déposer l'objet
        item = player.remove_item(item_name)
        current_room.add_item(item_name, item)
        
        print(f"\nVous avez déposé : {item}")
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Vérifier le contenu de votre inventaire.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(f"\n=== INVENTAIRE DE {player.name.upper()} ===")
        print(player.get_inventory_string())
        
        # Afficher l'équipement actuel
        if player.equipped_weapon:
            print(f"\nArme équipée: {player.equipped_weapon}")
        else:
            print(f"\nArme équipée: Aucune")
            
        if player.equipped_armor:
            print(f"Armure équipée: {player.equipped_armor}")
        else:
            print(f"Armure équipée: Aucune")
            
        print(f"\nOr: {player.gold} pièces")
        print(f"PV: {player.health}/{player.max_health}")
        
        return True

    # REMPLACER LA MÉTHODE fight() EXISTANTE PAR CECI DANS actions.py

    def fight(game, list_of_words, number_of_parameters):
        """
        Engager un combat avec un ennemi dans la pièce.
        Détecte si c'est Morgrath pour activer le combat spécial.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        import random
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        enemy_name = list_of_words[1].lower()

        # Vérifier si le joueur a choisi une voie
        if not player.chosen_path:
            print("\n⚠️ Vous devez d'abord choisir une voie (arc, épée ou magie) avant de combattre !")
            return False
        
        # Pour la scène spéciale de la rencontre ORC
        if current_room.name == "Rencontre Fatale":
            print("\n" + "="*50)
            print("COMBAT CONTRE UN ORC MASSIF")
            print("="*50)
            print("\nVous n'êtes pas prêt pour affronter cet orc seul !")
            print("Vous devriez fuir tant que vous le pouvez...")
            print("Cet orc vous écrase de sa présence...")
            print("\n⚠️ INSTRUCTION: Tapez 'back' pour vous échapper !")
            print("="*50)
            return False
        
        # Vérifier si l'ennemi existe dans la pièce
        if enemy_name not in current_room.enemies:
            print(f"\nL'ennemi '{enemy_name}' n'est pas dans cette pièce.")
            if current_room.enemies:
                print(f"Ennemis présents: {', '.join(current_room.enemies.keys())}")
            else:
                print("Aucun ennemi dans cette pièce.")
            return False
        
        enemy = current_room.enemies[enemy_name]
        
        # COMBAT SPÉCIAL CONTRE MORGRATH
        if enemy_name == "morgrath":
            return Actions._fight_morgrath_combat(game, enemy, player, current_room)
        
        # COMBAT NORMAL CONTRE LES AUTRES ENNEMIS
        print("\n" + "="*50)
        print(f"⚔️ COMBAT CONTRE {enemy.name.upper()} ⚔️")
        print("="*50)
        
        # Boucle de combat
        combat_round = 1
        while player.health > 0 and enemy.is_alive():
            print(f"\n--- Round {combat_round} ---")
            print(f"{player.name}: {player.health}/{player.max_health} PV")
            print(f"{enemy.name}: {enemy.health}/{enemy.max_health} PV")
            
            # Tour du joueur
            player_damage = player.attack(enemy)
            print(f"🗡️ Vous infligez {player_damage} dégâts à {enemy.name} !")
            
            if not enemy.is_alive():
                break
                
            # Tour de l'ennemi
            enemy_damage = enemy.calculate_damage()
            damage_taken = player.defend(enemy_damage)
            print(f"{enemy.name} vous inflige {damage_taken} dégâts !")
            
            if not player.is_alive():
                break
                
            combat_round += 1
        
        # Résultat du combat
        if enemy.is_alive():
            print("\n" + "="*50)
            print("DÉFAITE")
            print("="*50)
            print("Vous avez été vaincu...")
            game.finished = True
            return False
        else:
            print("\n" + "="*50)
            print("VICTOIRE")
            print("="*50)
            print(f"Vous avez vaincu {enemy.name} !")
            
            # Récupérer les récompenses
            loot = enemy.drop_loot()
            player.gold += loot["gold"]
            print(f"Vous avez gagné {loot['gold']} pièces d'or et {loot['experience']} XP !")
            
            # Retirer l'ennemi de la pièce
            current_room.remove_enemy(enemy_name)
            
            return True

    
    def _fight_morgrath_combat(game, enemy, player, current_room):
        """Gère le combat spécial contre Morgrath avec deux phases"""
        import random
        
        # Initialiser le compteur de rencontres si nécessaire
        if not hasattr(player, 'morgrath_encounters'):
            player.morgrath_encounters = 0
        
        player.morgrath_encounters += 1
        
        # PREMIÈRE RENCONTRE
        if player.morgrath_encounters == 1:
            print("\n" + "="*60)
            print("⚔️ AFFRONTEMENT AVEC MORGRATH, LE ROI DÉMON ⚔️")
            print("="*60)
            print(f"\n{player.name}: Il est temps de mettre fin à cette folie !")
            print(f"Morgrath: Enfin... tu es venu à ta ruine...\n")
            
            # Boucle de combat
            combat_round = 1
            while player.health > 0 and enemy.is_alive():
                print(f"\n--- Round {combat_round} ---")
                print(f"{player.name}: {player.health}/{player.max_health} PV")
                print(f"{enemy.name}: {enemy.health}/{enemy.max_health} PV (Phase {enemy.phase})")
                
                # Tour du joueur
                player_damage = player.attack(enemy)
                print(f"🗡️ Vous infligez {player_damage} dégâts à {enemy.name} !")
                
                if not enemy.is_alive():
                    break
                    
                # Tour de l'ennemi
                enemy_damage = enemy.calculate_damage()
                damage_taken = player.defend(enemy_damage)
                print(f"{enemy.name} vous inflige {damage_taken} dégâts !")
                
                if not player.is_alive():
                    break
                    
                combat_round += 1
            
            # Résultat de la première rencontre
            print("\n" + "="*60)
            print("PREMIÈRE RENCONTRE - ÉPUISEMENT")
            print("="*60)
            print("Morgrath vous écrase impitoyablement...")
            print("Vous sombrez dans les ténèbres...")
            print("\nMais une force étrange vous envahit...")
            print("Vous sentez un pouvoir ancien s'éveiller en vous...")
            print("="*60)
            
            # Réinitialiser pour la deuxième rencontre
            enemy.health = enemy.max_health
            enemy.phase = 1
            enemy.base_damage = 28
            player.health = player.max_health
            
            print(f"\n✨ Vous reprenez connaissance, rempli d'une énergie nouvelle...")
            print("Morgrath se rapproche pour vous achever...")
            print("C'est le moment de l'affrontement ultime !\n")
            
            return True
        
        # DEUXIÈME RENCONTRE - COMBAT FINAL
        else:
            print("\n" + "="*60)
            print("🔥 AFFRONTEMENT FINAL - MORGRATH S'ÉVEILLE 🔥")
            print("="*60)
            
            # 50% de chance de développer le pouvoir caché
            develops_hidden_power = random.random() < 0.5
            
            if develops_hidden_power:
                print("\n✨ UNE FORCE ANCIENNE S'ÉVEILLE EN VOUS ! ✨\n")
                print("Vous sentez le pouvoir des anciens héros d'Alderwood...")
                print("Lyra, Valerius, Thrain... leurs esprits vous guident...")
                print("\n🌟 POUVOIR CACHÉ ACTIVÉ: HÉRITAGE DES CENDRES 🌟")
                print("Vos attaques sont désormais DÉVASTANTES !\n")
                
                # Activer le pouvoir caché
                player.hidden_power_active = True
                player.hidden_power_multiplier = 12
            else:
                print("\n⚠️ Vous restez seul face à cette puissance écrasante...\n")
                player.hidden_power_active = False
            
            print("Morgrath rugit avec rage, prêt pour l'affrontement ultime!\n")
            
            # Boucle de combat finale
            combat_round = 1
            while player.health > 0 and enemy.is_alive():
                print(f"\n--- Round {combat_round} ---")
                print(f"{player.name}: {player.health}/{player.max_health} PV")
                if player.hidden_power_active:
                    print("⭐ POUVOIR CACHÉ ACTIF ⭐")
                print(f"{enemy.name}: {enemy.health}/{enemy.max_health} PV (Phase {enemy.phase})")
                
                # Tour du joueur avec pouvoir caché
                if player.hidden_power_active:
                    # Attaque amplifiée par le pouvoir caché
                    base_damage = player.attack(enemy)
                    amplified_damage = int(base_damage * player.hidden_power_multiplier)
                    
                    # Enlever les dégâts normaux et ajouter les amplifiés
                    enemy.health += base_damage
                    enemy.take_damage(amplified_damage)
                    
                    print(f"🌟 HÉRITAGE DES CENDRES ! 🌟")
                    print(f"Vous infligez {amplified_damage} dégâts DÉVASTATEURS à {enemy.name} !")
                else:
                    player_damage = player.attack(enemy)
                    print(f"🗡️ Vous infligez {player_damage} dégâts à {enemy.name} !")
                
                if not enemy.is_alive():
                    break
                    
                # Tour de l'ennemi
                enemy_damage = enemy.calculate_damage()
                damage_taken = player.defend(enemy_damage)
                print(f"{enemy.name} vous inflige {damage_taken} dégâts !")
                
                if not player.is_alive():
                    break
                    
                combat_round += 1
            
            # Résultat du combat final
            if enemy.is_alive():
                print("\n" + "="*60)
                print("DÉFAITE FINALE")
                print("="*60)
                print("Morgrath vous écrase définitivement...")
                if player.hidden_power_active:
                    print("Même l'héritage des anciens n'a pas suffi...")
                print("Votre quête s'achève dans la défaite.")
                print("="*60)
                game.finished = True
                return False
            else:
                print("\n" + "="*60)
                print("🏆 VICTOIRE ÉCLATANTE 🏆")
                print("="*60)
                print(f"\n{player.name} a vaincu Morgrath, le Roi Démon !")
                
                if player.hidden_power_active:
                    print("\n✨ L'héritage des cendres a prévalu ! ✨")
                    print("Les esprits des anciens héros se manifestent autour de vous...")
                    print("\nLyra: Tu as honoré notre mémoire...")
                    print("Valerius: Alderwood est vengé...")
                    print("Thrain: Repose en paix, dernier survivant...\n")
                else:
                    print("\nMalgré les odds, vous avez réussi !")
                    print("Votre détermination a été plus forte que la magie noire de Morgrath.\n")
                
                print("Morgrath s'effondre, et son corps se désagrège en poussière...")
                print("Les terres commencent à briller d'une lumière nouvelle...")
                print("Alderwood est libre. La malédiction est levée.\n")
                
                # Récupérer les récompenses
                loot = enemy.drop_loot()
                player.gold += loot["gold"]
                player.health = player.max_health
                
                print(f"Vous gagnez {loot['gold']} pièces d'or et {loot['experience']} XP !")
                print("\n" + "="*60)
                print("QUÊTE TERMINÉE - VICTOIRE FINALE!")
                print("="*60)
                
                # Retirer Morgrath de la pièce
                current_room.remove_enemy("morgrath")
                
                game.finished = True
                return True

    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un PNJ dans la pièce actuelle.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"\nLa commande '{command_word}' prend 1 seul paramètre.\n")
            return False
            
        character_name = list_of_words[1].lower()
        current_room = game.player.current_room
        
        if character_name not in current_room.characters:
            print(f"\nLe PNJ '{character_name}' n'est pas dans cette pièce.")
            if current_room.characters:
                print(f"PNJ présents: {', '.join(current_room.characters.keys())}")
            return False
            
        character = current_room.characters[character_name]
        dialogue = character.get_dialogue()
        
        print(f"\n=== Conversation avec {character.name} ===")
        print(f"{character.name}: {dialogue}")
        print(f"Type: {character.character_type}")
        
        # Dialogue spécial si Lyra est le mentor choisi
        if character_name == "lyra" and current_room.name == "Camp des Mentors":
            print(f"\nLyra vous regarde intensément...")
            print(f"Lyra: Ton entraînement est presque terminé. Tu es prêt à choisir ta voie.")
            print(f"Lyra: Arc, Épée ou Magie... quel chemin choisiras-tu ?")
        
        if character.quest_related:
            print(f"Quête associée: {character.quest_related}")
            
        return True

# AJOUTER CETTE NOUVELLE MÉTHODE À LA CLASSE Actions

    def choose(game, list_of_words, number_of_parameters):
        """
        Choisir votre voie (Arc, Épée ou Magie)

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        choice = list_of_words[1].upper()
        
        # Map des choix possibles
        choice_map = {
            "ARC": "ARC",
            "BOW": "ARC",
            "ARCHER": "ARC",
            "ÉPÉE": "EPEE",
            "EPEE": "EPEE",
            "SWORD": "EPEE",
            "WARRIOR": "EPEE",
            "GUERRIER": "EPEE",
            "MAGIE": "MAGIE",
            "MAGIC": "MAGIE",
            "MAGE": "MAGIE",
            "SORCIER": "MAGIE"
        }
        
        # Convertir le choix en format standard
        path = choice_map.get(choice, None)
        
        if path is None:
            print(f"\n⚠️  Voie inconnue: '{list_of_words[1]}'")
            print("Voies disponibles:")
            print(" - ARC (ou BOW, ARCHER)")
            print(" - ÉPÉE (ou EPEE, SWORD, WARRIOR)")
            print(" - MAGIE (ou MAGIC, MAGE)\n")
            return False
        
        if player.chosen_path:
            print(f"\n⚠️  Vous avez déjà choisi la voie: {player.chosen_path}")
            print("Vous ne pouvez pas changer de voie!\n")
            return False
        
        # Appliquer le choix de voie
        player.choose_path(path)
        
        print("\n" + "="*60)
        print(f"✨ VOIE CHOISIE: {path} ✨")
        print("="*60)
        
        if path == "ARC":
            print("\nVous avez choisi la voie de l'ARCHER!")
            print("Avantages: Attaques à distance précises, chances de coup critique élevées")
            print("Armes: Arc, Arbalète")
        elif path == "EPEE":
            print("\nVous avez choisi la voie du GUERRIER!")
            print("Avantages: Attaques puissantes et directes, bonne défense")
            print("Armes: Épée, Hache, Massue")
        elif path == "MAGIE":
            print("\nVous avez choisi la voie du MAGE!")
            print("Avantages: Attaques magiques puissantes, effets spéciaux (brûlure, poison)")
            print("Armes: Bâton, Grimoire, Cristal")
        
        print("\n🎯 Vous êtes maintenant prêt à affronter tous les ennemis!")
        print("="*60 + "\n")
        return True