# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = [] # Pour l'historique de déplacement
        
        # Stats de base pour le combat
        self.stats = {
            'FOR': 10, # Force - dégâts physiques, port d'armures lourdes
            'DEX': 10, # Dextérité - esquive, dégâts armes légères
            'INT': 10, # Intelligence - dégâts magiques, résistance magique
            'CON': 10, # Constitution - points de vie, résistance physique
            'SAG': 10, # Sagesse - perception, détection pièges
            'CHA': 10 # Charisme - persuasion, prix chez marchands
        }
        
        # État du joueur
        self.health = 50
        self.max_health = 50
        self.gold = 0
        
        # Inventaire et équipement
        self.inventory = {}
        self.equipped_weapon = None
        self.equipped_armor = None
        
        # Voie choisie (déterminée plus tard)
        self.chosen_path = None # "ARC", "EPEE", ou "MAGIE"

    # Define the move method.
    def move(self, direction):
        # Sauvegarder la room actuelle dans l'historique avant de bouger
        if self.current_room:
            self.history.append(self.current_room)
            
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        
        # Afficher l'historique après chaque déplacement réussi
        if self.history:
            print(self.get_history())
            
        return True

    # Méthode pour afficher l'historique
    def get_history(self):
        """Retourne l'historique des pièces visitées"""
        if not self.history:
            return "Aucun historique pour le moment."
        
        history_str = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in self.history:
            history_str += f" - {room.description}\n"
        return history_str

    # Méthodes pour les stats
    def get_stats_string(self):
        """Retourne une string formatée avec toutes les stats"""
        stats_str = f"\n=== STATISTIQUES DE {self.name.upper()} ===\n"
        stats_str += f"PV: {self.health}/{self.max_health} | Or: {self.gold} pièces\n\n"
        
        for stat, value in self.stats.items():
            stats_str += f"{stat}: {value}\n"
            
        if self.chosen_path:
            stats_str += f"\nVoie: {self.chosen_path}\n"
            
        return stats_str

    def calculate_physical_damage(self):
        """Calcule les dégâts physiques basés sur la FOR et l'arme"""
        base_damage = 5
        strength_bonus = self.stats['FOR'] * 0.2 # 20% par point de FOR
        
        if self.equipped_weapon:
            weapon_bonus = self.equipped_weapon.get('damage_bonus', 0)
        else:
            weapon_bonus = 0
            
        total_damage = base_damage + strength_bonus + weapon_bonus
        return max(1, int(total_damage))

    def calculate_magical_damage(self):
        """Calcule les dégâts magiques basés sur l'INT"""
        base_damage = 4
        intelligence_bonus = self.stats['INT'] * 0.25 # 25% par point d'INT
        
        if self.equipped_weapon and self.equipped_weapon.get('magic_bonus', 0):
            weapon_bonus = self.equipped_weapon['magic_bonus']
        else:
            weapon_bonus = 0
            
        total_damage = base_damage + intelligence_bonus + weapon_bonus
        return max(1, int(total_damage))

    def calculate_dodge_chance(self):
        """Calcule les chances d'esquive basées sur la DEX"""
        base_dodge = 10 # 10% de base
        dexterity_bonus = self.stats['DEX'] * 1.5 # 1.5% par point de DEX
        
        if self.equipped_armor and self.equipped_armor.get('dodge_penalty', 0):
            armor_penalty = self.equipped_armor['dodge_penalty']
        else:
            armor_penalty = 0
            
        total_dodge = base_dodge + dexterity_bonus - armor_penalty
        return max(5, min(80, total_dodge)) # Entre 5% et 80%

    def take_damage(self, damage):
        """Applique des dégâts au joueur"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health > 0 # Retourne True si toujours en vie

    def heal(self, amount):
        """Soigne le joueur"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        return self.health

    # Méthodes pour l'inventaire
    def add_item(self, item_name, item):
        """Ajoute un objet à l'inventaire"""
        self.inventory[item_name] = item
        return True

    def remove_item(self, item_name):
        """Retire un objet de l'inventaire"""
        if item_name in self.inventory:
            return self.inventory.pop(item_name)
        return None

    def get_inventory_string(self):
        """Retourne une string formatée de l'inventaire"""
        if not self.inventory:
            return "Votre inventaire est vide."
        
        inventory_str = "Vous disposez des items suivants:\n"
        for item_name, item in self.inventory.items():
            inventory_str += f" - {item_name}"
            if hasattr(item, 'description'):
                inventory_str += f" : {item.description}"
            inventory_str += "\n"
        return inventory_str

    # Méthodes pour l'équipement
    def equip_weapon(self, weapon_name):
        """Équipe une arme"""
        if weapon_name in self.inventory:
            self.equipped_weapon = self.inventory[weapon_name]
            return True
        return False

    def equip_armor(self, armor_name):
        """Équipe une armure"""
        if armor_name in self.inventory:
            self.equipped_armor = self.inventory[armor_name]
            return True
        return False

    def choose_path(self, path):
        """Définit la voie choisie (ARC, EPEE, MAGIE)"""
        valid_paths = ["ARC", "EPEE", "MAGIE"]
        if path in valid_paths:
            self.chosen_path = path
            
            # Bonus selon la voie choisie
            if path == "ARC":
                self.stats['DEX'] += 3
            elif path == "EPEE":
                self.stats['FOR'] += 3
            elif path == "MAGIE":
                self.stats['INT'] += 3
                
            return True
        return False

    # Méthodes de combat
    def attack(self, enemy):
        """Le joueur attaque un ennemi"""
        import random
        
        # Calcul des dégâts selon la voie choisie
        if self.chosen_path == "ARC":
            base_damage = self.calculate_physical_damage()
            # Chance de coup critique pour les archers
            if random.randint(1, 100) <= self.stats['DEX']:
                base_damage *= 2
                print("⭐ Coup critique !")
                
        elif self.chosen_path == "EPEE":
            base_damage = self.calculate_physical_damage()
            # Bonus de dégâts constant pour les guerriers
            base_damage += 2
            
        elif self.chosen_path == "MAGIE":
            base_damage = self.calculate_magical_damage()
            # Chance de brûlure magique
            if random.randint(1, 100) <= self.stats['INT']:
                burn_damage = self.stats['INT'] // 2
                base_damage += burn_damage
                print(f"🔥 Brûlure magique ! +{burn_damage} dégâts")
        else:
            base_damage = self.calculate_physical_damage()
        
        # Application des dégâts
        enemy.take_damage(base_damage)
        return base_damage
    
    def defend(self, enemy_damage):
        """Le joueur subit une attaque"""
        import random
        
        # Chance d'esquiver
        dodge_chance = self.calculate_dodge_chance()
        if random.randint(1, 100) <= dodge_chance:
            print("💨 Vous esquivez l'attaque !")
            return 0
        
        # Réduction des dégâts par l'armure
        damage_reduction = 0
        if self.equipped_armor:
            damage_reduction = self.equipped_armor.defense_bonus
        
        final_damage = max(1, enemy_damage - damage_reduction)
        self.take_damage(final_damage)
        
        return final_damage
    
    def use_consumable(self, item_name):
        """Utilise un consommable de l'inventaire"""
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if hasattr(item, 'effect_type'):
                if item.effect_type == "SOIN":
                    heal_amount = self.heal(item.effect_power)
                    print(f"💚 Vous utilisez {item_name} et récupérez {item.effect_power} PV !")
                    self.remove_item(item_name)
                    return True
                elif item.effect_type == "BUFF_FOR":
                    self.stats['FOR'] += item.effect_power
                    print(f"💪 Vous utilisez {item_name} et gagnez +{item.effect_power} en Force !")
                    self.remove_item(item_name)
                    return True
                elif item.effect_type == "BUFF_DEX":
                    self.stats['DEX'] += item.effect_power
                    print(f"🎯 Vous utilisez {item_name} et gagnez +{item.effect_power} en Dextérité !")
                    self.remove_item(item_name)
                    return True
        
        print(f"Vous ne pouvez pas utiliser {item_name}.")
        return False

    # Méthode pour vérifier si le joueur est en vie
    def is_alive(self):
        """Vérifie si le joueur est en vie"""
        return self.health > 0

    # Méthode pour réinitialiser le joueur (pour une nouvelle partie)
    def reset(self):
        """Réinitialise le joueur pour une nouvelle partie"""
        self.current_room = None
        self.history = []
        self.health = 50
        self.max_health = 50
        self.gold = 0
        self.inventory = {}
        self.equipped_weapon = None
        self.equipped_armor = None
        self.chosen_path = None
        
        # Réinitialiser les stats
        for stat in self.stats:
            self.stats[stat] = 10
            
        return True