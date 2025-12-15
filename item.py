"""
item.py - Système d'objets, d'équipement et de consommables pour "L'Héritage des Cendres"
"""

import random

class Item:
    """Classe de base pour tous les objets du jeu"""
    
    def __init__(self, name, description, item_type, value=0, weight=0):
        """
        Initialise un objet
        
        Args:
            name (str): Nom de l'objet
            description (str): Description de l'objet
            item_type (str): Type d'objet ("WEAPON", "ARMOR", "CONSUMABLE", "KEY", "MISC")
            value (int): Valeur en pièces d'or
            weight (float): Poids en unités (pour système de portage)
        """
        self.name = name
        self.description = description
        self.item_type = item_type
        self.value = value
        self.weight = weight
        
    def __str__(self):
        """Représentation textuelle de l'objet"""
        return f"{self.name}: {self.description}"
        
    def get_full_info(self):
        """Retourne des informations détaillées sur l'objet"""
        info = f"=== {self.name.upper()} ===\n"
        info += f"Description: {self.description}\n"
        info += f"Type: {self.item_type}\n"
        info += f"Valeur: {self.value} pièces d'or\n"
        info += f"Poids: {self.weight} unités\n"
        return info


class Weapon(Item):
    """Classe pour les armes"""
    
    def __init__(self, name, description, damage_bonus, weapon_type, 
                 magic_bonus=0, critical_chance=5, value=0, weight=1.0):
        """
        Initialise une arme
        
        Args:
            name (str): Nom de l'arme
            description (str): Description
            damage_bonus (int): Bonus de dégâts
            weapon_type (str): Type d'arme ("ARC", "EPEE", "BATON", "DAGUE")
            magic_bonus (int): Bonus de dégâts magiques
            critical_chance (int): Pourcentage de chance de coup critique
            value (int): Valeur en pièces d'or
            weight (float): Poids
        """
        super().__init__(name, description, "WEAPON", value, weight)
        self.damage_bonus = damage_bonus
        self.weapon_type = weapon_type
        self.magic_bonus = magic_bonus
        self.critical_chance = critical_chance
        
    def get_full_info(self):
        """Informations détaillées de l'arme"""
        info = super().get_full_info()
        info += f"Bonus dégâts: +{self.damage_bonus}\n"
        info += f"Type d'arme: {self.weapon_type}\n"
        if self.magic_bonus > 0:
            info += f"Bonus magique: +{self.magic_bonus}\n"
        info += f"Chance critique: {self.critical_chance}%\n"
        return info
        
    def calculate_critical(self):
        """Détermine si l'attaque est critique"""
        return random.randint(1, 100) <= self.critical_chance


class Armor(Item):
    """Classe pour les armures"""
    
    def __init__(self, name, description, defense_bonus, armor_type,
                 dodge_penalty=0, magic_resistance=0, value=0, weight=2.0):
        """
        Initialise une armure
        
        Args:
            name (str): Nom de l'armure
            description (str): Description
            defense_bonus (int): Bonus de défense
            armor_type (str): Type d'armure ("LEGER", "MOYEN", "LOURD")
            dodge_penalty (int): Malus à l'esquive
            magic_resistance (int): Résistance aux dégâts magiques
            value (int): Valeur en pièces d'or
            weight (float): Poids
        """
        super().__init__(name, description, "ARMOR", value, weight)
        self.defense_bonus = defense_bonus
        self.armor_type = armor_type
        self.dodge_penalty = dodge_penalty
        self.magic_resistance = magic_resistance
        
    def get_full_info(self):
        """Informations détaillées de l'armure"""
        info = super().get_full_info()
        info += f"Bonus défense: +{self.defense_bonus}\n"
        info += f"Type d'armure: {self.armor_type}\n"
        if self.dodge_penalty > 0:
            info += f"Malus esquive: -{self.dodge_penalty}%\n"
        if self.magic_resistance > 0:
            info += f"Résistance magique: +{self.magic_resistance}\n"
        return info


