import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("sistema_musical.db")

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear la tabla de Nucleos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Nucleos (
        ID_Nucleo INTEGER PRIMARY KEY,
        Nombre_Nucleo TEXT,
        Codigo TEXT,
        Fecha_Apertura TEXT,
        Direccion TEXT,
        Telefono TEXT,
        Estatus_Inmueble TEXT CHECK (Estatus_Inmueble IN ('Comodato', 'Alquilado', 'Prestado', 'Propio')),
        Infraestructura TEXT,
        -- Agregar más campos si es necesario
        UNIQUE (Codigo) -- Asegura que el código sea único
    )
''')


# Crear la tabla de Alumnos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alumnos (
        ID_Alumno INTEGER PRIMARY KEY,
        Nombre_Alumno TEXT,
        Apellido_alumno TEXT,
        Edad INTEGER,
        Fecha_Nacimiento TEXT,
        Numero_Documento TEXT,
        Descripcion TEXT,
        Catedra TEXT,
        ID_Nucleo INTEGER,
        FOREIGN KEY (ID_Nucleo) REFERENCES Nucleos (ID_Nucleo)
    )
''')

# Crear la tabla de Maestros con el campo "Estatus"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Maestros (
        ID_Maestro INTEGER PRIMARY KEY,
        Nombre_Maestro TEXT,
        Apellido_Maestro TEXT,
        Edad INTEGER,
        Fecha_Nacimiento TEXT,
        Numero_Documento TEXT,
        Descripcion TEXT,
        Cargo TEXT,
        Funcion TEXT,
        Nivel_Educativo TEXT,
        Fecha_Ingreso TEXT,
        ID_Nucleo INTEGER,
        Estatus TEXT CHECK (Estatus IN ('Activo', 'Inactivo')),  -- Campo de estatus
        FOREIGN KEY (ID_Nucleo) REFERENCES Nucleos (ID_Nucleo)
    )
''')


# Crear la tabla de Instrumentos con los datos adicionales
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Instrumentos (
        ID_Instrumento INTEGER PRIMARY KEY,
        Item INTEGER,
        Marca TEXT,
        Cantidad INTEGER,
        Modelo TEXT,
        Medida TEXT,
        Color TEXT CHECK (Color IN ('amarillo', 'azul', 'marron', 'gris', 'negro', 'blanco')),
        Numero_Serial TEXT,
        Numero_Inventario TEXT,
        Accesorio TEXT,
        Condicion TEXT,
        Ubicacion TEXT,
        Procedencia TEXT,
        Comodato_Vigente TEXT,
        Descripcion TEXT,
        ID_Nucleo INTEGER
    )
''')


# Crear la tabla de Usuarios con campos: usuario, contraseña y rol
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        ID_Usuario INTEGER PRIMARY KEY,
        Usuario TEXT UNIQUE NOT NULL,
        Contrasena TEXT NOT NULL,
        Rol TEXT NOT NULL,
        ID_Nucleo TEXT
    )
''')

# Crear la tabla de auditoria para el registro
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Auditoria (
        ID_Auditoria INTEGER PRIMARY KEY,
        Fecha_Hora TIMESTAMP,
        Usuario TEXT,
        Accion TEXT,
        Detalles TEXT
    )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
