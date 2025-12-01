# Define the Character class for NPCs

class Character:
    """
    Classe pour les Personnages Non Joueurs (PNJ)
    """
    
    def __init__(self, name, description, current_room, dialogue_lines, character_type="NEUTRE", quest_related=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.dialogue_lines = dialogue_lines # Liste des répliques de dialogue
        self.character_type = character_type # "ALLIE", "ENNEMI", "NEUTRE", "MENTOR"
        self.quest_related = quest_related # Quête associée au PNJ
        self.dialogue_index = 0 # Index pour le cycle de dialogue
        self.has_met = False # Si le joueur a déjà rencontré ce PNJ
        
    def __str__(self):
        return f"{self.name} - {self.description}"
    
    def get_dialogue(self):
        """Retourne la prochaine réplique de dialogue (cyclique)"""
        if not self.dialogue_lines:
            return f"{self.name} n'a rien à dire."
        
        dialogue = self.dialogue_lines[self.dialogue_index]
        self.dialogue_index = (self.dialogue_index + 1) % len(self.dialogue_lines)
        
        # Marquer la première rencontre
        if not self.has_met:
            self.has_met = True
            
        return dialogue
    
    def move(self, available_rooms):
        """Déplace le PNJ aléatoirement dans une pièce adjacente"""
        import random
        
        # 30% de chance de se déplacer
        if random.random() < 0.3:
            possible_exits = list(self.current_room.exits.keys())
            if possible_exits:
                direction = random.choice(possible_exits)
                new_room = self.current_room.exits[direction]
                if new_room:
                    # Retirer de l'ancienne pièce et ajouter à la nouvelle
                    if self.name in self.current_room.characters:
                        del self.current_room.characters[self.name]
                    self.current_room = new_room
                    new_room.characters[self.name] = self
                    return True
        return False

# Catalogue de PNJ prédéfinis
def create_characters():
    """Crée le catalogue de PNJ du jeu"""
    return {
        # MENTORS
        "lyra": Character(
            name="Lyra",
            description="une elfe gracieuse aux cheveux argentés, votre mentor",
            current_room=None, # Sera défini plus tard
            dialogue_lines=[
                "Je suis Lyra. Je t'ai sauvé des ruines d'Alderwood il y a cinq ans...",
                "Ton village a été détruit par Morgrath. Nous devons arrêter cette folie.",
                "Choisis ta voie avec sagesse : l'arc pour la précision, la magie pour la puissance.",
                "Thrain s'est sacrifié pour nous sauver. N'oublie jamais son courage.",
                "La vengeance est un chemin dangereux. Assure-toi d'en être digne."
            ],
            character_type="MENTOR",
            quest_related="entrainement"
        ),
        
        "valerius": Character(
            name="Valerius", 
            description="un capitaine humain aux cicatrices honorables, votre mentor",
            current_room=None,
            dialogue_lines=[
                "Je suis Valerius. J'étais là quand Alderwood est tombé...",
                "Thrain était mon frère d'armes. Sa mort ne sera pas vaine.",
                "Une épée bien maniée vaut mieux que cent sorts maladroits.",
                "La force ne vient pas des muscles, mais de la détermination.",
                "Promets-moi de vivre en paix. La vengeance est un fardeau lourd à porter."
            ],
            character_type="MENTOR", 
            quest_related="entrainement"
        ),
        
        # PNJ IMPORTANTS
        "thrain_esprit": Character(
            name="Esprit de Thrain",
            description="l'esprit du nain héroïque qui vous a sauvé",
            current_room=None,
            dialogue_lines=[
                "Je suis Thrain Barbe-de-Pierre. Je veille sur toi depuis l'au-delà...",
                "Ne pleure pas ma mort. J'ai choisi mon destin pour te sauver.",
                "Un vrai héros se bat pour protéger, pas pour détruire.",
                "Rassemble les peuples. Seuls unis, vous vaincrez Morgrath.",
                "Sois plus fort que ta colère. Sois meilleur que tes ennemis."
            ],
            character_type="ALLIE",
            quest_related="heritage_thrain"
        ),
        
        "chef_gobelin": Character(
            name="Grok le Gobelin",
            description="le chef gobelin cruel et rusé",
            current_room=None, 
            dialogue_lines=[
                "Grok être chef ! Toi être viande pour la marmite !",
                "Armée de Morgrath écraser tous les humains !",
                "Grok savoir où elfes et humains être allés... mais Grok pas dire !",
                "Toi être trop faible pour battre Grok !",
                "Morgrath être trop fort pour petits humains !"
            ],
            character_type="ENNEMI",
            quest_related="interrogation_gobelins"
        ),
        
        "marchand_vagabond": Character(
            name="Boris le Vagabond",
            description="un marchand itinérant aux affaires douteuses",
            current_room=None,
            dialogue_lines=[
                "Des potions, des armes... Boris a tout ce qu'il faut !",
                "J'ai vu les héros passer par ici. Ils cherchaient des renforts...",
                "Les orcs ont un camp au nord. Fais attention, c'est bien gardé.",
                "Une potion de soin ? Seulement 25 pièces d'or !",
                "J'ai entendu dire que l'elfe Lyra était encore en vie..."
            ],
            character_type="NEUTRE",
            quest_related="marchandage"
        ),
        
        # PNJ SUPPLÉMENTAIRES POUR L'HISTOIRE
        "captif_orc": Character(
            name="Captif Humain",
            description="un prisonnier maltraité par les orcs",
            current_room=None,
            dialogue_lines=[
                "Aidez-moi... ils nous ont tous capturés...",
                "Lyra était ici ! Ils l'ont emmenée plus profondément dans les montagnes...",
                "Les trolls gardent quelque chose... ou quelqu'un...",
                "Morgrath... ce nom me glace le sang...",
                "Fuyez pendant que vous le pouvez..."
            ],
            character_type="ALLIE",
            quest_related="sauvetage_prisonniers"
        ),
        
        "sage_elfe": Character(
            name="Eldrin le Sage",
            description="un vieil elfe connaissant les secrets anciens",
            current_room=None,
            dialogue_lines=[
                "Je vois le même feu dans tes yeux que dans ceux de Lyra...",
                "Morgrath n'était pas toujours un démon. C'était un homme autrefois...",
                "La magie qu'il utilise corrompt autant qu'elle renforce.",
                "Ton destin est lié au sien, jeune héros.",
                "La clé de sa défaite se trouve dans son passé..."
            ],
            character_type="ALLIE",
            quest_related="verite_morgrath"
        ),
        
        "forgeron_nain": Character(
            name="Durin Forge-acier",
            description="un forgeron nain expert en armures",
            current_room=None,
            dialogue_lines=[
                "Thrain était mon ami. Sa perte est une tragédie pour notre peuple.",
                "Prends cette armure. Elle protégera mieux que les mots.",
                "Les nains se souviennent. Nous n'oublions pas nos héros.",
                "Pour battre Morgrath, il faudra plus qu'une simple épée.",
                "Son armure a une faille... cherche le symbole du phénix..."
            ],
            character_type="ALLIE",
            quest_related="equipement_special"
        ),
        
        "morgrath": Character(
            name="Morgrath",
            description="le Roi Démon, source de toute cette destruction",
            current_room=None,
            dialogue_lines=[
                "Enfin... le dernier survivant d'Alderwood...",
                "Tu cherches la vengeance ? Comme je l'ai cherchée autrefois...",
                "Mon village aussi a été détruit. Par les humains.",
                "Je ne fais que rendre ce qu'on m'a donné.",
                "La boucle est bouclée. Toi ou moi..."
            ],
            character_type="ENNEMI",
            quest_related="confrontation_finale"
        )
    }

CHARACTER_CATALOG = create_characters()

def get_character(character_name):
    """Retourne une instance de PNJ par son nom"""
    if character_name in CHARACTER_CATALOG:
        original = CHARACTER_CATALOG[character_name]
        # Créer une nouvelle instance pour éviter les références partagées
        new_character = Character(
            original.name, 
            original.description, 
            original.current_room,
            original.dialogue_lines.copy(), # Copie de la liste pour l'indépendance
            original.character_type, 
            original.quest_related
        )
        return new_character
    return None

def move_all_characters(rooms):
    """Déplace tous les PNJ dans toutes les pièces"""
    moved_characters = []
    
    for room in rooms:
        characters_to_move = list(room.characters.items()) # Copie pour éviter les modifications pendant l'itération
        
        for char_name, character in characters_to_move:
            # Ne pas déplacer certains PNJ importants
            if character.character_type in ["MENTOR", "BOSS"]:
                continue
                
            if character.move(rooms):
                moved_characters.append(character.name)
    
    return moved_characters