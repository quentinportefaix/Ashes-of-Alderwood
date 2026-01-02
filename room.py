# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {} # Inventaire des objets dans la piÃ¨ce
        self.enemies = {} # Dictionnaire des ennemis dans la piÃ¨ce
        self.characters = {} # Dictionnaire des PNJ dans la piÃ¨ce
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits and items.
    def get_long_description(self):
        description = f"\n{self.description}\n\n{self.get_exit_string()}\n"
        
        # Ajouter la liste des objets dans la piÃ¨ce
        if self.inventory:
            description += "\nVous voyez au sol:\n"
            for item_name, item in self.inventory.items():
                description += f" - {item}\n"
        
        # Ajouter la liste des ennemis dans la piÃ¨ce
        if self.enemies:
            description += self.get_enemies_string()
            
        # Ajouter la liste des PNJ dans la piÃ¨ce
        if self.characters:
            description += self.get_characters_string()
        
        return description

    # MÃ©thodes pour gÃ©rer l'inventaire de la piÃ¨ce
    def add_item(self, item_name, item):
        """Ajoute un objet Ã  la piÃ¨ce"""
        self.inventory[item_name] = item
        return True

    def remove_item(self, item_name):
        """Retire un objet de la piÃ¨ce"""
        if item_name in self.inventory:
            return self.inventory.pop(item_name)
        return None

    def get_items_string(self):
        """Retourne une string formatÃ©e des objets dans la piÃ¨ce"""
        if not self.inventory:
            return "Il n'y a rien d'intÃ©ressant ici."
        
        items_str = "Objets dans la piÃ¨ce:\n"
        for item_name, item in self.inventory.items():
            items_str += f" - {item}\n"
        return items_str

    # MÃ©thodes pour gÃ©rer les ennemis
    def add_enemy(self, enemy_name, enemy):
        """Ajoute un ennemi Ã  la piÃ¨ce"""
        self.enemies[enemy_name] = enemy
        return True

    def remove_enemy(self, enemy_name):
        """Retire un ennemi de la piÃ¨ce"""
        if enemy_name in self.enemies:
            return self.enemies.pop(enemy_name)
        return None

    def get_enemies_string(self):
        """Retourne une string formatÃ©e des ennemis dans la piÃ¨ce"""
        if not self.enemies:
            return ""
        
        enemies_str = "\nðŸ§Œ Ennemis prÃ©sents:\n"
        for enemy_name, enemy in self.enemies.items():
            enemies_str += f" - {enemy_name}: {enemy}\n"
        return enemies_str

    # MÃ©thodes pour gÃ©rer les PNJ
    def add_character(self, character_name, character):
        """Ajoute un PNJ Ã  la piÃ¨ce"""
        self.characters[character_name] = character
        character.current_room = self # Mettre Ã  jour la rÃ©fÃ©rence de la piÃ¨ce
        return True

    def remove_character(self, character_name):
        """Retire un PNJ de la piÃ¨ce"""
        if character_name in self.characters:
            character = self.characters.pop(character_name)
            character.current_room = None # Retirer la rÃ©fÃ©rence Ã  la piÃ¨ce
            return character
        return None

    def get_characters_string(self):
        """Retourne une string formatÃ©e des PNJ dans la piÃ¨ce"""
        if not self.characters:
            return ""
        
        characters_str = "\nðŸ§ Personnages prÃ©sents:\n"
        for character_name, character in self.characters.items():
            characters_str += f" - {character_name}: {character.description}\n"
        return characters_str

    # MÃ©thode utilitaire pour obtenir toutes les informations de la piÃ¨ce
    def get_full_info(self):
        """Retourne toutes les informations de la piÃ¨ce (pour debug)"""
        info = f"=== {self.name} ===\n"
        info += f"Description: {self.description}\n"
        info += f"Exits: {self.exits}\n"
        
        if self.inventory:
            info += f"Objets: {list(self.inventory.keys())}\n"
        else:
            info += "Objets: Aucun\n"
            
        if self.enemies:
            info += f"Ennemis: {list(self.enemies.keys())}\n"
        else:
            info += "Ennemis: Aucun\n"
            
        if self.characters:
            info += f"PNJ: {list(self.characters.keys())}\n"
        else:
            info += "PNJ: Aucun\n"
            
        return info

    # MÃ©thode pour vider complÃ¨tement une piÃ¨ce (pour les rÃ©initialisations)
    def clear_room(self):
        """Vide complÃ¨tement la piÃ¨ce de tous ses contenus"""
        self.inventory.clear()
        self.enemies.clear()
        self.characters.clear()
        return True

    # MÃ©thode pour vÃ©rifier si un PNJ spÃ©cifique est dans la piÃ¨ce
    def has_character(self, character_name):
        """VÃ©rifie si un PNJ spÃ©cifique est dans la piÃ¨ce"""
        return character_name in self.characters

    # MÃ©thode pour vÃ©rifier si un ennemi spÃ©cifique est dans la piÃ¨ce
    def has_enemy(self, enemy_name):
        """VÃ©rifie si un ennemi spÃ©cifique est dans la piÃ¨ce"""
        return enemy_name in self.enemies

    # MÃ©thode pour vÃ©rifier si un objet spÃ©cifique est dans la piÃ¨ce
    def has_item(self, item_name):
        """VÃ©rifie si un objet spÃ©cifique est dans la piÃ¨ce"""
        return item_name in self.inventory