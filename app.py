from flask import Flask

<<<<<<< HEAD
from config import SECRET_KEY
=======
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from extensions import db

from models.figures import ComplexShape
from models.game import DragAndDropGame
from models.score_storage import ScoreStorage
>>>>>>> d1d1715 (Canvis per a migrar els usuaris a la BBDD i edició als arxius per a que funcionen totes les funcionalitats)
from routes.auth import auth_bp
from routes.game_routes import game_bp
from routes.main_routes import main_bp


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> f00198c (Resolts confictes al merge de app.py)
def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(main_bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
<<<<<<< HEAD
=======
=======
>>>>>>> f00198c (Resolts confictes al merge de app.py)
app = Flask(__name__)
app.secret_key = 'clau_secreta_super_segura_per_educative_game'

# MariaDB Configuration
DB_USER = "arnau"
DB_PASS = "035HFTkuQa2v3bLu"
DB_HOST = "158.179.217.136"
DB_PORT = "3307"
DB_NAME = "appdb"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

score_storage = ScoreStorage(os.path.join(app.root_path, 'data', 'scores.json'))

# Aquí definim els jocs que han d'aparèixer al rànquing.
RANKING_GAMES = [
    ('teclado', 'Keyboard Hero'),
    ('raton', 'Mouse Master'),
    ('drag_drop', 'Drag & Drop')
]


def load_rankings():
    # Ara llegim els usuaris de la base de dades MariaDB
    from models.user import User
    users = User.query.all()

    # Llegim les puntuacions guardades al fitxer separat (que encara es JSON per ara)
    scores_by_user = score_storage.get_scores_map()
    rankings = []

    # Creem una taula per a cada joc.
    for game_key, game_title in RANKING_GAMES:
        rows = []

        for user in users:
            username = user.username
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


@app.route('/')
def index():
    current_user = session.get('username')
    return render_template('index.html', username=current_user)


@app.route('/joc-rato')
def joc_rato():
    return render_template('games/raton.html')


@app.route('/game/drag-and-drop')
def drag_and_drop():
    # Carrego les figures del joc de drag & drop des del backend.
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


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    from models.storage import Storage
    storage = Storage()
    
    if 'username' not in session:
        return redirect(url_for('auth.login'))
        
    usuari = storage.get_user(session['username'])
    
    if request.method == 'POST':
        # Nota: Els camps anotacions i vist s'haurien de migrar a la BBDD 
        # si es volen seguir fent servir. Per ara, ja no es guarden en JSON.
        pass
        
    return render_template('perfil.html', usuari=usuari)


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', rankings=load_rankings())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> d1d1715 (Canvis per a migrar els usuaris a la BBDD i edició als arxius per a que funcionen totes les funcionalitats)
