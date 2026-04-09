from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, total_score=0, is_hashed=False, anotacions="", vist=False):
        # Inicialització de l'usuari amb el seu nom i puntuació inicial
        self.username = username
        self.total_score = total_score
        
        # 🟢 NOU: Atribut privat (exigit a l'examen per demostrar encapsulació)
        self.__anotacions = anotacions
        # 🟢 NOU: Atribut públic
        self.vist = vist
        
        # Si la contrasenya ja ve encriptada (per exemple, quan la llegim del JSON)
        if is_hashed:
            self.password = password
        else:
            # Si és un usuari nou, encriptem la contrasenya abans de guardar-la
            self.password = generate_password_hash(password)

    # 🟢 NOU: Getter per a l'atribut privat
    def get_anotacions(self):
        return self.__anotacions

    # 🟢 NOU: Setter per a l'atribut privat
    def set_anotacions(self, text):
        self.__anotacions = text

    def check_password(self, password_attempt):
        # Comprova si la contrasenya introduïda coincideix amb el hash guardat
        return check_password_hash(self.password, password_attempt)

    def add_score(self, points):
        self.total_score += points

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password, # Ara es guardarà en format encriptat
            "total_score": self.total_score,
            "anotacions": self.__anotacions, # 🟢 NOU: Guardem el valor privat al JSON
            "vist": self.vist                # 🟢 NOU: Guardem el valor públic al JSON
        }

    def __str__(self):
        return f"User: {self.username} | Total Score: {self.total_score} | Vist: {self.vist}"