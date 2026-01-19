"""
enemy.py - Système d'ennemis, de combat et de gestion des monstres pour "L'Héritage des Cendres"
"""

import random
from abc import ABC, abstractmethod


class Enemy(ABC):
    """Classe abstraite de base pour tous les ennemis"""
    
    def __init__(self, name, health, damage, enemy_type, experience=0, 
                 gold_range=(0, 0), resistance=None, weakness=None):
        """
        Initialise un ennemi
        
        Args:
            name (str): Nom de l'ennemi
            health (int): Points de vie maximum
            damage (int): Dégâts de base
            enemy_type (str): Type d'ennemi ("GOBELIN", "ORC", "TROLL", "BOSS", "SPECIAL")
            experience (int): XP donné à la défaite
            gold_range (tuple): Plage d'or donné (min, max)
            resistance (dict): Résistances aux types de dégâts
            weakness (dict): Faiblesses aux types de dégâts
        """
        self.name = name
        self.health = health
        self.max_health = health
        self.base_damage = damage
        self.enemy_type = enemy_type
        self.experience = experience
        self.gold_range = gold_range
        self.resistance = resistance or {}
        self.weakness = weakness or {}
        
        # État de combat
        self.is_stunned = False
        self.is_poisoned = False
        self.poison_damage = 0
        self.poison_duration = 0
        self.is_burning = False
        self.burn_damage = 0
        self.burn_duration = 0
        
    def __str__(self):
        """Représentation textuelle de l'ennemi"""
        health_percent = (self.health / self.max_health) * 100
        if health_percent > 70:
            status = "✅"
        elif health_percent > 30:
            status = "⚠️"
        else:
            status = "❌"
        return f"{status} {self.name} ({self.health}/{self.max_health} PV)"
    
    def is_alive(self):
        """Vérifie si l'ennemi est en vie"""
        return self.health > 0
    
    def take_damage(self, damage, damage_type="PHYSICAL"):
        """
        Inflige des dégâts à l'ennemi avec gestion des résistances/faiblesses
        
        Args:
            damage (int): Dégâts de base
            damage_type (str): Type de dégâts ("PHYSICAL", "MAGICAL", "FIRE", "ICE", "LIGHTNING")
            
        Returns:
            tuple: (dégâts réels, était critique)
        """
        # Appliquer résistances/faiblesses
        multiplier = 1.0
        
        if damage_type in self.resistance:
            multiplier *= (1 - self.resistance[damage_type])
        if damage_type in self.weakness:
            multiplier *= (1 + self.weakness[damage_type])
            
        actual_damage = int(damage * multiplier)
        
        # Réduction minimale de 1 dégât
        actual_damage = max(1, actual_damage)
        
        # Appliquer les dégâts
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
            
        # Messages spéciaux pour résistances/faiblesses
        message = ""
        if multiplier > 1.2:
            message = " C'est super efficace !"
        elif multiplier < 0.8:
            message = " L'ennemi résiste !"
            
        return actual_damage, message
    
    def apply_status_effect(self, effect_type, power, duration):
        """Applique un effet de statut à l'ennemi"""
        if effect_type == "POISON":
            self.is_poisoned = True
            self.poison_damage = power
            self.poison_duration = duration
        elif effect_type == "BURN":
            self.is_burning = True
            self.burn_damage = power
            self.burn_duration = duration
        elif effect_type == "STUN":
            self.is_stunned = True
    
    def process_status_effects(self):
        """Traite les effets de statut au début du tour"""
        effects = []
        
        if self.is_poisoned and self.poison_duration > 0:
            self.health -= self.poison_damage
            self.poison_duration -= 1
            effects.append(f"☠ Poison: -{self.poison_damage} PV")
            if self.poison_duration <= 0:
                self.is_poisoned = False
                
        if self.is_burning and self.burn_duration > 0:
            self.health -= self.burn_damage
            self.burn_duration -= 1
            effects.append(f"🔥 Brûlure: -{self.burn_damage} PV")
            if self.burn_duration <= 0:
                self.is_burning = False
                
        if self.is_stunned:
            effects.append("😵 Étourdi")
            self.is_stunned = False # Stun dure 1 tour
            
        return effects
    
    @abstractmethod
    def calculate_damage(self):
        """Calcule les dégâts infligés par l'ennemi"""
        pass
    
    def get_attack_description(self):
        """Retourne la description de l'attaque"""
        pass
    
    def drop_loot(self):
        """Génère le butin de l'ennemi"""
        gold = random.randint(self.gold_range[0], self.gold_range[1])
        return {
            "gold": gold,
            "experience": self.experience
        }
    
    def get_full_info(self):
        """Retourne des informations complètes sur l'ennemi"""
        info = f"=== {self.name.upper()} ===\n"
        info += f"Type: {self.enemy_type}\n"
        info += f"PV: {self.health}/{self.max_health}\n"
        info += f"Dégâts: {self.base_damage}\n"
        info += f"XP donné: {self.experience}\n"
        info += f"Or: {self.gold_range[0]}-{self.gold_range[1]} pièces\n"
        
        if self.resistance:
            info += "Résistances: "
            for dmg_type, value in self.resistance.items():
                info += f"{dmg_type} ({int(value*100)}%), "
            info = info.rstrip(", ") + "\n"
            
        if self.weakness:
            info += "Faiblesses: "
            for dmg_type, value in self.weakness.items():
                info += f"{dmg_type} (+{int(value*100)}%), "
            info = info.rstrip(", ") + "\n"
            
        return info


