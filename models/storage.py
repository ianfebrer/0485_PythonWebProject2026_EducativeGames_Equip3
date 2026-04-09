import json
import os
from .user import User

class Storage:
    def __init__(self, file_path='data/results.json'):
        self.file_path = file_path

    def save_users(self, users_list):
        data = [user.to_dict() for user in users_list]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # Modifiquem load_users per llegir els nous camps
    def load_users(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [User(
                    u['username'], 
                    u['password'], 
                    u.get('total_score', 0), 
                    is_hashed=True,
                    anotacions=u.get('anotacions', ""),
                    vist=u.get('vist', False)           
                ) for u in data]
        except (json.JSONDecodeError, KeyError):
            return []

    def save_game_result(self, username, game_name, game_type, points):
        from .user import User
        from .game import Game
        from .result import Result
        
        users = self.load_users()
        current_user = next((u for u in users if u.username == username), None)
        if not current_user:
            current_user = User(username, "password123")
            users.append(current_user)
            
        game_instance = Game(game_name, game_type)
        result = Result(current_user, game_instance, points)
        result.save()
        
        self.save_users(users)
        return current_user.total_score
    # --- NOUS MÈTODES PER FACILITAR EL LOGIN/REGISTRE ---
    def get_user(self, username):
        # Busca i retorna un usuari pel seu nom, o None si no existeix
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def add_user(self, new_user):
        # Afegeix un nou usuari a la llista i guarda el fitxer
        users = self.load_users()
        users.append(new_user)
        self.save_users(users)