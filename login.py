from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from flask_bcrypt import Bcrypt 

# Crea un Blueprint para el módulo de inicio de sesión
login_bp = Blueprint('login', __name__)

# Define la clase Usuario para la gestión de usuarios y roles
class Usuario(UserMixin):
    def __init__(self, id, usuario, rol, id_nucleo):
        self.id = id
        self.usuario = usuario
        self.rol = rol
        self.id_nucleo = id_nucleo



login_manager = LoginManager()

bcrypt = Bcrypt()


@login_manager.user_loader
def cargar_usuario(id):
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Usuario, usuario, rol, ID_Nucleo FROM usuarios WHERE ID_Usuario = ?", (id,))
    usuario_data = cursor.fetchone()
    conn.close()

    if usuario_data:
        return Usuario(id=usuario_data[0], usuario=usuario_data[1], rol=usuario_data[2], id_nucleo=usuario_data[3])
    return None


@login_bp.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        # Realiza la autenticación del usuario en la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Usuario, Usuario, Contrasena, Rol, ID_Nucleo FROM Usuarios WHERE Usuario = ?", (usuario,))
        usuario_data = cursor.fetchone()
        conn.close()

        if usuario_data and bcrypt.check_password_hash(usuario_data[2], contrasena):  # Compara las contraseñas
            usuario_obj = Usuario(id=usuario_data[0], usuario=usuario_data[1], rol=usuario_data[3], id_nucleo=usuario_data[4])
            login_user(usuario_obj)
            flash('Iniciaste sesión exitosamente', 'success')
            
            return redirect(url_for('login.inicio'))

        flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')


# Ruta para cerrar sesión
@login_bp.route('/logout')
@login_required
def cerrar_sesion():
    logout_user()
    flash('Cerraste sesión exitosamente', 'success')
    return redirect(url_for('login.iniciar_sesion'))

# Ruta para la página de inicio (requiere inicio de sesión)
@login_bp.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')

@login_bp.route('/politica_privacidad')
def politica_privacidad():
    return render_template('politica_privacidad.html')

