import json
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class ScoreStorage:
    def __init__(self, file_path="data/scores.json"):
        self.file_path = file_path
        self.default_scores = {
            "teclado": 0,
            "raton": 0,
            "drag_drop": 0,
        }
        self._load_dotenv_file()
        self.db_config = self._load_db_config()
        self.database_enabled = self._is_database_configured()
        self.collection = None

        if self.database_enabled:
            self.collection = self._get_collection()
            self._initialize_database()
            self._migrate_legacy_scores_if_needed()

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

    def _is_database_configured(self):
        uri = self.db_config["uri"]
        if not uri:
            return False

        if "<db_username>" in uri or "<db_password>" in uri:
            return False

        return True

    def _get_collection(self):
        client = MongoClient(self.db_config["uri"], serverSelectionTimeoutMS=10000)
        database = client[self.db_config["database"]]
        return database[self.db_config["collection"]]

    def _initialize_database(self):
        try:
            self.collection.create_index("username", unique=True)
        except PyMongoError:
            self.collection = None
            self.database_enabled = False

    def _migrate_legacy_scores_if_needed(self):
        if not self.database_enabled or not os.path.exists(self.file_path):
            return

        if self.collection.count_documents({}) > 0:
            return

        for entry in self._load_legacy_scores():
            self.collection.update_one(
                {"username": entry["username"]},
                {"$set": {"scores": entry["scores"]}},
                upsert=True,
            )

    def _ensure_file(self):
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    def _load_legacy_scores(self):
        self._ensure_file()

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            data = []

        clean_data = []

        for item in data:
            username = item.get("username", "Usuari")
            saved_scores = item.get("scores", {})
            scores = dict(self.default_scores)

            for game_key in scores:
                if game_key in saved_scores:
                    try:
                        scores[game_key] = int(saved_scores[game_key])
                    except (TypeError, ValueError):
                        scores[game_key] = 0

            clean_data.append({"username": username, "scores": scores})

        return clean_data

    def _save_legacy_scores(self, scores_list):
        self._ensure_file()

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(scores_list, file, indent=4)

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
        if not self.database_enabled:
            return self._load_legacy_scores()

        scores_map = self.get_scores_map()
        return [{"username": username, "scores": scores} for username, scores in scores_map.items()]

    def get_scores_map(self):
        if not self.database_enabled:
            scores_map = {}

            for item in self._load_legacy_scores():
                scores_map[item["username"]] = item["scores"]

            return scores_map

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

        if not self.database_enabled:
            scores_list = self._load_legacy_scores()

            for item in scores_list:
                if item["username"] == username:
                    current_best = item["scores"].get(game_key, 0)

                    if points > current_best:
                        item["scores"][game_key] = points
                        self._save_legacy_scores(scores_list)
                        return points

                    return current_best

            new_entry = {"username": username, "scores": dict(self.default_scores)}
            new_entry["scores"][game_key] = points
            scores_list.append(new_entry)
            self._save_legacy_scores(scores_list)
            return points

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
