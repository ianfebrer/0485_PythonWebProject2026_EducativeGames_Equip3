import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "results.json"

SECRET_KEY = os.getenv("SECRET_KEY", "clau_secreta_super_segura_per_educative_game")

RANKING_GAMES = [
    ("teclado", "Keyboard Hero"),
    ("raton", "Mouse Master"),
    ("drag_drop", "Drag & Drop"),
]
