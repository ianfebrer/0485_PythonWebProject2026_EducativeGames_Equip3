import random
import unicodedata


class MouseMoveGame:
    def __init__(self):
        # Aquí guardo totes les figures que pot demanar el joc.
        self.figures = [
            'Estrella',
            'Cor',
            'Flor',
            'Diamant',
            'Sol',
            'Lluna',
            'Núvol',
            'Llamp',
            'Floc De Neu',
            'Fulla',
            'Flama',
            'Cercle',
            'Triangle',
            'Quadrat',
            'Hexàgon'
        ]

    def obtenir_objectiu(self):
        # Trio una figura aleatòria per a la ronda actual.
        return random.choice(self.figures)

    def normalitzar_text(self, text):
        # Aquí normalitzo el text per evitar errors amb accents o majúscules.
        text = text.strip().lower()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        return text

    def validar_resposta(self, figura_objectiu, figura_seleccionada):
        # Aquí comprovo si l'usuari ha triat la figura correcta.
        objectiu_normalitzat = self.normalitzar_text(figura_objectiu)
        seleccionada_normalitzada = self.normalitzar_text(figura_seleccionada)
        return objectiu_normalitzat == seleccionada_normalitzada

    def calcular_punts(self, es_correcte):
        # Si encerta, suma 10 punts. Si falla, no suma res.
        if es_correcte:
            return 10
        return 0
