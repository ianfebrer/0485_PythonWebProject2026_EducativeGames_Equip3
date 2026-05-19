from models.user import User
from extensions import db

class UserStorage:
    def __init__(self, file_path="data/results.json"):
        # Keep parameter for backward compatibility, but we don't need JSON anymore
        self.file_path = file_path

    def load_users(self):
        try:
            return User.query.all()
        except Exception as e:
            print(f"Error loading users from database: {e}")
            return []

    def get_user(self, username):
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error getting user '{username}' from database: {e}")
            return None

    def add_user(self, new_user):
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error adding user '{new_user.username}' to database: {e}")

    def update_user(self, updated_user):
        try:
            db.session.commit()
            return updated_user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating user '{updated_user.username}' in database: {e}")
