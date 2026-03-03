class Result:
    def __init__(self, user, game, points):
        # Registra un resultat vinculant un usuari, un joc i els punts obtinguts
        self.user = user
        self.game = game
        self.points = points

    def save(self):
        # Actualitza la puntuació total de l'usuari directament des del resultat
        self.user.add_score(self.points)

    def __str__(self):
        # Descripció del resultat obtingut
        return f"{self.user.username} scored {self.points} in {self.game.name}"