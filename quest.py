"""
quest.py - Système de gestion des quêtes pour "L'Héritage des Cendres"
"""

class Quest:
    """
    Classe représentant une quête du jeu.
    """
    def __init__(self, quest_id, title, description, objectives, reward, 
                 required_item=None, next_quest=None, auto_start=False):
        """
        Initialise une quête.

        Args:
            quest_id (str): Identifiant unique de la quête
            title (str): Titre de la quête
            description (str): Description narrative de la quête
            objectives (list[str]): Liste des objectifs à accomplir
            reward (dict): Récompense (ex: {'xp': 100, 'gold': 50, 'item': 'arc_dentrainement'})
            required_item (str, optional): Objet nécessaire pour commencer ou terminer la quête
            next_quest (str, optional): ID de la quête suivante à démarrer automatiquement
            auto_start (bool): Si True, la quête démarre automatiquement quand elle est débloquée
        """
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives
        self.reward = reward
        self.required_item = required_item
        self.next_quest = next_quest
        self.auto_start = auto_start

        self.completed_objectives = []
        self.is_active = False
        self.is_completed = False

    def start(self):
        """Active la quête."""
        if not self.is_active and not self.is_completed:
            self.is_active = True
            print(f"\n📜 Nouvelle quête : {self.title}\n{self.description}\n")
            print("Objectifs :")
            for i, obj in enumerate(self.objectives, 1):
                print(f"  {i}. {obj}")
            print()
            return True
        return False

    def complete_objective(self, objective):
        """Marque un objectif comme complété."""
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"✅ Objectif accompli : {objective}")
            
            # Vérifier si tous les objectifs sont complétés
            if set(self.completed_objectives) == set(self.objectives):
                self.complete_quest()
            return True
        return False

    def complete_quest(self):
        """Marque la quête comme terminée et affiche la récompense."""
        if not self.is_completed:
            self.is_completed = True
            self.is_active = False
            print(f"\n🏆 Quête terminée : {self.title}")
            print("Récompenses :")
            if 'xp' in self.reward:
                print(f" - {self.reward['xp']} points d'expérience")
            if 'gold' in self.reward:
                print(f" - {self.reward['gold']} pièces d'or")
            if 'item' in self.reward:
                print(f" - Objet obtenu : {self.reward['item']}")
            print()
            return True
        return False

    def get_status(self):
        """Retourne un résumé du statut de la quête."""
        status = "Terminée" if self.is_completed else "En cours" if self.is_active else "Non commencée"
        progress = f"{len(self.completed_objectives)}/{len(self.objectives)}"
        return f"{self.title} [{status}] - {progress} objectifs accomplis."

    def get_detailed_status(self):
        """Retourne un statut détaillé avec la liste des objectifs."""
        status_str = f"\n=== {self.title} ===\n"
        status_str += f"Statut: {'✓ Terminée' if self.is_completed else '⚡ En cours' if self.is_active else '○ Non commencée'}\n"
        status_str += f"Progression: {len(self.completed_objectives)}/{len(self.objectives)}\n"
        status_str += "\nObjectifs:\n"
        
        for obj in self.objectives:
            if obj in self.completed_objectives:
                status_str += f"  ✅ {obj}\n"
            else:
                status_str += f"  ○ {obj}\n"
        
        return status_str


class QuestManager:
    """Gestionnaire de toutes les quêtes du jeu"""
    
    def __init__(self, player):
        """
        Initialise le gestionnaire de quêtes
        
        Args:
            player: L'objet joueur
        """
        self.player = player
        self.all_quests = create_quests()
        self.active_quests = []
        self.completed_quests = []
        
    def start_quest(self, quest_id):
        """Démarre une quête par son ID"""
        if quest_id in self.all_quests:
            quest = self.all_quests[quest_id]
            if quest.start():
                if quest not in self.active_quests:
                    self.active_quests.append(quest)
                return True
        return False
    
    def complete_objective(self, quest_id, objective):
        """Complète un objectif d'une quête"""
        if quest_id in self.all_quests:
            quest = self.all_quests[quest_id]
            if quest.complete_objective(objective):
                # Si la quête est terminée, gérer la suite
                if quest.is_completed:
                    self.active_quests.remove(quest)
                    self.completed_quests.append(quest)
                    
                    # Donner les récompenses au joueur
                    self.give_rewards(quest)
                    
                    # Démarrer la quête suivante si elle existe
                    if quest.next_quest:
                        self.start_quest(quest.next_quest)
                    
                return True
        return False
    
    def give_rewards(self, quest):
        """Donne les récompenses d'une quête au joueur"""
        if 'xp' in quest.reward:
            # Pour l'instant, on affiche juste (système XP à implémenter)
            pass
        
        if 'gold' in quest.reward:
            self.player.gold += quest.reward['gold']
        
        if 'item' in quest.reward:
            # Ajouter l'objet à l'inventaire
            item_name = quest.reward['item']
            self.player.add_item(item_name, f"Récompense: {item_name}")
    
    def check_quest_triggers(self, location_name):
        """Vérifie si l'arrivée à un lieu déclenche des objectifs de quête"""
        for quest in self.active_quests:
            # Vérifier les objectifs liés aux lieux
            for objective in quest.objectives:
                if location_name.lower() in objective.lower() and objective not in quest.completed_objectives:
                    self.complete_objective(quest.quest_id, objective)
    
    def get_active_quests_string(self):
        """Retourne une string avec toutes les quêtes actives"""
        if not self.active_quests:
            return "\nAucune quête active pour le moment.\n"
        
        quests_str = "\n=== QUÊTES ACTIVES ===\n"
        for quest in self.active_quests:
            quests_str += quest.get_detailed_status()
            quests_str += "\n"
        
        return quests_str
    
    def get_all_quests_string(self):
        """Retourne une string avec toutes les quêtes (actives et complétées)"""
        result = "\n" + "="*50 + "\n"
        result += "JOURNAL DE QUÊTES\n"
        result += "="*50 + "\n"
        
        if self.active_quests:
            result += "\n--- QUÊTES ACTIVES ---\n"
            for quest in self.active_quests:
                result += quest.get_detailed_status()
        
        if self.completed_quests:
            result += "\n--- QUÊTES TERMINÉES ---\n"
            for quest in self.completed_quests:
                result += f"✓ {quest.title}\n"
        
        if not self.active_quests and not self.completed_quests:
            result += "\nAucune quête pour le moment.\n"
        
        result += "="*50 + "\n"
        return result


