from config import SCORES_FILE
from storage.score_storage import ScoreStorage


class ScoreService:
    def __init__(self, score_storage=None):
        self.score_storage = score_storage or ScoreStorage(str(SCORES_FILE))

    def save_best_score(self, username, game_key, points):
        return self.score_storage.update_user_score(username, game_key, points)

    def build_score_response(self, username, game_key, points, login_message):
        if username:
            best_score = self.save_best_score(username, game_key, points)
            return {
                "guardat": True,
                "message": f"Has aconseguit {points} punts! Millor puntuacio guardada: {best_score}.",
                "best_score": best_score,
            }

        return {
            "guardat": False,
            "message": f"Has aconseguit {points} punts! {login_message}",
            "best_score": None,
        }
