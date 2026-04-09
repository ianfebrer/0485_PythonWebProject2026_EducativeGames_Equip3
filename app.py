import json
import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from models.figures import ComplexShape
from models.game import DragAndDropGame
from models.score_storage import ScoreStorage
from models.storage import Storage
from routes.auth import auth_bp
from routes.game_routes import game_bp


app = Flask(__name__)
app.secret_key = 'clau_secreta_super_segura_per_educative_game'

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

score_storage = ScoreStorage(os.path.join(app.root_path, 'data', 'scores.json'))
storage = Storage(os.path.join(app.root_path, 'data', 'results.json'))

# Aquí definim els jocs que han d'aparèixer al rànquing.
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

    # Llegim les puntuacions guardades al fitxer separat.
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

        rows.sort(key=lambda row: (-row['points'], row['username'].lower()))

        rankings.append({
            'key': game_key,
            'title': game_title,
            'rows': rows
        })

    return rankings


@app.route('/', methods=['GET', 'POST'])
def index():
    current_user = session.get('username')
    user = None

    if current_user:
        # busquem l'usuari que té la sessió iniciada
        users = storage.load_users()

        for u in users:
            if u.username == current_user:
                user = u
                break

        if request.method == 'POST' and user:
            # des de l'inici es poden modificar anotacions i vist
            user.set_anotacions(request.form.get('anotacions', ''))
            user.vist = request.form.get('vist') == 'on'
            storage.save_users(users)
            return redirect(url_for('index'))

    return render_template('index.html', username=current_user, user=user)


@app.route('/joc-rato')
def joc_rato():
    return render_template('games/raton.html')


@app.route('/game/drag-and-drop')
def drag_and_drop():
    # es carreguen les figures del joc de drag drop des del backend
    shapes = DragAndDropGame.get_shapes()
    shapes_data = [shape.to_dict() for shape in shapes]
    return render_template('games/drag_drop.html', shapes=shapes_data)


@app.route('/api/validate_move', methods=['POST'])
def validate_move():
    data = request.get_json() or {}
    shape_name = data.get('shape_name')
    target_name = data.get('target_name')

    # Creo la figura i faig servir el seu mètode per validar el forat.
    shape = ComplexShape("dummy_color", shape_name, 0)
    is_valid = shape.validate_drop(target_name)

    return jsonify({"valid": is_valid})


@app.route('/api/save_score', methods=['POST'])
def save_score():
    # Guardo la millor puntuació del drag & drop al mateix fitxer que la resta de jocs.
    data = request.get_json() or {}
    points = data.get('score', 0)

    try:
        points = int(points)
    except (TypeError, ValueError):
        points = 0

    if session.get('username'):
        username = session.get('username')
        millor_puntuacio = score_storage.update_user_score(username, 'drag_drop', points)

        return jsonify({
            "success": True,
            "guardat": True,
            "message": f"Has aconseguit {points} punts! Millor puntuacio guardada: {millor_puntuacio}."
        })

    return jsonify({
        "success": True,
        "guardat": False,
        "message": f"Has aconseguit {points} punts! Inicia sessio per guardar els teus resultats!"
    })


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', rankings=load_rankings())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