# =====================================================================
# CATALOGUE DE QUÊTES
# =====================================================================

def create_quests():
    """Crée le catalogue des quêtes disponibles dans le jeu."""
    quests = {
        # QUÊTE 1 : Arriver au camp des mentors
        "fuite_vers_camp": Quest(
            quest_id="fuite_vers_camp",
            title="La Fuite vers l'Espoir",
            description="Échappez au village en flammes et trouvez refuge au Camp des Mentors.",
            objectives=[
                "Fuir la chambre brûlante",
                "Traverser le village détruit",
                "Atteindre la Forêt Frontière",
                "Arriver au Camp des Mentors"
            ],
            reward={"xp": 50},
            next_quest="choix_de_la_voie",
            auto_start=True
        ),
        
        # QUÊTE 2 : Choisir sa voie (déclenchée automatiquement après la quête 1)
        "choix_de_la_voie": Quest(
            quest_id="choix_de_la_voie",
            title="Le Choix du Héros",
            description="Après 5 ans d'entraînement, vous devez choisir votre voie. "
                       "Arc, Épée ou Magie - votre décision façonnera votre destin.",
            objectives=[
                "Parler à Lyra ou Valerius",
                "Visiter la Zone d'Entraînement",
                "Choisir votre voie (arc, épée ou magie)"
            ],
            reward={"xp": 100, "gold": 50},
            next_quest="heritage_thrain",
            auto_start=True
        ),
        
        # QUÊTE 3 : L'héritage de Thrain
        "heritage_thrain": Quest(
            quest_id="heritage_thrain",
            title="L'Héritage de Thrain",
            description="L'esprit de Thrain vous confie une mission : retrouver son épée légendaire et honorer sa mémoire.",
            objectives=[
                "Rencontrer l'esprit de Thrain",
                "Explorer les ruines",
                "Récupérer l'Épée Barbe-de-Pierre"
            ],
            reward={"xp": 300, "item": "epee_barbe_de_pierre"},
            auto_start=False
        ),
        
        # QUÊTE 4 : Les captifs de Morgrath
        "sauvetage_prisonniers": Quest(
            quest_id="sauvetage_prisonniers",
            title="Les Captifs de Morgrath",
            description="Des prisonniers humains sont détenus dans les montagnes. Libérez-les avant qu'il ne soit trop tard.",
            objectives=[
                "Trouver l'entrée des cavernes",
                "Vaincre le gardien orc",
                "Libérer les captifs"
            ],
            reward={"xp": 200, "gold": 75},
            auto_start=False
        ),
        
        # QUÊTE FINALE : Confrontation avec Morgrath
        "confrontation_finale": Quest(
            quest_id="confrontation_finale",
            title="La Chute du Roi Démon",
            description="Le moment est venu. Morgrath vous attend dans son antre. "
                       "C'est l'heure de la vengeance... ou de la rédemption.",
            objectives=[
                "Atteindre l'Antre de Morgrath",
                "Affronter Morgrath",
                "Vaincre le Roi Démon"
            ],
            reward={"xp": 1000, "gold": 500},
            auto_start=False
        )
    }
    return quests


# Exemple d'utilisation
if __name__ == "__main__":
    # Simulation pour tester
    class MockPlayer:
        def __init__(self):
            self.gold = 0
            self.inventory = {}
        
        def add_item(self, item_name, item):
            self.inventory[item_name] = item
    
    # Test du système
    player = MockPlayer()
    quest_manager = QuestManager(player)
    
    print("=== TEST DU SYSTÈME DE QUÊTES ===\n")
    
    # Démarrer la première quête
    quest_manager.start_quest("fuite_vers_camp")
    
    # Compléter les objectifs
    print("\n--- Complétion des objectifs ---")
    quest_manager.complete_objective("fuite_vers_camp", "Fuir la chambre brûlante")
    quest_manager.complete_objective("fuite_vers_camp", "Traverser le village détruit")
    quest_manager.complete_objective("fuite_vers_camp", "Atteindre la Forêt Frontière")
    quest_manager.complete_objective("fuite_vers_camp", "Arriver au Camp des Mentors")
    
    # La quête suivante devrait se déclencher automatiquement
    print("\n--- État des quêtes ---")
    print(quest_manager.get_all_quests_string())
    
    # Compléter la deuxième quête
    print("\n--- Complétion de la quête 'Choix de la Voie' ---")
    quest_manager.complete_objective("choix_de_la_voie", "Parler à Lyra ou Valerius")
    quest_manager.complete_objective("choix_de_la_voie", "Visiter la Zone d'Entraînement")
    quest_manager.complete_objective("choix_de_la_voie", "Choisir votre voie (arc, épée ou magie)")
    
    print("\n--- État final ---")
    print(quest_manager.get_all_quests_string())
    print(f"\nOr du joueur: {player.gold}")
    print(f"Inventaire: {list(player.inventory.keys())}")