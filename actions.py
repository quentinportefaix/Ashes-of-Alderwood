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

        # Vérifier si la direction mène à une room None (game over ou chemin bloqué)
        if game.player.current_room.exits[direction] is None:
            if direction == "FENETRE":
                print("\n" + "="*50)
                print("GAME OVER")
                print("="*50)
                print("Vous sautez par la fenêtre et tombez de deux étages...")
                print("La chute vous brise les jambes. Des orcs vous achèvent au sol.")
                print("⛔ Parfois, la bravoure n'est que de l'imprudence.")
                print("="*50)
                game.finished = True
            elif direction == "DROITE":
                print("\n" + "="*50)
                print("GAME OVER") 
                print("="*50)
                print("Vous tombez nez à nez avec un orc massif...")
                print("Sa hache s'abat sur vous avant même que vous puissiez réagir.")
                print("⛔ L'observation avant l'action aurait été plus sage.")
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
        print(" - Spéciales : PORTE, FENETRE, GAUCHE, DROITE, etc.")
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

    def fight(game, list_of_words, number_of_parameters):
        """
        Engager un combat avec un ennemi dans la pièce.

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
        enemy_name = list_of_words[1].lower()
        
        # Vérifier si le joueur a choisi une voie
        if not player.chosen_path:
            print("\n❌ Vous devez d'abord choisir une voie (arc, épée ou magie) avant de combattre !")
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