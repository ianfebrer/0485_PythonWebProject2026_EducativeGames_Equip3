from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, is_hashed=False):
        self.username = username
        
        if is_hashed:
            self.password = password
        else:
            self.password = generate_password_hash(password)

    def check_password(self, password_attempt):
        return check_password_hash(self.password, password_attempt)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password
        }

    def __str__(self):
        return f"User: {self.username} | Total Score: {self.total_score}"