# ============================================================================
# ENNEMIS CONCRETS
# ============================================================================

class Goblin(Enemy):
    """Gobelin - Ennemi faible mais nombreux"""
    
    def __init__(self, variant="normal"):
        variants = {
            "normal": ("Gobelin", 20, 4, 10, (1, 5)),
            "archer": ("Gobelin Archer", 15, 5, 12, (2, 6)),
            "brute": ("Gobelin Brute", 30, 6, 15, (3, 8))
        }
        
        name, health, damage, exp, gold_range = variants.get(variant, variants["normal"])
        
        super().__init__(
            name=name,
            health=health,
            damage=damage,
            enemy_type="GOBELIN",
            experience=exp,
            gold_range=gold_range,
            weakness={"FIRE": 0.25}
        )
    
    def calculate_damage(self):
        """Les gobelins ont des attaques imprévisibles"""
        damage = random.randint(self.base_damage - 2, self.base_damage + 3)
        # 20% chance de coup faible, 10% chance de coup fort
        if random.random() < 0.2:
            damage = max(1, damage - 3)
        elif random.random() < 0.1:
            damage += 4
        return max(1, damage)
    
    def get_attack_description(self):
        """Description des attaques gobelines"""
        attacks = [
            f"{self.name} frappe avec sa massue rouillée !",
            f"{self.name} lance un caillou !",
            f"{self.name} mord sauvagement !",
            f"{self.name} attaque avec un couteau tordu !"
        ]
        return random.choice(attacks)


class Orc(Enemy):
    """Orc - Ennemi équilibré et résistant"""
    
    def __init__(self, rank="soldat"):
        ranks = {
            "soldat": ("Orc Soldat", 40, 8, 25, (5, 15)),
            "berserker": ("Orc Berserker", 35, 10, 30, (8, 20)),
            "chef": ("Orc Chef", 60, 12, 40, (15, 30))
        }
        
        name, health, damage, exp, gold_range = ranks.get(rank, ranks["soldat"])
        
        super().__init__(
            name=name,
            health=health,
            damage=damage,
            enemy_type="ORC",
            experience=exp,
            gold_range=gold_range,
            resistance={"PHYSICAL": 0.15},
            weakness={"MAGICAL": 0.20}
        )
    
    def calculate_damage(self):
        """Les orcs ont des attaques puissantes et stables"""
        damage = random.randint(self.base_damage - 1, self.base_damage + 2)
        # Les berserkers ont 25% de chance de coup enragé
        if "berserker" in self.name.lower() and random.random() < 0.25:
            damage = int(damage * 1.5)
        return max(1, damage)
    
    def get_attack_description(self):
        """Description des attaques orques"""
        if "berserker" in self.name.lower():
            attacks = [
                f"{self.name} rugit et attaque enragé !",
                f"{self.name} frappe avec une force bestiale !",
                f"{self.name} entre en frénésie !"
            ]
        else:
            attacks = [
                f"{self.name} attaque avec sa hache de guerre !",
                f"{self.name} frappe avec discipline martiale !",
                f"{self.name} exécute une attaque tournoyante !"
            ]
        return random.choice(attacks)


