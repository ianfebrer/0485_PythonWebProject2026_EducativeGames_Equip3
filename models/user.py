from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, total_score=0, is_hashed=False):
        # Inicialització de l'usuari amb el seu nom i puntuació inicial
        self.username = username
        self.total_score = total_score
        
        # Si la contrasenya ja ve encriptada (per exemple, quan la llegim del JSON)
        if is_hashed:
            self.password = password
        else:
            # Si és un usuari nou, encriptem la contrasenya abans de guardar-la
            self.password = generate_password_hash(password)

    def check_password(self, password_attempt):
        # Comprova si la contrasenya introduïda coincideix amb el hash guardat
        return check_password_hash(self.password, password_attempt)

    def add_score(self, points):
        self.total_score += points

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password, # Ara es guardarà en format encriptat
            "total_score": self.total_score
        }

    def __str__(self):
        return f"User: {self.username} | Total Score: {self.total_score}"