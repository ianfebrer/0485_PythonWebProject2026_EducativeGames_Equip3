from flask import Flask, render_template, session
from routes.auth import auth_bp # Importem les rutes que vam crear

app = Flask(__name__)

# 1. CLAU SECRETA (CRÍTIC)
# Obligatòria per fer servir 'session' i 'flash'. Sense això, Flask donarà error.
# En un entorn real, això ha de ser una cadena de text aleatòria i complexa.
app.secret_key = 'clau_secreta_super_segura_per_educative_game' 

# 2. REGISTRE DEL BLUEPRINT
# Això li diu a Flask: "Escolta, tinc més rutes guardades en aquest altre fitxer, incorpora-les!"
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    # Agafem el nom d'usuari de la sessió (si no ha iniciat sessió, serà None)
    current_user = session.get('username')
    
    # Passem l'usuari al teu index.html perquè puguis comprovar si el login ha funcionat
    return render_template('index.html', username=current_user)

if __name__ == '__main__':
    # El host 0.0.0.0 es necesario para que funcione en tu servidor Oracle
    app.run(debug=True, host='0.0.0.0', port=5000)