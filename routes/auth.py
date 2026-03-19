from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from models.storage import Storage

# Creem el Blueprint i instanciem la teva classe Storage
auth_bp = Blueprint('auth', __name__)
storage = Storage() 

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Utilitzem el teu Storage per comprovar si ja existeix
        if storage.get_user(username):
            flash('Aquest nom d\'usuari ja existeix.')
            return redirect(url_for('auth.register'))
        
        # Creem el nou usuari (es fa el hash automàtic)
        new_user = User(username=username, password=password)
        # Utilitzem el teu Storage per afegir-lo
        storage.add_user(new_user)
        
        flash('Registre completat amb èxit! Ara pots iniciar sessió.')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Traiem l'objecte User directament del teu Storage
        user = storage.get_user(username)
        
        # Com user ja és de classe User, directament usem el check_password
        if user and user.check_password(password):
            session['username'] = user.username # Guardem la sessió
            return redirect(url_for('index')) # Redirigim a la principal (assegura't que es diu 'index' a app.py)
            
        flash('Usuari o contrasenya incorrectes.')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))