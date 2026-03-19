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

    def load_users(self):
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # CRÍTIC: Afegim is_hashed=True perquè no torni a encriptar les claus del JSON
                return [User(u['username'], u['password'], u.get('total_score', 0), is_hashed=True) for u in data]
        except (json.JSONDecodeError, KeyError):
            return []

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