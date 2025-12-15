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
        
        # Directions autorisées dans le jeu
        self.allowed_directions = [
            "N", "S", "E", "O", "U", "D", # Cardinales
            "PORTE", "FENETRE", "GAUCHE", "DROITE", "CENTRE", # Spéciales
            "FORET", "ENTRAINEMENT", "VENGEANCE", "ENTRER", "SORTIR",
            "RETOUR", "CONTINUER", "INFILTRATION", "ASSAUT"
        ]
        
        # Variables de debug
        self.DEBUG = True
        
    def setup(self):
        """Configure le jeu : crée joueur, pièces, commandes"""
        self.show_intro()
        
        # Création du joueur
        self.create_player()
        
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
            "Un orc massif vous bloque le chemin. Ses yeux brûlent de haine."
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
        
        # ACTE 2 - ENTRAÎNEMENT (3 pièces)
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
        
        # Connecter les pièces de l'Acte 1
        self.rooms["CHAMBRE_BRULANTE"].exits = {
            "PORTE": self.rooms["RUE_PRINCIPALE"],
            "FENETRE": None # Game over
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
        
        self.rooms["RENCONTRE_ORC"].exits = {
            "COMBATTRE": None, # À implémenter
            "FUIR": self.rooms["ECOULEMENT"]
        }
        
        self.rooms["ECOULEMENT"].exits = {
            "RETOUR": self.rooms["RUE_PRINCIPALE"]
        }
        
        self.rooms["FORET_FRONTIERE"].exits = {
            "CONTINUER": self.rooms["CAMP_MENTORS"]
        }
        
        # Connecter les pièces de l'Acte 2
        self.rooms["CAMP_MENTORS"].exits = {
            "ENTRAINEMENT": self.rooms["ZONE_ENTRAINEMENT"],
            "FORET": self.rooms["CLAIRIERE_ADIEU"]
        }
        
        self.rooms["ZONE_ENTRAINEMENT"].exits = {
            "RETOUR": self.rooms["CAMP_MENTORS"]
        }
        
        self.rooms["CLAIRIERE_ADIEU"].exits = {
            "RETOUR": self.rooms["CAMP_MENTORS"],
            "VENGEANCE": None # Transition vers Acte 3
        }
        
        # Ajouter des objets dans certaines pièces
        self.add_initial_items()
        
        # Ajouter des PNJ
        self.add_initial_characters()
        
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
            "stats": Command("stats", " - Voir vos statistiques", self.show_stats, 0),
            "fight": Command("fight", " - Combattre un ennemi", Actions.fight, 1),
            "combattre": Command("combattre", " - Combattre", Actions.fight, 1),
            "talk": Command("talk", " - Parler à un PNJ", self.talk_to_character, 1),
            "parler": Command("parler", " - Parler à un PNJ", self.talk_to_character, 1),
            "debug": Command("debug", " - Mode debug (affiche toutes les infos)", self.debug_mode, 0)
        }
        
    def show_stats(self, list_of_words=None, number_of_parameters=0):
        """Affiche les statistiques du joueur (commande stats)"""
        print(self.player.get_stats_string())
        return True
        
    def talk_to_character(self, list_of_words, number_of_parameters):
        """Parler à un PNJ (à intégrer plus tard dans actions.py)"""
        if len(list_of_words) != 2:
            print("\nUsage: talk <nom_du_pnj>")
            return False
            
        character_name = list_of_words[1].lower()
        current_room = self.player.current_room
        
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
        
        if character.quest_related:
            print(f"Quête associée: {character.quest_related}")
            
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
            return command.action(self, words, command.number_of_parameters)
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