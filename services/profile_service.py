from config import USERS_FILE
from storage.user_storage import UserStorage


class ProfileService:
    def __init__(self, user_storage=None):
        self.user_storage = user_storage or UserStorage(str(USERS_FILE))

    def get_user(self, username):
        return self.user_storage.get_user(username)

    def update_profile(self, username, anotacions, vist):
        user = self.user_storage.get_user(username)
        if not user:
            raise ValueError(f"User '{username}' not found")

        user.set_anotacions(anotacions)
        user.vist = vist
        self.user_storage.update_user(user)
        return user
