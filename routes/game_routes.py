import os

from flask import Blueprint, jsonify, request, render_template, session

from games.mouse_move_game import MouseMoveGame
from models.keyboard_game import KeyboardGame
from models.score_storage import ScoreStorage


game_bp = Blueprint('game', __name__)
mecanografia_game = KeyboardGame()
mouse_move_game = MouseMoveGame()
score_storage = ScoreStorage(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'scores.json')
)


@game_bp.route('/mecanografia')
def play_mecanografia():
    return render_template('games/teclado.html')


@game_bp.route('/api/get-frase', methods=['GET'])
def api_get_frase():
    frase = mecanografia_game.obtenir_frase()
    return jsonify({'frase': frase})


@game_bp.route('/api/mouse-objectiu', methods=['GET'])
def api_mouse_objectiu():
    # Aquí envio al frontend quina figura toca buscar en la ronda.
    objectiu = mouse_move_game.obtenir_objectiu()
    return jsonify({'objectiu': objectiu})


@game_bp.route('/api/mouse-validar', methods=['POST'])
def api_mouse_validar():
    # Aquí valido des del backend si la figura triada és correcta o no.
    dades = request.get_json() or {}
    figura_objectiu = dades.get('objectiu', '')
    figura_seleccionada = dades.get('seleccionada', '')

    es_correcte = mouse_move_game.validar_resposta(figura_objectiu, figura_seleccionada)
    punts = mouse_move_game.calcular_punts(es_correcte)

    return jsonify({
        'correcte': es_correcte,
        'punts': punts
    })


@game_bp.route('/api/guardar-resultat', methods=['POST'])
def api_guardar_resultat():
    # Guarda la millor puntuació del joc de teclado.
    dades = request.get_json() or {}
    correctes = dades.get('correctes', 0)
    incorrectes = dades.get('incorrectes', 0)

    punts_finals = mecanografia_game.calcular_puntuacio(correctes, incorrectes)
    missatge = f'Has aconseguit {punts_finals} punts!'

    if session.get('username'):
        username = session.get('username')
        millor_puntuacio = score_storage.update_user_score(username, 'teclado', punts_finals)
        guardat = True
        missatge += f' Millor puntuacio guardada: {millor_puntuacio}.'
    else:
        guardat = False
        missatge += ' Inicia sessió per guardar els teus resultats!'

    return jsonify({
        'punts': punts_finals,
        'guardat': guardat,
        'missatge': missatge
    })


@game_bp.route('/api/guardar-resultat-rato', methods=['POST'])
def api_guardar_resultat_rato():
    # Guarda la millor puntuació del joc del ratolí.
    dades = request.get_json() or {}
    punts = dades.get('punts', 0)

    try:
        punts = int(punts)
    except (TypeError, ValueError):
        punts = 0

    missatge = f'Has aconseguit {punts} punts!'

    if session.get('username'):
        username = session.get('username')
        millor_puntuacio = score_storage.update_user_score(username, 'raton', punts)
        guardat = True
        missatge += f' Millor puntuacio guardada: {millor_puntuacio}.'
    else:
        guardat = False
        missatge += ' Inicia sessio per guardar els teus resultats!'

    return jsonify({
        'punts': punts,
        'guardat': guardat,
        'missatge': missatge
    })
