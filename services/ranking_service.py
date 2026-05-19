from config import RANKING_GAMES
from storage.score_storage import ScoreStorage


class RankingService:
    def __init__(self, score_storage=None):
        self.score_storage = score_storage or ScoreStorage()

    def load_rankings(self):
        scores_by_user = self.score_storage.get_scores_map()
        rankings = []

        for game_key, game_title in RANKING_GAMES:
            rows = []

            for username, user_scores in scores_by_user.items():
                rows.append(
                    {
                        "username": username,
                        "points": user_scores.get(game_key, 0),
                    }
                )

            rows.sort(key=lambda row: (-row["points"], row["username"].lower()))
            rankings.append({"key": game_key, "title": game_title, "rows": rows})

        return rankings
