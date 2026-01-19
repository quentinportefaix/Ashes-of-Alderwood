"""
game.py - Moteur principal du jeu "L'Héritage des Cendres"
Connecte toutes les classes et gère la boucle de jeu principale
"""

import sys
import time
from room import Room
from player import Player
from command import Command
from character import Character, get_character, move_all_characters
from actions import Actions
from quest import QuestManager  # NOUVEAU : Import du gestionnaire de quêtes

class Game:
    """Classe principale qui gère l'état global du jeu"""
    
    def __init__(self):
        """Initialise le jeu avec des valeurs par défaut"""
        self.finished = False
        self.player = None
        self.rooms = {}
        self.commands = {}
        self.current_act = 1
        self.turn_count = 0
        self.quest_manager = None  # NOUVEAU : Gestionnaire de quêtes
        
        # Directions autorisées dans le jeu
        self.allowed_directions = [
            "N", "S", "E", "O", "U", "D", # Cardinales
            "PORTE", "FENETRE", "GAUCHE", "DROITE", "CENTRE", # Spéciales
            "FORET", "ENTRAINEMENT", "VENGEANCE", "ENTRER", "SORTIR",
            "RETOUR", "CONTINUER", "INFILTRATION", "ASSAUT", "VALLEE"
        ]
        
        # Variables de debug
        self.DEBUG = True
        
    def setup(self):
        """Configure le jeu : crée joueur, pièces, commandes"""
        self.show_intro()
        
        # Création du joueur
        self.create_player()
        
        # NOUVEAU : Initialiser le gestionnaire de quêtes
        self.quest_manager = QuestManager(self.player)
        # Démarrer la première quête automatiquement
        self.quest_manager.start_quest("fuite_vers_camp")
        
        # Création du monde
        self.create_world()
        
        # Initialisation des commandes
        self.setup_commands()
        
        # Position initiale
        self.player.current_room = self.rooms["CHAMBRE_BRULANTE"]
        
        print("\n" + "="*50)
        print("Le jeu est prêt. Tapez 'help' pour voir les commandes disponibles.")
        print("="*50)
        
    def show_intro(self):
        """Affiche l'introduction du jeu"""
        print("\n" + "="*60)
        print("L'HÉRITAGE DES CENDRES")
        print("Ashes of Alderwood")
        print("="*60)
        print("\nIl y a 5 ans, le village d'Alderwood a été réduit en cendres.")
        print("Vous êtes le dernier survivant. Votre voyage commence maintenant...")
        print("\nAppuyez sur Entrée pour commencer...")
        input()
        
    def create_player(self):
        """Crée le personnage du joueur"""
        print("\n" + "-"*40)
        name = input("Quel est votre nom, survivant d'Alderwood ? ").strip()
        if not name:
            name = "Survivant"
        
        self.player = Player(name)
        print(f"\nBienvenue, {name}. Votre quête pour la justice commence.")
        
    def create_world(self):
        """Crée toutes les pièces du jeu et les connecte"""
        print("\nCréation du monde...")
        
        # ACTE 1 - FUITE (6 pièces)
        self.rooms["CHAMBRE_BRULANTE"] = Room(
            "Chambre Brûlante",
            "Votre chambre d'enfance est en flammes. La chaleur est insupportable."
        )
        
        self.rooms["RUE_PRINCIPALE"] = Room(
            "Rue Principale",
            "La rue du village est jonchée de cadavres. Des cris résonnent au loin. "
            "Trois chemins s'offrent à vous."
        )
        
        self.rooms["TROU_MUR"] = Room(
            "Trou dans le Mur",
            "Vous avez trouvé une brèche dans le mur de la maison voisine. "
            "C'est étroit mais praticable."
        )
        
        self.rooms["RENCONTRE_ORC"] = Room(
            "Rencontre Fatale",
            "Un orc massif vous bloque le chemin. Ses yeux brûlent de haine. "
            "Vous devez fuir pour sauver votre vie !"
            "⚠️ INSTRUCTION: Tapez 'back' pour vous échapper !"
        )
        
        self.rooms["ECOULEMENT"] = Room(
            "Écoulement",
            "Vous retournez à votre point de départ. Le feu gagne du terrain."
        )
        
        self.rooms["FORET_FRONTIERE"] = Room(
            "Forêt Frontière",
            "Vous avez réussi à fuir le village. La forêt sombre s'étend devant vous. "
            "ACTE 1 TERMINÉ - 5 ans plus tard..."
        )
        
        # ACTE 2 - ENTRAÎNEMENT (4 pièces)
        self.rooms["CAMP_MENTORS"] = Room(
            "Camp des Mentors",
            "5 ans ont passé. Lyra et Valerius vous ont entraîné. "
            "Il est temps de choisir votre voie."
        )
        
        self.rooms["ZONE_ENTRAINEMENT"] = Room(
            "Zone d'Entraînement",
            "Un terrain de pratique avec des cibles et des mannequins. "
            "C'est ici que vous avez passé la plupart de votre temps."
        )
        
        self.rooms["CLAIRIERE_ADIEU"] = Room(
            "Clairière des Adieux",
            "Un endroit paisible où vous avez fait la promesse "
            "de ne jamais chercher la vengeance... une promesse brisée."
        )
        
        self.rooms["CHEMIN_VALLEE_DEMONIAQUE"] = Room(
            "Chemin de la Vallée Démoniaque",
            "Un sentier sinueux qui s'enfonce dans les terres sombres. "
            "L'air devient froid et suffocant. Des cris lointains résonnent "
            "à travers la vallée. Des ombres étranges dansent entre les arbres. "
            "Vous sentez que vous vous approchez du siège du pouvoir de Morgrath..."
        )
        
        self.rooms["ANTRE_MORGRATH"] = Room(
            "Antre de Morgrath",
            "Vous vous trouvez enfin face à face avec votre destin. "
            "L'antre de Morgrath s'étend devant vous, une caverne immense aux murs "
            "de pierre noire suintant d'une énergie maléfique. Des flammes vertes "
            "dansent sur le sol. Au loin, assis sur un trône de crânes, Morgrath "
            "vous observe. Ses yeux rouges brillent d'une haine millénaire. "
            "Le moment tant attendu est enfin arrivé. Votre vendetta prend fin ici. "
            "\n\n⚔️ COMBAT FINAL IMMINENT ⚔️\n"
            "Utilisez la commande 'fight morgrath' pour affronter le Roi Démon !"
        )
        
        # Connecter les pièces de l'Acte 1
        self.rooms["CHAMBRE_BRULANTE"].exits = {
            "PORTE": self.rooms["RUE_PRINCIPALE"],
            "FENETRE": None
        }
        
        self.rooms["RUE_PRINCIPALE"].exits = {
            "GAUCHE": self.rooms["TROU_MUR"],
            "DROITE": self.rooms["RENCONTRE_ORC"],
            "CENTRE": self.rooms["ECOULEMENT"],
            "RETOUR": self.rooms["CHAMBRE_BRULANTE"]
        }
        
        self.rooms["TROU_MUR"].exits = {
            "CONTINUER": self.rooms["FORET_FRONTIERE"],
            "RETOUR": self.rooms["RUE_PRINCIPALE"]
        }
        
        self.rooms["RENCONTRE_ORC"].exits = {}
        
        self.rooms["ECOULEMENT"].exits = {
            "RETOUR": self.rooms["RUE_PRINCIPALE"]
        }
        
        self.rooms["FORET_FRONTIERE"].exits = {
            "CONTINUER": self.rooms["CAMP_MENTORS"]
        }
        
        # Connecter les pièces de l'Acte 2
        self.rooms["CAMP_MENTORS"].exits = {
            "ENTRAINEMENT": self.rooms["ZONE_ENTRAINEMENT"],
            "FORET": self.rooms["CLAIRIERE_ADIEU"],
            "VALLEE": self.rooms["CHEMIN_VALLEE_DEMONIAQUE"]
        }
        
        self.rooms["ZONE_ENTRAINEMENT"].exits = {
            "RETOUR": self.rooms["CAMP_MENTORS"]
        }
        
        self.rooms["CLAIRIERE_ADIEU"].exits = {
            "RETOUR": self.rooms["CAMP_MENTORS"],
            "VENGEANCE": None
        }
        
        self.rooms["CHEMIN_VALLEE_DEMONIAQUE"].exits = {
            "RETOUR": self.rooms["CAMP_MENTORS"],
            "CONTINUER": self.rooms["ANTRE_MORGRATH"]
        }
        
        self.rooms["ANTRE_MORGRATH"].exits = {
            "RETOUR": self.rooms["CHEMIN_VALLEE_DEMONIAQUE"]
        }
        
        # Ajouter des objets dans certaines pièces
        self.add_initial_items()
        
        # Ajouter des PNJ
        self.add_initial_characters()
        
        # Ajouter des ennemis
        self.add_initial_enemies()
        
        print(f"Monde créé avec {len(self.rooms)} pièces.")
        
    def add_initial_items(self):
        """Ajoute des objets initiaux dans le monde"""
        # Pour l'instant, on utilise des dictionnaires simples
        # Plus tard, remplacer par des instances de Item
        
        # Objets dans la chambre brûlante
        self.rooms["CHAMBRE_BRULANTE"].inventory = {
            "journal": "Votre vieux journal, à moitié brûlé",
            "medaillon": "Un médaillon avec le portrait de vos parents"
        }
        
        # Objets dans la zone d'entraînement
        self.rooms["ZONE_ENTRAINEMENT"].inventory = {
            "arc": "Un arc d'entraînement en frêne",
            "epee": "Une épée en bois pour la pratique",
            "grimoire": "Un grimoire de sorts élémentaires"
        }
        
    def add_initial_characters(self):
        """Ajoute des PNJ initiaux dans le monde"""
        # Créer des instances de PNJ depuis le catalogue
        lyra = get_character("lyra")
        if lyra:
            lyra.current_room = self.rooms["CAMP_MENTORS"]
            self.rooms["CAMP_MENTORS"].add_character("lyra", lyra)
            
        valerius = get_character("valerius")
        if valerius:
            valerius.current_room = self.rooms["CAMP_MENTORS"]
            self.rooms["CAMP_MENTORS"].add_character("valerius", valerius)
        
        # Ajouter Morgrath dans son antre
        morgrath = get_character("morgrath")
        if morgrath:
            morgrath.current_room = self.rooms["ANTRE_MORGRATH"]
            self.rooms["ANTRE_MORGRATH"].add_character("morgrath", morgrath)
    
    def add_initial_enemies(self):
        """Ajoute les ennemis initiaux dans le monde"""
        from enemy import EnemyCatalog
        
        # Ajouter Morgrath comme ennemi dans son antre
        morgrath_enemy = EnemyCatalog.create_enemy("MORGRATH")
        if morgrath_enemy:
            self.rooms["ANTRE_MORGRATH"].add_enemy("morgrath", morgrath_enemy)
            
    def setup_commands(self):
        """Configure toutes les commandes disponibles"""
        self.commands = {
            "go": Command("go", " - Se déplacer dans une direction", Actions.go, 1),
            "aller": Command("aller", " - Se déplacer (synonyme de go)", Actions.go, 1),
            "quit": Command("quit", " - Quitter le jeu", Actions.quit, 0),
            "quitter": Command("quitter", " - Quitter le jeu", Actions.quit, 0),
            "help": Command("help", " - Afficher l'aide", Actions.help, 0),
            "aide": Command("aide", " - Afficher l'aide", Actions.help, 0),
            "back": Command("back", " - Revenir à la pièce précédente", Actions.back, 0),
            "retour": Command("retour", " - Revenir en arrière", Actions.back, 0),
            "history": Command("history", " - Voir l'historique des pièces visitées", Actions.history, 0),
            "historique": Command("historique", " - Voir l'historique", Actions.history, 0),
            "look": Command("look", " - Observer attentivement la pièce", Actions.look, 0),
            "observer": Command("observer", " - Observer la pièce", Actions.look, 0),
            "take": Command("take", " - Prendre un objet", Actions.take, 1),
            "prendre": Command("prendre", " - Prendre un objet", Actions.take, 1),
            "drop": Command("drop", " - Déposer un objet", Actions.drop, 1),
            "poser": Command("poser", " - Déposer un objet", Actions.drop, 1),
            "check": Command("check", " - Vérifier votre inventaire et stats", Actions.check, 0),
            "inventaire": Command("inventaire", " - Voir l'inventaire", Actions.check, 0),
            "stats": Command("stats", " - Voir vos statistiques", Actions.check, 0),
            "fight": Command("fight", " - Combattre un ennemi", Actions.fight, 1),
            "combattre": Command("combattre", " - Combattre", Actions.fight, 1),
            "talk": Command("talk", " - Parler à un PNJ", Actions.talk, 1),
            "parler": Command("parler", " - Parler à un PNJ", Actions.talk, 1),
            "choose": Command("choose", " - Choisir votre voie (arc, épée, magie)", Actions.choose, 1),
            "choisir": Command("choisir", " - Choisir votre voie", Actions.choose, 1),
            "debug": Command("debug", " - Mode debug (affiche toutes les infos)", self.debug_mode, 0),
            "fuir": Command("fuir", " - Fuir une situation dangereuse", Actions.go, 1),
            "flee": Command("flee", " - Flee a dangerous situation", Actions.go, 1),
            # NOUVEAU : Commandes de quêtes
            "quests": Command("quests", " - Voir vos quêtes", self.show_quests, 0),
            "quetes": Command("quetes", " - Voir vos quêtes", self.show_quests, 0),
            "journal": Command("journal", " - Ouvrir le journal de quêtes", self.show_quests, 0),
        }
        
    def show_stats(self, list_of_words=None, number_of_parameters=0):
        """Affiche les statistiques du joueur (commande stats)"""
        print(self.player.get_stats_string())
        return True
    
    # NOUVEAU : Méthode pour afficher les quêtes
    def show_quests(self, list_of_words=None, number_of_parameters=0):
        """Affiche les quêtes actives"""
        if self.quest_manager:
            print(self.quest_manager.get_all_quests_string())
        else:
            print("\nAucune quête disponible pour le moment.\n")
        return True
    
    def debug_mode(self, list_of_words=None, number_of_parameters=0):
        """Mode debug - affiche toutes les informations"""
        if not self.DEBUG:
            print("\nMode debug désactivé.")
            return False
            
        print("\n" + "="*60)
        print("DEBUG MODE - Informations complètes")
        print("="*60)
        
        # Info joueur
        print(f"\nJOUEUR: {self.player.name}")
        print(f"Pièce actuelle: {self.player.current_room.name}")
        print(f"PV: {self.player.health}/{self.player.max_health}")
        print(f"Voie choisie: {self.player.chosen_path}")
        
        # Info pièce actuelle
        room = self.player.current_room
        print(f"\nPIÈCE: {room.name}")
        print(f"Description: {room.description}")
        print(f"Sorties: {list(room.exits.keys())}")
        print(f"Objets: {list(room.inventory.keys())}")
        print(f"PNJ: {list(room.characters.keys())}")
        
        # NOUVEAU : Info quêtes
        if self.quest_manager:
            print(f"\nQUÊTES ACTIVES: {len(self.quest_manager.active_quests)}")
            for quest in self.quest_manager.active_quests:
                print(f"  - {quest.title}: {len(quest.completed_objectives)}/{len(quest.objectives)} objectifs")
        
        # Commandes disponibles
        print(f"\nCOMMANDES DISPONIBLES ({len(self.commands)}):")
        for cmd_name, cmd in self.commands.items():
            print(f" {cmd_name}: {cmd.help_string}")
            
        print("="*60)
        return True
        
    def process_command(self, command_input):
        """Traite une commande entrée par le joueur"""
        if not command_input:
            return
            
        words = command_input.strip().split()
        command_word = words[0].lower()
        
        # Commandes spéciales sans objet Command
        if command_word in ["n", "s", "e", "o", "nord", "sud", "est", "ouest"]:
            # Convertir en commande go
            direction = words[0].upper()
            if direction in ["NORD", "SUD", "EST", "OUEST"]:
                direction = direction[0] # Prendre première lettre
            return Actions.go(self, ["go", direction], 1)
            
        # Commandes normales
        if command_word in self.commands:
            command = self.commands[command_word]
            
            # Vérifier le nombre de paramètres
            if len(words) - 1 != command.number_of_parameters:
                if command.number_of_parameters == 0:
                    print(f"\nLa commande '{command_word}' ne prend pas de paramètre.")
                else:
                    print(f"\nLa commande '{command_word}' prend {command.number_of_parameters} paramètre(s).")
                return False
                
            # Exécuter la commande
            success = command.action(self, words, command.number_of_parameters)
            
            # NOUVEAU : Après une action réussie, vérifier les déclencheurs de quêtes
            if success and self.player.current_room and self.quest_manager:
                self.quest_manager.check_quest_triggers(self.player.current_room.name)
            
            return success
        else:
            print(f"\nCommande inconnue: '{command_word}'")
            print("Tapez 'help' pour voir les commandes disponibles.")
            return False
            
    def update_game_state(self):
        """Met à jour l'état du jeu à chaque tour"""
        self.turn_count += 1
        
        # Déplacer les PNJ périodiquement
        if self.turn_count % 5 == 0: # Tous les 5 tours
            moved_chars = move_all_characters(self.rooms.values())
            if moved_chars and self.DEBUG:
                print(f"\n[DEBUG] PNJ déplacés: {', '.join(moved_chars)}")
                
        # Vérifier si le joueur est mort
        if not self.player.is_alive():
            print("\n" + "="*50)
            print("GAME OVER")
            print("="*50)
            print("Vous avez succombé à vos blessures...")
            print("Votre quête s'arrête ici, mais votre légende perdurera.")
            print("="*50)
            self.finished = True
            return
            
    def play(self):
        """Boucle principale du jeu"""
        print("\n" + "="*50)
        print("DEBUT DE L'AVENTURE")
        print("="*50)
        
        # Afficher la pièce initiale
        print(self.player.current_room.get_long_description())
        
        # Boucle de jeu principale
        while not self.finished:
            try:
                # Invite de commande
                command_input = input(f"\n[{self.player.name}] > ").strip()
                
                # Traiter la commande
                if command_input:
                    success = self.process_command(command_input)
                    
                    # Mettre à jour l'état du jeu
                    self.update_game_state()
                    
            except KeyboardInterrupt:
                print("\n\nInterruption du jeu. Sauvegarde...")
                self.finished = True
            except EOFError:
                print("\n\nFin de fichier détectée. Quitter...")
                self.finished = True
            except Exception as e:
                if self.DEBUG:
                    print(f"\n[ERREUR] {e}")
                    import traceback
                    traceback.print_exc()
                else:
                    print("\nUne erreur est survenue. Veuillez réessayer.")
                    
        self.show_ending()
        
    def show_ending(self):
        """Affiche l'écran de fin"""
        print("\n" + "="*50)
        print("FIN DU JEU")
        print("="*50)
        print(f"Merci d'avoir joué à 'L'Héritage des Cendres', {self.player.name}!")
        print(f"Nombre de tours joués: {self.turn_count}")
        
        # NOUVEAU : Afficher les statistiques de quêtes
        if self.quest_manager:
            print(f"Quêtes terminées: {len(self.quest_manager.completed_quests)}")
            print(f"Quêtes actives: {len(self.quest_manager.active_quests)}")
        
        print("="*50)
        
    def save_game(self, filename="savegame.json"):
        """Sauvegarde l'état du jeu (à implémenter)"""
        print("\nFonction de sauvegarde non implémentée dans cette version.")
        return False
        
    def load_game(self, filename="savegame.json"):
        """Charge un jeu sauvegardé (à implémenter)"""
        print("\nFonction de chargement non implémentée dans cette version.")
        return False


def main():
    """Point d'entrée principal du jeu"""
    try:
        game = Game()
        game.setup()
        game.play()
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        print("\nLe jeu a rencontré une erreur et doit s'arrêter.")
    finally:
        print("\nAu revoir !")


# Point d'entrée
if __name__ == "__main__":
    main()