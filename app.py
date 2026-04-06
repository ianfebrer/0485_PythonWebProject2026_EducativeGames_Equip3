import json
import os
from flask import Flask, render_template, request, jsonify, session
from routes.auth import auth_bp
from routes.game_routes import game_bp
from models.score_storage import ScoreStorage
from models.figures import ComplexShape
from models.game import DragAndDropGame
from models.storage import Storage

app = Flask(__name__)
app.secret_key = 'clau_secreta_super_segura_per_educative_game'

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

score_storage = ScoreStorage(os.path.join(app.root_path, 'data', 'scores.json'))
storage = Storage('data/results.json')

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
@app.route('/game/drag-and-drop')
def drag_and_drop():
    # Instanciem les figures a través de la pròpia classe filla del joc (POO)
    shapes = DragAndDropGame.get_shapes()
    shapes_data = [shape.to_dict() for shape in shapes]
    return render_template('games/drag_drop.html', shapes=shapes_data)

@app.route('/api/validate_move', methods=['POST'])
def validate_move():
    data = request.json
    shape_name = data.get('shape_name')
    target_name = data.get('target_name')
    
    # Podem instanciar la figura i fer servir el seu mètode, tal com es demana (Object Methods)
    # Donat que només necessitem el nom per validar, els altres paràmetres poden ser dummy
    shape = ComplexShape("dummy_color", shape_name, 0)
    
    is_valid = shape.validate_drop(target_name)
    return jsonify({"valid": is_valid})

@app.route('/api/save_score', methods=['POST'])
def save_score():
    data = request.json
    points = data.get('score', 0)
    username = session.get('username', 'guest')
    
    # Deleguem tota la lògica d'orquestració de Resultats i Usuaris a l'objecte Storage (POO)
    new_total_score = storage.save_game_result(username, "Drag and Drop", "mouse drag", points)
    
    return jsonify({"success": True, "new_total_score": new_total_score})


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', rankings=load_rankings())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
