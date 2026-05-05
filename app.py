from flask import Flask

from config import SECRET_KEY
from routes.auth import auth_bp
from routes.game_routes import game_bp
from routes.main_routes import main_bp


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
