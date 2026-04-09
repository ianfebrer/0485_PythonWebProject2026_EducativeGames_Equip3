from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, total_score=0, is_hashed=False, anotacions="", vist=False):
        self.username = username
        self.total_score = total_score
        
        self.__anotacions = anotacions
        self.vist = vist
        
        if is_hashed:
            self.password = password
        else:
            self.password = generate_password_hash(password)

    def check_password(self, password_attempt):
        return check_password_hash(self.password, password_attempt)

    def add_score(self, points):
        self.total_score += points

    def get_anotacions(self):
        return self.__anotacions

    def set_anotacions(self, text):
        self.__anotacions = text

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "total_score": self.total_score,
            "anotacions": self.get_anotacions(),
            "vist": self.vist
        }

    def __str__(self):
        return f"User: {self.username} | Total Score: {self.total_score}"

class Alumne(User):
    def __init__(self, username, password, total_score=0, is_hashed=False, anotacions="", vist=False):
        super().__init__(username, password, total_score, is_hashed, anotacions, vist)

class Professor(User):
    def __init__(self, username, password, total_score=0, is_hashed=False, anotacions="", vist=False):
        super().__init__(username, password, total_score, is_hashed, anotacions, vist)