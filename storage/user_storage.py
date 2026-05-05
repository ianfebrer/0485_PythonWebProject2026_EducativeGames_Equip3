import json
import os

from models.user import User


class UserStorage:
    def __init__(self, file_path="data/results.json"):
        self.file_path = file_path

    def _ensure_file(self):
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def save_users(self, users_list):
        self._ensure_file()
        data = [user.to_dict() for user in users_list]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_users(self):
        self._ensure_file()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError, OSError):
            return []

        return [
            User(
                u["username"],
                u["password"],
                u.get("total_score", 0),
                is_hashed=True,
                anotacions=u.get("anotacions", ""),
                vist=u.get("vist", False),
            )
            for u in data
        ]

    def get_user(self, username):
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def add_user(self, new_user):
        users = self.load_users()
        if any(user.username == new_user.username for user in users):
            raise ValueError(f"Username '{new_user.username}' already exists")
        users.append(new_user)
        self.save_users(users)

    def update_user(self, updated_user):
        users = self.load_users()
        for index, user in enumerate(users):
            if user.username == updated_user.username:
                users[index] = updated_user
                self.save_users(users)
                return updated_user
        raise ValueError(f"User '{updated_user.username}' not found")
