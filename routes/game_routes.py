from flask import Blueprint, jsonify, render_template, request, session

from games.keyboard_game import KeyboardGame
from games.mouse_move_game import MouseMoveGame
from services.score_service import ScoreService


game_bp = Blueprint("game", __name__)
mecanografia_game = KeyboardGame()
mouse_move_game = MouseMoveGame()
score_service = ScoreService()


@game_bp.route("/mecanografia")
def play_mecanografia():
    return render_template("games/teclado.html")


@game_bp.route("/api/get-frase", methods=["GET"])
def api_get_frase():
    frase = mecanografia_game.obtenir_frase()
    return jsonify({"frase": frase})


@game_bp.route("/api/mouse-objectiu", methods=["GET"])
def api_mouse_objectiu():
    objectiu = mouse_move_game.obtenir_objectiu()
    return jsonify({"objectiu": objectiu})


@game_bp.route("/api/mouse-validar", methods=["POST"])
def api_mouse_validar():
    dades = request.get_json() or {}
    figura_objectiu = dades.get("objectiu", "")
    figura_seleccionada = dades.get("seleccionada", "")

    es_correcte = mouse_move_game.validar_resposta(figura_objectiu, figura_seleccionada)
    punts = mouse_move_game.calcular_punts(es_correcte)

    return jsonify({"correcte": es_correcte, "punts": punts})


@game_bp.route("/api/guardar-resultat", methods=["POST"])
def api_guardar_resultat():
    dades = request.get_json() or {}

    try:
        correctes = int(dades.get("correctes", 0))
        incorrectes = int(dades.get("incorrectes", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Dades no valides"}), 400

    punts_finals = mecanografia_game.calcular_puntuacio(correctes, incorrectes)
    response = score_service.build_score_response(
        username=session.get("username"),
        game_key="teclado",
        points=punts_finals,
        login_message="Inicia sessio per guardar els teus resultats!",
    )

    return jsonify(
        {
            "punts": punts_finals,
            "guardat": response["guardat"],
            "missatge": response["message"],
        }
    )


@game_bp.route("/api/guardar-resultat-rato", methods=["POST"])
def api_guardar_resultat_rato():
    dades = request.get_json() or {}
    punts = dades.get("punts", 0)

    try:
        punts = int(punts)
    except (TypeError, ValueError):
        punts = 0

    response = score_service.build_score_response(
        username=session.get("username"),
        game_key="raton",
        points=punts,
        login_message="Inicia sessio per guardar els teus resultats!",
    )

    return jsonify(
        {
            "punts": punts,
            "guardat": response["guardat"],
            "missatge": response["message"],
        }
    )
