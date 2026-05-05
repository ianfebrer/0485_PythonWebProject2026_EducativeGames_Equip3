from config import RANKING_GAMES, SCORES_FILE, USERS_FILE
from storage.score_storage import ScoreStorage
from storage.user_storage import UserStorage


class RankingService:
    def __init__(self, user_storage=None, score_storage=None):
        self.user_storage = user_storage or UserStorage(str(USERS_FILE))
        self.score_storage = score_storage or ScoreStorage(str(SCORES_FILE))

    def load_rankings(self):
        users = self.user_storage.load_users()
        scores_by_user = self.score_storage.get_scores_map()
        rankings = []

        for game_key, game_title in RANKING_GAMES:
            rows = []

            for user in users:
                rows.append(
                    {
                        "username": user.username,
                        "points": scores_by_user.get(user.username, {}).get(game_key, 0),
                    }
                )

            rows.sort(key=lambda row: (-row["points"], row["username"].lower()))
            rankings.append({"key": game_key, "title": game_title, "rows": rows})

        return rankings