class Consumable(Item):
    """Classe pour les objets consommables (potions, etc.)"""
    
    def __init__(self, name, description, effect_type, effect_power, 
                 duration=0, value=0, weight=0.5):
        """
        Initialise un consommable
        
        Args:
            name (str): Nom du consommable
            description (str): Description
            effect_type (str): Type d'effet ("HEAL", "BUFF_FOR", "BUFF_DEX", 
                               "BUFF_INT", "BUFF_CON", "ANTIDOTE", "INVISIBILITY")
            effect_power (int): Puissance de l'effet
            duration (int): Durée en tours (0 = instantané)
            value (int): Valeur en pièces d'or
            weight (float): Poids
        """
        super().__init__(name, description, "CONSUMABLE", value, weight)
        self.effect_type = effect_type
        self.effect_power = effect_power
        self.duration = duration
        
    def get_full_info(self):
        """Informations détaillées du consommable"""
        info = super().get_full_info()
        info += f"Effet: {self.get_effect_name()}\n"
        info += f"Puissance: {self.effect_power}\n"
        if self.duration > 0:
            info += f"Durée: {self.duration} tours\n"
        return info
        
    def get_effect_name(self):
        """Retourne le nom de l'effet en français"""
        effect_names = {
            "HEAL": "Soin",
            "BUFF_FOR": "Bonus de Force",
            "BUFF_DEX": "Bonus de Dextérité",
            "BUFF_INT": "Bonus d'Intelligence",
            "BUFF_CON": "Bonus de Constitution",
            "ANTIDOTE": "Antidote",
            "INVISIBILITY": "Invisibilité"
        }
        return effect_names.get(self.effect_type, self.effect_type)


class KeyItem(Item):
    """Classe pour les objets clés (quêtes, progression)"""
    
    def __init__(self, name, description, use_location=None, value=0, weight=0.1):
        """
        Initialise un objet clé
        
        Args:
            name (str): Nom de l'objet
            description (str): Description
            use_location (str): Lieu où l'objet peut être utilisé
            value (int): Valeur en pièces d'or
            weight (float): Poids
        """
        super().__init__(name, description, "KEY", value, weight)
        self.use_location = use_location
        self.used = False
        
    def get_full_info(self):
        """Informations détaillées de l'objet clé"""
        info = super().get_full_info()
        if self.use_location:
            info += f"Utilisable à: {self.use_location}\n"
        info += f"État: {'Utilisé' if self.used else 'Non utilisé'}\n"
        return info


class QuestItem(Item):
    """Classe pour les objets de quête"""
    
    def __init__(self, name, description, quest_name, value=0, weight=0.5):
        """
        Initialise un objet de quête
        
        Args:
            name (str): Nom de l'objet
            description (str): Description
            quest_name (str): Nom de la quête associée
            value (int): Valeur en pièces d'or
            weight (float): Poids
        """
        super().__init__(name, description, "QUEST", value, weight)
        self.quest_name = quest_name
        
    def get_full_info(self):
        """Informations détaillées de l'objet de quête"""
        info = super().get_full_info()
        info += f"Quête associée: {self.quest_name}\n"
        return info


# ============================================================================
# CATALOGUE D'OBJETS PRÉDÉFINIS
# ============================================================================