class Troll(Enemy):
    """Troll - Lent mais très résistant, régénère des PV"""
    
    def __init__(self, variant="caverne"):
        variants = {
            "caverne": ("Troll des Cavernes", 60, 10, 50, (20, 40)),
            "des_forets": ("Troll des Forêts", 55, 12, 60, (25, 45)),
            "des_montagnes": ("Troll des Montagnes", 70, 15, 80, (30, 60))
        }
        
        name, health, damage, exp, gold_range = variants.get(variant, variants["caverne"])
        
        super().__init__(
            name=name,
            health=health,
            damage=damage,
            enemy_type="TROLL",
            experience=exp,
            gold_range=gold_range,
            resistance={"PHYSICAL": 0.25, "MAGICAL": 0.10},
            weakness={"FIRE": 0.50}
        )
        
        self.regeneration = 3
    
    def calculate_damage(self):
        """Les trolls frappent lentement mais fort"""
        # 30% chance de rater à cause de la lenteur
        if random.random() < 0.3:
            return 0
        
        damage = random.randint(self.base_damage, self.base_damage + 5)
        # 15% chance de coup écrasant
        if random.random() < 0.15:
            damage = int(damage * 1.8)
        return max(1, damage)
    
    def get_attack_description(self):
        """Description des attaques de troll"""
        attacks = [
            f"{self.name} frappe de toute sa masse !",
            f"{self.name} attaque avec son gourdin géant !",
            f"{self.name} lance un rocher !",
            f"{self.name} tente de vous écraser !"
        ]
        return random.choice(attacks)
    
    def regenerate(self):
        """Le troll régénère des PV chaque tour"""
        if self.health > 0 and self.health < self.max_health:
            old_health = self.health
            self.health = min(self.max_health, self.health + self.regeneration)
            return self.health - old_health
        return 0


class Boss(Enemy):
    """Boss - Ennemi spécial avec phases et attaques spéciales"""
    
    def __init__(self, name, health, damage, phase_health=0.5, special_attacks=None):
        super().__init__(
            name=name,
            health=health,
            damage=damage,
            enemy_type="BOSS",
            experience=200,
            gold_range=(100, 200),
            resistance={"PHYSICAL": 0.20, "MAGICAL": 0.20}
        )
        
        self.max_health = health
        self.phase_health = int(health * phase_health)
        self.phase = 1
        self.special_attacks = special_attacks or []
        self.special_cooldown = 0
        self.enraged = False
    
    def calculate_damage(self):
        """Les boss ont des attaques variées"""
        # Vérifier la phase
        if self.health <= self.phase_health and self.phase == 1:
            self.phase = 2
            self.enraged = True
            print(f"\n⚡ {self.name} entre en phase 2 ! Il est enragé ! ⚡")
        
        # Attaque spéciale si disponible
        if self.special_attacks and self.special_cooldown <= 0 and random.random() < 0.3:
            self.special_cooldown = 3
            return self.use_special_attack()
        
        # Attaque normale avec bonus si enragé
        damage = random.randint(self.base_damage - 2, self.base_damage + 4)
        if self.enraged:
            damage = int(damage * 1.5)
            
        self.special_cooldown = max(0, self.special_cooldown - 1)
        return max(1, damage)
    
    def use_special_attack(self):
        """Utilise une attaque spéciale"""
        special = random.choice(self.special_attacks)
        damage = special["damage"]
        effect = special.get("effect")
        
        print(f"\n💥 {self.name} utilise {special['name']} !")
        if "description" in special:
            print(f" {special['description']}")
            
        # Appliquer les effets spéciaux
        if effect:
            print(f" Effet: {effect}")
            
        return damage
    
    def get_attack_description(self):
        """Description des attaques de boss"""
        if self.enraged:
            attacks = [
                f"{self.name} frappe avec une fureur démoniaque !",
                f"{self.name} rugit et attaque sans pitié !",
                f"{self.name} devient incontrôlable !"
            ]
        else:
            attacks = [
                f"{self.name} attaque avec une puissance terrible !",
                f"{self.name} utilise sa force écrasante !",
                f"{self.name} montre pourquoi il est le chef !"
            ]
        return random.choice(attacks)


