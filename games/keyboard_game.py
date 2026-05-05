import random


class KeyboardGame:
    def __init__(self):
        self.frases = [
            "El gat negre salta per la finestra.",
            "La programacio web es molt divertida.",
            "Python es un llenguatge orientat a objectes.",
            "Aquest joc serveix per practicar la mecanografia.",
            "Sempre he de tancar les etiquetes a HTML.",
        ]

    def obtenir_frase(self):
        return random.choice(self.frases)

    def calcular_puntuacio(self, correctes, incorrectes):
        punts = (correctes * 10) - (incorrectes * 5)
        return max(0, punts)
