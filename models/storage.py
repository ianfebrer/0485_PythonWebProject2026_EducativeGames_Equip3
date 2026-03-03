import json
import os
from .user import User

class Storage:
    def __init__(self, file_path='data/results.json'):
        # Ruta del fitxer on es guarden les dades
        self.file_path = file_path

    def save_users(self, users_list):
        # Converteix la llista d'objectes User a una llista de diccionaris i la guarda al JSON
        data = [user.to_dict() for user in users_list]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def load_users(self):
        # Llegeix el fitxer JSON i torna una llista d'objectes de la classe User
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reconstruïm els objectes User a partir de les dades del diccionari
                return [User(u['username'], u['password'], u['total_score']) for u in data]
        except (json.JSONDecodeError, KeyError):
            return []