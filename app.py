from flask import Flask
from extensions import db
from config import SECRET_KEY
from routes.auth import auth_bp
from routes.game_routes import game_bp
from routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

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
    app.register_blueprint(main_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
