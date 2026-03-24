from flask import Flask, render_template, request, jsonify, session
from models.figures import ComplexShape
from models.game import DragAndDropGame
from models.storage import Storage

app = Flask(__name__)
app.secret_key = 'super_secret_key_educative_games'  # Necessari per usar session

# Storage initialization (using a dummy file or the default one)
storage = Storage('data/results.json')

@app.route('/')
def index():
    # Inicialitzem un usuari de prova a la sessió per poder desar punts
    if 'username' not in session:
        session['username'] = 'player1'
    return render_template('index.html')

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

if __name__ == '__main__':
    # El host 0.0.0.0 es necesario para que funcione en tu servidor Oracle
    app.run(debug=True, host='0.0.0.0', port=5000)