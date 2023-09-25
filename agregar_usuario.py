import sqlite3
from flask_bcrypt import Bcrypt  # Importa la clase Bcrypt

bcrypt = Bcrypt()  # Crea una instancia de Bcrypt

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("sistema_musical.db")
cursor = conn.cursor()

# Definir los datos del usuario que deseas agregar
usuario = "javier_medio11"
contrasena = "24.Javier.98"  # Contraseña en texto plano
rol = "medio"  # Por ejemplo, "supremo", "medio", "basico"

# Hashea la contraseña antes de almacenarla
hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')

# Agrega el campo ID_Nucleo al registro de usuarios
id_nucleo = 11  # Asigna manualmente el ID_Nucleo que deseas para este usuario básico

# Insertar el nuevo usuario en la base de datos con la contraseña hasheada y el ID_Nucleo
cursor.execute("INSERT INTO Usuarios (Usuario, Contrasena, Rol, ID_Nucleo) VALUES (?, ?, ?, ?)",
               (usuario, hashed_password, rol, id_nucleo))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