# ============================================================================
# BOSS SPÉCIFIQUES DU JEU
# ============================================================================

class ChefGobelin(Boss):
    """Boss des Gobelins - Acte 3"""
    
    def __init__(self):
        special_attacks = [
            {
                "name": "Appel des Renforts",
                "damage": 5,
                "description": "Le chef appelle d'autres gobelins !"
            },
            {
                "name": "Coup Sournois",
                "damage": 12,
                "description": "Une attaque sournoise dans le dos !"
            },
            {
                "name": "Cri de Guerre",
                "damage": 8,
                "description": "Un cri qui étourdit l'ennemi !",
                "effect": "STUN"
            }
        ]
        
        super().__init__(
            name="Grok le Chef Gobelin",
            health=80,
            damage=10,
            phase_health=0.4,
            special_attacks=special_attacks
        )
        
        self.gold_range = (50, 100)
        self.experience = 100


class ChefTroll(Boss):
    """Boss des Trolls - Acte 5"""
    
    def __init__(self):
        special_attacks = [
            {
                "name": "Écrasement de Montagne",
                "damage": 25,
                "description": "Le troll frappe le sol avec une force titanesque !"
            },
            {
                "name": "Régénération Frénétique",
                "damage": 0,
                "description": "Le troll régénère rapidement ses blessures !",
                "effect": "HEAL_50"
            },
            {
                "name": "Lancer de Rocher",
                "damage": 18,
                "description": "Un énorme rocher est lancé avec précision !"
            }
        ]
        
        super().__init__(
            name="Borog le Chef Troll",
            health=120,
            damage=18,
            phase_health=0.3,
            special_attacks=special_attacks
        )
        
        self.gold_range = (150, 250)
        self.experience = 200
        self.regeneration = 5


