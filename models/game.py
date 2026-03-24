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

from .figures import ComplexShape

class DragAndDropGame(Game):
    def __init__(self):
        super().__init__("Drag and Drop", "mouse drag")

    @staticmethod
    def get_shapes():
        return [
            ComplexShape("yellow", "Estrella", 10),
            ComplexShape("red", "Creu", 12),
            ComplexShape("blue", "Hexàgon", 6),
            ComplexShape("green", "Rombe", 4),
            ComplexShape("purple", "Triangle", 3),
            ComplexShape("orange", "Pentàgon", 5),
            ComplexShape("cyan", "Octàgon", 8),
            ComplexShape("pink", "Fletxa", 7),
            ComplexShape("white", "Quadrat", 4),
            ComplexShape("magenta", "Cercle", 0),
            ComplexShape("brown", "Casa", 5),
            ComplexShape("lime", "Trapezi", 4)
        ]