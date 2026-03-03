class Usuari:
    def __init__(self, id_usuari, nom):
        self.id_usuari = id_usuari
        self.nom = nom
        self.puntuacio_total = 0

    def afegir_punts(self, punts):
        self.puntuacio_total += punts

    def __str__(self):
        return f"Usuari: {self.nom} | Puntuació total: {self.puntuacio_total}"