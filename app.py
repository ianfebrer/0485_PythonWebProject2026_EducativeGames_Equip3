from flask import Flask, render_template, session
from routes.auth import auth_bp # Importem les rutes d'autenticació que vam crear
from routes.game_routes import game_bp # <-- NOVA LÍNIA: Importem les rutes del joc

app = Flask(__name__)

# 1. CLAU SECRETA (CRÍTIC)
# Obligatòria per fer servir 'session' i 'flash'. Sense això, Flask donarà error.
# En un entorn real, això ha de ser una cadena de text aleatòria i complexa.
app.secret_key = 'clau_secreta_super_segura_per_educative_game' 

# 2. REGISTRE DELS BLUEPRINTS
# Això li diu a Flask: "Escolta, tinc més rutes guardades en aquests altres fitxers, incorpora-les!"
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp) # <-- NOVA LÍNIA: Connectem el joc a l'aplicació principal

@app.route('/')
def index():
    # Agafem el nom d'usuari de la sessió (si no ha iniciat sessió, serà None)
    current_user = session.get('username')
    
    # Passem l'usuari al teu index.html perquè puguis comprovar si el login ha funcionat
    return render_template('index.html', username=current_user)

@app.route('/joc-rato')
def joc_rato():
    return render_template('games/raton.html')

if __name__ == '__main__':
    # El host 0.0.0.0 es necessari perquè funcioni en el teu servidor Oracle
    app.run(debug=True, host='0.0.0.0', port=5000)