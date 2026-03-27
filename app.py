from flask import Flask, render_template, request, jsonify, session
from routes.auth import auth_bp # Importem les rutes que vam crear
from models.figures import ComplexShape
from models.game import DragAndDropGame
from models.storage import Storage

app = Flask(__name__)

# 1. CLAU SECRETA (CRÍTIC)
# Obligatòria per fer servir 'session' i 'flash'. Sense això, Flask donarà error.
# En un entorn real, això ha de ser una cadena de text aleatòria i complexa.
app.secret_key = 'clau_secreta_super_segura_per_educative_game' 

# 2. REGISTRE DEL BLUEPRINT
# Això li diu a Flask: "Escolta, tinc més rutes guardades en aquest altre fitxer, incorpora-les!"
app.register_blueprint(auth_bp)

# Storage initialization (using a dummy file or the default one)
storage = Storage('data/results.json')

@app.route('/')
def index():
    # Agafem el nom d'usuari de la sessió (si no ha iniciat sessió, serà None)
    current_user = session.get('username')
    
    # Passem l'usuari al teu index.html perquè puguis comprovar si el login ha funcionat
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

if __name__ == '__main__':
    # El host 0.0.0.0 es necesario para que funcione en tu servidor Oracle
    app.run(debug=True, host='0.0.0.0', port=5000)