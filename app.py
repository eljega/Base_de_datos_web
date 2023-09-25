from flask import Flask, redirect, url_for
from maestros import maestros_bp  # Importa el Blueprint de maestros
from alumnos import alumnos_bp  # Importa el Blueprint de alumnos
from nucleos import nucleos_bp  # Importa el Blueprint de nucleos
from instrumentos import instrumentos_bp  # Importa el Blueprint de los instrumentos
from login import login_bp  # Importa el Blueprint de inicio de sesión (login.py)
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import sqlite3, datetime
from flask_login import current_user

app = Flask(__name__, static_url_path='/static')
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
# Configuración para servir archivos estáticos desde la carpeta "imagenes"

app.secret_key = '123'  # Reemplaza 'tu_clave_secreta_aqui' con una clave secreta real y segura

# Registra la función user_loader
from login import cargar_usuario  # Asegúrate de que esta importación sea correcta

login_manager.user_loader(cargar_usuario)

# Registra los Blueprints de maestros, alumnos, nucleos, instrumentos y login
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(nucleos_bp)
app.register_blueprint(instrumentos_bp)
app.register_blueprint(login_bp)  # Registra el Blueprint de inicio de sesión

def registrar_auditoria(usuario, accion, detalles):
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    fecha_hora = datetime.now()
    cursor.execute("INSERT INTO Auditoria (Fecha_Hora, Usuario, Accion, Detalles) VALUES (?, ?, ?, ?)",
                   (fecha_hora, usuario, accion, detalles))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Verifica si el usuario está autenticado
    if current_user.is_authenticated:
        # Si está autenticado, redirige al usuario a la ruta '/inicio'
        return redirect(url_for('login.inicio'))
    else:
        # Si no está autenticado, redirige al usuario a la ruta '/login'
        return redirect(url_for('login.iniciar_sesion'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

