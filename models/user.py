class User:
    def __init__(self, username, password, total_score=0):
        # Inicialització de l'usuari amb el seu nom, contrasenya i puntuació inicial
        self.username = username
        self.password = password
        self.total_score = total_score

    def add_score(self, points):
        # Mètode per sumar punts a la puntuació acumulada de l'usuari
        self.total_score += points

    def to_dict(self):
        # Converteix l'objecte en un diccionari per poder guardar-lo en format JSON
        return {
            "username": self.username,
            "password": self.password,
            "total_score": self.total_score
        }

    def __str__(self):
        # Representació en text de l'objecte usuari
        return f"User: {self.username} | Total Score: {self.total_score}"