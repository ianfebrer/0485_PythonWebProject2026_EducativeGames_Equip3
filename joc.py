class Joc:
    def __init__(self, nom):
        self.nom = nom
        self.usuaris = []

    def afegir_usuari(self, usuari):
        self.usuaris.append(usuari)

    def iniciar(self):
        print(f"El joc '{self.nom}' ha començat.")

    def finalitzar(self):
        print(f"El joc '{self.nom}' ha acabat.")