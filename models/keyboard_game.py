import random

class KeyboardGame:
    def __init__(self):
        # Llista de frases predefinides. En pots afegir tantes com vulguis!
        self.frases = [
            "El gat negre salta per la finestra.",
            "La programacio web es molt divertida.",
            "Python es un llenguatge orientat a objectes.",
            "Aquest joc serveix per practicar la mecanografia.",
            "Sempre he de tancar les etiquetes a HTML."
        ]

    def obtenir_frase(self):
        # Retorna una frase aleatòria de la llista
        return random.choice(self.frases)

    def calcular_puntuacio(self, correctes, incorrectes):
        # Sistema de puntuació senzill:
        # +10 punts per lletra correcta, -5 punts per cada error
        punts = (correctes * 10) - (incorrectes * 5)
        
        # Ens assegurem que la puntuació mai sigui per sota de 0
        if punts < 0:
            return 0
        return punts