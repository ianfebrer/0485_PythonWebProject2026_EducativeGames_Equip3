from flask import Blueprint, jsonify, request, render_template, session
from models.keyboard_game import KeyboardGame

game_bp = Blueprint('game', __name__)
mecanografia_game = KeyboardGame()

@game_bp.route('/mecanografia')
def play_mecanografia():
    return render_template('games/teclado.html') # A la captura he vist que el teu HTML es diu teclado.html!

@game_bp.route('/api/get-frase', methods=['GET'])
def api_get_frase():
    frase = mecanografia_game.obtenir_frase()
    return jsonify({"frase": frase})

@game_bp.route('/api/guardar-resultat', methods=['POST'])
def api_guardar_resultat():
    dades = request.get_json()
    correctes = dades.get('correctes', 0)
    incorrectes = dades.get('incorrectes', 0)
    
    punts_finals = mecanografia_game.calcular_puntuacio(correctes, incorrectes)
    missatge = f"Has aconseguit {punts_finals} punts!"

    if session.get('username'):
        guardat = True
        missatge += " Puntuació guardada al teu historial."
    else:
        guardat = False
        missatge += " Inicia sessió per guardar els teus resultats!"

    return jsonify({"punts": punts_finals, "guardat": guardat, "missatge": missatge})