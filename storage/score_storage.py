import os

from pymongo import MongoClient


class ScoreStorage:
    def __init__(self, file_path=None):
        self.default_scores = {
            "teclado": 0,
            "raton": 0,
            "drag_drop": 0,
        }
        self._load_dotenv_file()
        self.db_config = self._load_db_config()
        self.collection = self._get_collection()
        self._initialize_database()

    def _load_dotenv_file(self):
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if not os.path.exists(env_path):
            return

        try:
            with open(env_path, "r", encoding="utf-8") as env_file:
                for raw_line in env_file:
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            return

    def _load_db_config(self):
        return {
            "uri": os.getenv("MONGODB_URI", "").strip(),
            "database": os.getenv("MONGODB_DB_NAME", "educative_games").strip(),
            "collection": os.getenv("MONGODB_COLLECTION", "game_scores").strip(),
        }

    def _get_collection(self):
        uri = self.db_config["uri"]
        if not uri or "<db_username>" in uri or "<db_password>" in uri:
            raise RuntimeError("MONGODB_URI no esta configurado correctamente para el ranking.")

        client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        database = client[self.db_config["database"]]
        return database[self.db_config["collection"]]

    def _initialize_database(self):
        self.collection.create_index("username", unique=True)

    def _normalize_scores(self, saved_scores):
        scores = dict(self.default_scores)

        if not isinstance(saved_scores, dict):
            return scores

        for game_key in scores:
            try:
                scores[game_key] = int(saved_scores.get(game_key, 0))
            except (TypeError, ValueError):
                scores[game_key] = 0

        return scores

    def load_scores(self):
        scores_map = self.get_scores_map()
        return [{"username": username, "scores": scores} for username, scores in scores_map.items()]

    def get_scores_map(self):
        scores_map = {}

        for item in self.collection.find({}, {"_id": 0, "username": 1, "scores": 1}):
            username = item.get("username")
            if not username:
                continue

            scores_map[username] = self._normalize_scores(item.get("scores", {}))

        return scores_map

    def update_user_score(self, username, game_key, points):
        if game_key not in self.default_scores:
            raise ValueError(f"Unknown game key: {game_key}")

        try:
            points = int(points)
        except (TypeError, ValueError):
            points = 0

        current_item = self.collection.find_one({"username": username}, {"_id": 0, "scores": 1})
        current_scores = self._normalize_scores(current_item.get("scores", {}) if current_item else {})
        current_best = current_scores.get(game_key, 0)

        if points > current_best:
            current_scores[game_key] = points
            self.collection.update_one(
                {"username": username},
                {"$set": {"scores": current_scores}},
                upsert=True,
            )
            return points

        if current_item:
            return current_best

        self.collection.update_one(
            {"username": username},
            {"$set": {"scores": current_scores}},
            upsert=True,
        )
        return current_best
