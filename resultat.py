class Resultat:
    def __init__(self, usuari, joc, punts):
        self.usuari = usuari
        self.joc = joc
        self.punts = punts

    def guardar(self):
        self.usuari.afegir_punts(self.punts)

    def __str__(self):
        return f"{self.usuari.nom} ha obtingut {self.punts} punts al joc {self.joc.nom}"