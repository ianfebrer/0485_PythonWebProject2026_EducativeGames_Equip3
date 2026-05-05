from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from games.drag_drop_game import DragAndDropGame
from services.profile_service import ProfileService
from services.ranking_service import RankingService
from services.score_service import ScoreService


main_bp = Blueprint("main", __name__)
profile_service = ProfileService()
ranking_service = RankingService()
score_service = ScoreService()


@main_bp.route("/")
def index():
    return render_template("index.html", username=session.get("username"))


@main_bp.route("/joc-rato")
def joc_rato():
    return render_template("games/raton.html")


@main_bp.route("/game/drag-and-drop")
def drag_and_drop():
    shapes_data = [shape.to_dict() for shape in DragAndDropGame.get_shapes()]
    return render_template("games/drag_drop.html", shapes=shapes_data)


@main_bp.route("/api/validate_move", methods=["POST"])
def validate_move():
    data = request.get_json() or {}
    shape_name = data.get("shape_name", "")
    target_name = data.get("target_name", "")

    return jsonify({"valid": DragAndDropGame.validate_shape_drop(shape_name, target_name)})


@main_bp.route("/api/save_score", methods=["POST"])
def save_score():
    data = request.get_json() or {}

    try:
        points = int(data.get("score", 0))
    except (TypeError, ValueError):
        points = 0

    response = score_service.build_score_response(
        username=session.get("username"),
        game_key="drag_drop",
        points=points,
        login_message="Inicia sessio per guardar els teus resultats!",
    )

    return jsonify(
        {
            "success": True,
            "guardat": response["guardat"],
            "message": response["message"],
        }
    )


@main_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        profile_service.update_profile(
            username=username,
            anotacions=request.form.get("anotacions", ""),
            vist=bool(request.form.get("vist")),
        )

    usuari = profile_service.get_user(username)
    return render_template("perfil.html", usuari=usuari)


@main_bp.route("/ranking")
def ranking():
    return render_template("ranking.html", rankings=ranking_service.load_rankings())
