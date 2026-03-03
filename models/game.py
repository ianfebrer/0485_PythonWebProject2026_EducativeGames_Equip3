class Game:
    def __init__(self, name, interaction_type):
        # Defineix el nom del joc i el tipus d'interacció (teclat, ratolí, etc.)
        self.name = name
        self.interaction_type = interaction_type

    def start(self):
        # Mostra un missatge quan el joc comença
        print(f"Game '{self.name}' has started.")

    def finish(self):
        # Mostra un missatge quan el joc acaba
        print(f"Game '{self.name}' has finished.")