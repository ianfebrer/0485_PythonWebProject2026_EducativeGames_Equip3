import json
import os


class ScoreStorage:
    def __init__(self, file_path='data/scores.json'):
        self.file_path = file_path
        self.default_scores = {
            'teclado': 0,
            'raton': 0,
            'drag_drop': 0
        }

    def _ensure_file(self):
        folder = os.path.dirname(self.file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)

    def load_scores(self):
        self._ensure_file()

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            data = []

        clean_data = []

        for item in data:
            username = item.get('username', 'Usuari')
            saved_scores = item.get('scores', {})

            scores = {
                'teclado': 0,
                'raton': 0,
                'drag_drop': 0
            }

            for game_key in scores:
                if game_key in saved_scores:
                    scores[game_key] = saved_scores[game_key]

            clean_data.append({
                'username': username,
                'scores': scores
            })

        return clean_data

    def save_scores(self, scores_list):
        self._ensure_file()

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(scores_list, file, indent=4)

    def get_scores_map(self):
        scores_map = {}

        for item in self.load_scores():
            scores_map[item['username']] = item['scores']

        return scores_map

    def update_user_score(self, username, game_key, points):
        scores_list = self.load_scores()

        for item in scores_list:
            if item['username'] == username:
                current_best = item['scores'].get(game_key, 0)

                if points > current_best:
                    item['scores'][game_key] = points
                    self.save_scores(scores_list)
                    return points

                return current_best

        new_entry = {
            'username': username,
            'scores': {
                'teclado': 0,
                'raton': 0,
                'drag_drop': 0
            }
        }
        new_entry['scores'][game_key] = points

        scores_list.append(new_entry)
        self.save_scores(scores_list)
        return points