class ItemCatalog:
    """Catalogue central de tous les objets du jeu"""
    
    @staticmethod
    def create_items():
        """Crée et retourne le catalogue d'objets"""
        
        catalog = {}
        
        # ====================================================================
        # ARMES DE DÉPART (Acte 2 - Choix de voie)
        # ====================================================================
        
        catalog["arc_dentrainement"] = Weapon(
            name="Arc d'Entraînement",
            description="Un arc simple en frêne, utilisé pour l'entraînement",
            damage_bonus=2,
            weapon_type="ARC",
            critical_chance=10,
            value=10,
            weight=1.5
        )
        
        catalog["epee_dentrainement"] = Weapon(
            name="Épée d'Entraînement",
            description="Une épée en bois pour la pratique, solide et équilibrée",
            damage_bonus=3,
            weapon_type="EPEE",
            value=12,
            weight=2.0
        )
        
        catalog["grimoire_elementaire"] = Weapon(
            name="Grimoire Élémentaire",
            description="Un livre de sorts basiques, couvert de runes anciennes",
            damage_bonus=1,
            weapon_type="BATON",
            magic_bonus=4,
            value=15,
            weight=1.0
        )
        
        # ====================================================================
        # ARMES AMÉLIORÉES (Acte 3)
        # ====================================================================
        
        catalog["arc_long_elfique"] = Weapon(
            name="Arc Long Elfique",
            description="Un arc élégant fabriqué par les elfes, précis et puissant",
            damage_bonus=5,
            weapon_type="ARC",
            critical_chance=15,
            value=50,
            weight=1.2
        )
        
        catalog["epee_garde_royale"] = Weapon(
            name="Épée de la Garde Royale",
            description="Une épée droite et mortelle, forgée pour les champions",
            damage_bonus=6,
            weapon_type="EPEE",
            value=60,
            weight=2.5
        )
        
        catalog["baton_ancien_sage"] = Weapon(
            name="Bâton de l'Ancien Sage",
            description="Un bâton de chêne centenaire, imprégné de magie naturelle",
            damage_bonus=2,
            weapon_type="BATON",
            magic_bonus=8,
            value=70,
            weight=1.8
        )
        
        # ====================================================================
        # ARMES LÉGENDAIRES (Acte 5)
        # ====================================================================
        
        catalog["arc_cendres"] = Weapon(
            name="Arc des Cendres",
            description="Forgé dans les cendres d'Alderwood, il brûle de vengeance",
            damage_bonus=10,
            weapon_type="ARC",
            magic_bonus=5,
            critical_chance=20,
            value=200,
            weight=1.0
        )
        
        catalog["epee_barbe_de_pierre"] = Weapon(
            name="Épée Barbe-de-Pierre",
            description="L'épée légendaire de Thrain, aussi solide que la montagne",
            damage_bonus=12,
            weapon_type="EPEE",
            value=250,
            weight=3.0
        )
        
        catalog["grimoire_ardenwein"] = Weapon(
            name="Grimoire d'Ardenwein",
            description="Le livre interdit de l'archimage Ardenwein, source de pouvoir",
            damage_bonus=4,
            weapon_type="BATON",
            magic_bonus=15,
            value=300,
            weight=1.5
        )
        
        # ====================================================================
        # ARMURES
        # ====================================================================
        
        catalog["armure_cuir"] = Armor(
            name="Armure de Cuir",
            description="Une armure légère en cuir tanné, flexible mais protectrice",
            defense_bonus=3,
            armor_type="LEGER",
            dodge_penalty=5,
            value=20,
            weight=3.0
        )
        
        catalog["cotte_mailles"] = Armor(
            name="Cotte de Mailles",
            description="Une armure de mailles solide, protège bien contre les coups",
            defense_bonus=6,
            armor_type="MOYEN",
            dodge_penalty=15,
            value=45,
            weight=6.0
        )
        
        catalog["plaque_acier"] = Armor(
            name="Armure de Plaque",
            description="Une lourde armure d'acier, presque impénétrable",
            defense_bonus=10,
            armor_type="LOURD",
            dodge_penalty=25,
            value=100,
            weight=12.0
        )
        
        catalog["tunique_elfique"] = Armor(
            name="Tunique Elfique",
            description="Une tunique légère tissée avec de la soie d'araignée magique",
            defense_bonus=4,
            armor_type="LEGER",
            magic_resistance=5,
            value=80,
            weight=1.0
        )
        
        # ====================================================================
        # CONSOMMABLES - POTIONS
        # ====================================================================
        
        catalog["potion_soin"] = Consumable(
            name="Potion de Soin",
            description="Une potion rouge qui restaure la santé",
            effect_type="HEAL",
            effect_power=20,
            value=25,
            weight=0.3
        )
        
        catalog["potion_soin_majeure"] = Consumable(
            name="Potion de Soin Majeure",
            description="Une potion rouge foncé qui restaure beaucoup de santé",
            effect_type="HEAL",
            effect_power=50,
            value=60,
            weight=0.4
        )
        
        catalog["potion_force"] = Consumable(
            name="Potion de Force",
            description="Une potion verte qui augmente temporairement la force",
            effect_type="BUFF_FOR",
            effect_power=5,
            duration=10,
            value=40,
            weight=0.3
        )
        
        catalog["potion_dexterite"] = Consumable(
            name="Potion de Dextérité",
            description="Une potion bleue qui améliore l'agilité",
            effect_type="BUFF_DEX",
            effect_power=5,
            duration=10,
            value=40,
            weight=0.3
        )
        
        catalog["potion_intelligence"] = Consumable(
            name="Potion d'Intelligence",
            description="Une potion violette qui aiguise l'esprit",
            effect_type="BUFF_INT",
            effect_power=5,
            duration=10,
            value=40,
            weight=0.3
        )
        
        catalog["antidote"] = Consumable(
            name="Antidote",
            description="Un remède contre les poisons et les maladies",
            effect_type="ANTIDOTE",
            effect_power=1,
            value=30,
            weight=0.2
        )
        
        # ====================================================================
        # OBJETS CLÉS ET DE QUÊTE
        # ====================================================================
        
        catalog["medaillon_parents"] = QuestItem(
            name="Médaillon Familial",
            description="Un médaillon avec le portrait de vos parents, votre seul souvenir d'eux",
            quest_name="Souvenirs d'Alderwood",
            value=1, # Inestimable
            weight=0.1
        )
        
        catalog["journal_brul"] = QuestItem(
            name="Journal Brûlé",
            description="Votre journal d'enfance, à moitié consumé par les flammes",
            quest_name="Souvenirs d'Alderwood",
            value=0,
            weight=0.2
        )
        
        catalog["clef_gobelins"] = KeyItem(
            name="Clé Gobeline",
            description="Une clé grossière forgée par les gobelins",
            use_location="Porte des Gobelins",
            value=5,
            weight=0.5
        )
        
        catalog["gemme_portail"] = KeyItem(
            name="Gemme de Portail",
            description="Une gemme magique qui pulse d'énergie ancienne",
            use_location="Portail des Trolls",
            value=100,
            weight=0.3
        )
        
        catalog["amulette_thrain"] = QuestItem(
            name="Amulette de Thrain",
            description="L'amulette que portait Thrain lors de son sacrifice",
            quest_name="Héritage de Thrain",
            value=150,
            weight=0.2
        )
        
        catalog["note_lyra"] = QuestItem(
            name="Note de Lyra",
            description="Un message chiffré de Lyra, trouvé dans sa cellule",
            quest_name="Sauvetage de Lyra",
            value=0,
            weight=0.1
        )
        
        catalog["coeur_demon"] = QuestItem(
            name="Cœur de Démon",
            description="Le cœur cristallisé de Morgrath, source de son pouvoir",
            quest_name="Confrontation Finale",
            value=500,
            weight=1.0
        )
        
        # ====================================================================
        # OBJETS DIVERS
        # ====================================================================
        
        catalog["torche"] = Item(
            name="Torche",
            description="Une torche qui éclaire les zones sombres",
            item_type="MISC",
            value=2,
            weight=1.0
        )
        
        catalog["cordes"] = Item(
            name="Corde Solide",
            description="Une longueur de corde robuste, utile pour l'escalade",
            item_type="MISC",
            value=3,
            weight=2.0
        )
        
        catalog["pioche"] = Item(
            name="Pioche",
            description="Une pioche de mineur, utile pour creuser",
            item_type="MISC",
            value=8,
            weight=3.0
        )
        
        catalog["bourse_or"] = Item(
            name="Bourse d'Or",
            description="Une bourse contenant des pièces d'or",
            item_type="MISC",
            value=50, # La valeur EST le contenu
            weight=0.5
        )
        
        return catalog
    
    @staticmethod
    def get_item(item_name):
        """
        Retourne une copie d'un objet depuis le catalogue
        
        Args:
            item_name (str): Nom de l'objet dans le catalogue
            
        Returns:
            Item: Une nouvelle instance de l'objet
        """
        catalog = ItemCatalog.create_items()
        
        if item_name in catalog:
            # Pour les objets simples, on retourne une nouvelle instance
            original = catalog[item_name]
            
            # Recréer l'objet selon son type
            if isinstance(original, Weapon):
                return Weapon(
                    name=original.name,
                    description=original.description,
                    damage_bonus=original.damage_bonus,
                    weapon_type=original.weapon_type,
                    magic_bonus=original.magic_bonus,
                    critical_chance=original.critical_chance,
                    value=original.value,
                    weight=original.weight
                )
            elif isinstance(original, Armor):
                return Armor(
                    name=original.name,
                    description=original.description,
                    defense_bonus=original.defense_bonus,
                    armor_type=original.armor_type,
                    dodge_penalty=original.dodge_penalty,
                    magic_resistance=original.magic_resistance,
                    value=original.value,
                    weight=original.weight
                )
            elif isinstance(original, Consumable):
                return Consumable(
                    name=original.name,
                    description=original.description,
                    effect_type=o