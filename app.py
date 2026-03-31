import json
import os

from flask import Flask, render_template, session

from models.score_storage import ScoreStorage
from routes.auth import auth_bp
from routes.game_routes import game_bp


app = Flask(__name__)
app.secret_key = 'clau_secreta_super_segura_per_educative_game'

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

score_storage = ScoreStorage(os.path.join(app.root_path, 'data', 'scores.json'))

# Ací definim els jocs que han d'aparéixer al rànquing.
RANKING_GAMES = [
    ('teclado', 'Keyboard Hero'),
    ('raton', 'Mouse Master'),
    ('drag_drop', 'Drag & Drop')
]


def load_rankings():
    # Llegim els usuaris registrats.
    results_path = os.path.join(app.root_path, 'data', 'results.json')
    users = []

    if os.path.exists(results_path):
        try:
            with open(results_path, 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (json.JSONDecodeError, OSError):
            users = []

    # Llegim les puntuacions guardades en el fitxer separat.
    scores_by_user = score_storage.get_scores_map()
    rankings = []

    # Creem una taula per a cada joc.
    for game_key, game_title in RANKING_GAMES:
        rows = []

        for user in users:
            username = user.get('username', 'Usuari')
            user_scores = scores_by_user.get(username, {})
            game_points = user_scores.get(game_key, 0)

            rows.append({
                'username': username,
                'points': game_points
            })

        # Ordenem de més punts a menys.
        rows.sort(key=lambda row: (-row['points'], row['username'].lower()))

        rankings.append({
            'key': game_key,
            'title': game_title,
            'rows': rows
        })

    return rankings


@app.route('/')
def index():
    current_user = session.get('username')
    return render_template('index.html', username=current_user)


@app.route('/joc-rato')
def joc_rato():
    return render_template('games/raton.html')


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', rankings=load_rankings())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
