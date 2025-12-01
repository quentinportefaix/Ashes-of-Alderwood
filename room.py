# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {} # Inventaire des objets dans la pièce
        self.enemies = {} # Dictionnaire des ennemis dans la pièce
        self.characters = {} # Dictionnaire des PNJ dans la pièce
    
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
        description = f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
        
        # Ajouter la liste des objets dans la pièce
        if self.inventory:
            description += "\nVous voyez au sol:\n"
            for item_name, item in self.inventory.items():
                description += f" - {item}\n"
        
        # Ajouter la liste des ennemis dans la pièce
        if self.enemies:
            description += self.get_enemies_string()
            
        # Ajouter la liste des PNJ dans la pièce
        if self.characters:
            description += self.get_characters_string()
        
        return description

    # Méthodes pour gérer l'inventaire de la pièce
    def add_item(self, item_name, item):
        """Ajoute un objet à la pièce"""
        self.inventory[item_name] = item
        return True

    def remove_item(self, item_name):
        """Retire un objet de la pièce"""
        if item_name in self.inventory:
            return self.inventory.pop(item_name)
        return None

    def get_items_string(self):
        """Retourne une string formatée des objets dans la pièce"""
        if not self.inventory:
            return "Il n'y a rien d'intéressant ici."
        
        items_str = "Objets dans la pièce:\n"
        for item_name, item in self.inventory.items():
            items_str += f" - {item}\n"
        return items_str

    # Méthodes pour gérer les ennemis
    def add_enemy(self, enemy_name, enemy):
        """Ajoute un ennemi à la pièce"""
        self.enemies[enemy_name] = enemy
        return True

    def remove_enemy(self, enemy_name):
        """Retire un ennemi de la pièce"""
        if enemy_name in self.enemies:
            return self.enemies.pop(enemy_name)
        return None

    def get_enemies_string(self):
        """Retourne une string formatée des ennemis dans la pièce"""
        if not self.enemies:
            return ""
        
        enemies_str = "\n🧌 Ennemis présents:\n"
        for enemy_name, enemy in self.enemies.items():
            enemies_str += f" - {enemy_name}: {enemy}\n"
        return enemies_str

    # Méthodes pour gérer les PNJ
    def add_character(self, character_name, character):
        """Ajoute un PNJ à la pièce"""
        self.characters[character_name] = character
        character.current_room = self # Mettre à jour la référence de la pièce
        return True

    def remove_character(self, character_name):
        """Retire un PNJ de la pièce"""
        if character_name in self.characters:
            character = self.characters.pop(character_name)
            character.current_room = None # Retirer la référence à la pièce
            return character
        return None

    def get_characters_string(self):
        """Retourne une string formatée des PNJ dans la pièce"""
        if not self.characters:
            return ""
        
        characters_str = "\n🧍 Personnages présents:\n"
        for character_name, character in self.characters.items():
            characters_str += f" - {character_name}: {character.description}\n"
        return characters_str

    # Méthode utilitaire pour obtenir toutes les informations de la pièce
    def get_full_info(self):
        """Retourne toutes les informations de la pièce (pour debug)"""
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

    # Méthode pour vider complètement une pièce (pour les réinitialisations)
    def clear_room(self):
        """Vide complètement la pièce de tous ses contenus"""
        self.inventory.clear()
        self.enemies.clear()
        self.characters.clear()
        return True

    # Méthode pour vérifier si un PNJ spécifique est dans la pièce
    def has_character(self, character_name):
        """Vérifie si un PNJ spécifique est dans la pièce"""
        return character_name in self.characters

    # Méthode pour vérifier si un ennemi spécifique est dans la pièce
    def has_enemy(self, enemy_name):
        """Vérifie si un ennemi spécifique est dans la pièce"""
        return enemy_name in self.enemies

    # Méthode pour vérifier si un objet spécifique est dans la pièce
    def has_item(self, item_name):
        """Vérifie si un objet spécifique est dans la pièce"""
        return item_name in self.inventory