class Morgrath(Boss):
    """Boss Final - Roi Démon - L'antagoniste principal du jeu"""
    
    def __init__(self):
        special_attacks = [
            {
                "name": "Vague de Corruption",
                "damage": 20,
                "description": "Une vague d'énergie démoniaque vous envahit !",
                "effect": "POISON"
            },
            {
                "name": "Flammes de la Haine",
                "damage": 25,
                "description": "Des flammes noires brûlent tout sur leur passage !",
                "effect": "BURN"
            },
            {
                "name": "Absorption d'Âme",
                "damage": 15,
                "description": "Morgrath absorbe votre vitalité !",
                "effect": "DRAIN"
            },
            {
                "name": "Apocalypse Démoniaque",
                "damage": 40,
                "description": "L'attaque ultime du Roi Démon ! Les cieux s'assombrissent !",
                "effect": "STUN"
            },
            {
                "name": "Légion d'Ombres",
                "damage": 22,
                "description": "Des créatures spectrales surgissent de l'obscurité !",
                "effect": "POISON"
            }
        ]
        
        super().__init__(
            name="Morgrath, le Roi Démon",
            health=250,
            damage=28,
            phase_health=0.5,
            special_attacks=special_attacks
        )
        
        self.max_health = 250
        self.gold_range = (500, 1000)
        self.experience = 500
        self.phase = 1
        self.phase_triggers = [200, 150, 100]
        self.enrage_threshold = 150
    
    def calculate_damage(self):
        """Morgrath a plusieurs phases avec des attaques de plus en plus puissantes"""
        # Vérifier les changements de phase
        for i, trigger in enumerate(self.phase_triggers):
            if self.health <= trigger and self.phase < i + 2:
                self.phase = i + 2
                print(f"\n" + "="*60)
                print(f"⚡ PHASE {self.phase} - MORGRATH INTENSIFIE SON ATTAQUE ! ⚡")
                print("="*60)
                # Augmenter les dégâts à chaque phase
                self.base_damage += 8
                
                # Messages spéciaux par phase
                if self.phase == 2:
                    print("Morgrath: Enfin, un adversaire qui mérite mon attention !")
                elif self.phase == 3:
                    print("Morgrath: Tu oses me défier dans mon propre domaine ?!")
                elif self.phase == 4:
                    print("Morgrath: Prépare-toi à connaître la véritable puissance !")
        
        # Chance d'attaque spéciale augmente selon la phase
        special_chance = 0.3 + (self.phase * 0.1)
        
        if self.special_attacks and self.special_cooldown <= 0 and random.random() < special_chance:
            self.special_cooldown = 2
            return self.use_special_attack()
        
        # Attaque normale avec bonus de phase
        damage = random.randint(self.base_damage - 3, self.base_damage + 8)
        damage = int(damage * (1 + (self.phase - 1) * 0.25))
        
        self.special_cooldown = max(0, self.special_cooldown - 1)
        return max(1, damage)
    
    def get_attack_description(self):
        """Description des attaques de Morgrath selon sa phase"""
        if self.phase >= 4:
            attacks = [
                f"{self.name} frappe avec une fureur apocalyptique !",
                f"{self.name} canalise l'énergie démoniaque ultime !",
                f"{self.name} devient une tempête de destruction !"
            ]
        elif self.phase == 3:
            attacks = [
                f"{self.name} attaque avec une rage croissante !",
                f"{self.name} libère des vagues d'énergie noire !",
                f"{self.name} s'élève au-dessus du sol, entouré de flammes !",
                f"{self.name} invoque le pouvoir des ombres !"
            ]
        elif self.phase == 2:
            attacks = [
                f"{self.name} frappe avec une puissance terrifiante !",
                f"{self.name} utilise son énergie démoniaque !",
                f"{self.name} vous regarde d'un air menaçant et attaque !",
                f"{self.name} canalise le pouvoir des anciens !"
            ]
        else:
            attacks = [
                f"{self.name} avance vers vous, hache levée !",
                f"{self.name} gronde d'une voix abyssale !",
                f"{self.name} vous fixe avec ses yeux rouges enflammés !",
                f"{self.name} commence à révéler sa véritable nature !"
            ]
        return random.choice(attacks)
    
    def get_full_info(self):
        """Informations détaillées sur Morgrath"""
        info = super().get_full_info()
        info += f"\nPhase actuelle: {self.phase}/4\n"
        info += f"Attaques spéciales: {len(self.special_attacks)}\n"
        info += "Attaques spéciales:\n"
        for attack in self.special_attacks:
            info += f"  - {attack['name']}: {attack['damage']} dégâts\n"
        return info


# ============================================================================
# CATALOGUE D'ENNEMIS
# ============================================================================

class EnemyCatalog:
    """Catalogue central de tous les ennemis du jeu"""
    
    @staticmethod
    def create_enemy(enemy_type, variant="normal"):
        """
        Crée une instance d'ennemi
        
        Args:
            enemy_type (str): Type d'ennemi ("GOBELIN", "ORC", "TROLL", "BOSS")
            variant (str): Variante spécifique
            
        Returns:
            Enemy: Instance de l'ennemi
        """
        enemy_classes = {
            "GOBELIN": Goblin,
            "ORC": Orc,
            "TROLL": Troll,
            "CHEF_GOBELIN": ChefGobelin,
            "CHEF_TROLL": ChefTroll,
            "MORGRATH": Morgrath
        }
        
        if enemy_type in enemy_classes:
            if enemy_type == "GOBELIN":
                return Goblin(variant)
            elif enemy_type == "ORC":
                return Orc(variant)
            elif enemy_type == "TROLL":
                return Troll(variant)
            else:
                return enemy_classes[enemy_type]()
        
        return None
    
    @staticmethod
    def get_enemy_info(enemy_type):
        """Retourne les informations sur un type d'ennemi"""
        enemy = EnemyCatalog.create_enemy(enemy_type)
        if enemy:
            return enemy.get_full_info()
        return f"Ennemi '{enemy_type}' non trouvé."