class GameGUI(tk.Tk):
    """Interface graphique principale du jeu."""

    def __init__(self, game):
        super().__init__()

        self.game = game
        self.title("Ashes of Alderwood - GUI")
        self.geometry("800x600")

        # Zone de texte (scrollable) pour afficher les messages
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Rediriger print vers text_area
        sys.stdout = _StdoutRedirector(self.text_area)

        # Commande entrée
        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.entry.bind("<Return>", self.on_enter)

        # Bouton envoyer
        self.send_button = tk.Button(self, text="Envoyer", command=self.on_enter)
        self.send_button.grid(row=1, column=3)

        # Boutons exemple (on peut ajouter Directions)
        self.btn_go_north = tk.Button(self, text="Aller Nord", command=lambda: self.handle("go n"))
        self.btn_go_north.grid(row=2, column=0)

        self.btn_go_south = tk.Button(self, text="Aller Sud", command=lambda: self.handle("go s"))
        self.btn_go_south.grid(row=2, column=1)

        self.btn_talk = tk.Button(self, text="Parler", command=lambda: self.handle("talk lyra"))
        self.btn_talk.grid(row=2, column=2)

        self.btn_quests = tk.Button(self, text="Quêtes", command=lambda: self.handle("quests"))
        self.btn_quests.grid(row=2, column=3)

        # Ajustements layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2,3), weight=1)

    def on_enter(self, event=None):
        """Récupère le texte de l’Entry."""
        text = self.entry.get().strip()
        if text:
            print(f"> {text}")
            self.handle(text)
            self.entry.delete(0, tk.END)

    def handle(self, command_text):
        """Appelle le moteur de jeu avec la commande."""
        list_of_words = command_text.lower().split()
        cmd = list_of_words[0]

        if cmd not in self.game.commands:
            print("\nCommande inconnue. Tapez help.")
            return

        command = self.game.commands[cmd]
        command.action(self.game, list_of_words, command.number_of_parameters)
