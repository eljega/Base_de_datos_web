from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import sqlite3
from flask_login import login_manager  # Importa login_manager
from flask_login import LoginManager
from flask_login import current_user, login_required


maestros_bp = Blueprint('maestros', __name__)
login_manager = LoginManager()

@maestros_bp.route('/personal', methods=['GET'])
@login_required
def lista_maestros():
    # Obtener la cadena de búsqueda del formulario
    busqueda = request.args.get('busqueda', '')

    # Obtener el parámetro mostrar_todos de la solicitud GET
    mostrar_todos = request.args.get('mostrar_todos')

    # Dividir la cadena de búsqueda en palabras clave
    palabras_clave = busqueda.split()

    # Consultar la base de datos con los criterios de búsqueda
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()

    # Inicializar la consulta SQL
    sql_query = "SELECT * FROM Maestros WHERE 1"

    # Crear una lista de parámetros y una lista de condiciones
    params = []
    condiciones = []

    if current_user.rol != 'supremo':
        # Si el usuario no es supremo, agregar condición de ID_Nucleo
        condiciones.append("ID_Nucleo = ?")
        params.append(current_user.id_nucleo)

    # Agregar condiciones para cada palabra clave
    for palabra_clave in palabras_clave:
        condiciones.append("(Nombre_Maestro LIKE ? OR Apellido_Maestro LIKE ? OR Numero_Documento LIKE ?)")
        params.extend([f"%{palabra_clave}%", f"%{palabra_clave}%", f"%{palabra_clave}%"])

    # Combinar todas las condiciones con operador AND
    if condiciones:
        sql_query += " AND " + " AND ".join(condiciones)

    # Ejecutar la consulta
    cursor.execute(sql_query, params)

    # Obtener los resultados
    resultados = cursor.fetchall()

    conn.close()

    return render_template('lista_maestros.html', maestros=resultados)


@maestros_bp.route('/personal/agregar_personal', methods=['GET', 'POST'])
def agregar_maestro():
    if request.method == 'POST':
        # Lógica para agregar un maestro a la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        numero_documento = request.form['numero_documento']
        descripcion = request.form['descripcion']
        cargo = request.form['cargo']
        funcion = request.form['funcion']
        nivel_educativo = request.form['nivel_educativo']
        fecha_ingreso = request.form['fecha_ingreso']
        id_nucleo = request.form['id_nucleo']
        
        # Obtén el valor del campo Estatus del formulario
        estatus = request.form['estatus']
        
        # Resto de los campos
        cursor.execute("INSERT INTO Maestros (Nombre_Maestro, Apellido_Maestro, Edad, Fecha_Nacimiento, Numero_Documento, Descripcion, Cargo, Funcion, Nivel_Educativo, Fecha_Ingreso, ID_Nucleo, Estatus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (nombre, apellido, edad, fecha_nacimiento, numero_documento, descripcion, cargo, funcion, nivel_educativo, fecha_ingreso, id_nucleo, estatus))
        
        conn.commit()
        conn.close()
        return redirect('/personal')
    return render_template('agregar_maestro.html')


@maestros_bp.route('/personal/editar_personal/<int:id>', methods=['GET', 'POST'])
def editar_maestro(id):
    if request.method == 'POST':
        # Lógica para editar un maestro en la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        numero_documento = request.form['numero_documento']
        descripcion = request.form['descripcion']
        cargo = request.form['cargo']  # Agregar campo "Cargo"
        funcion = request.form['funcion']  # Agregar campo "Funcion"
        nivel_educativo = request.form['nivel_educativo']  # Agregar campo "Nivel_Educativo"
        fecha_ingreso = request.form['fecha_ingreso']  # Agregar campo "Fecha_Ingreso"
        id_nucleo = request.form['id_nucleo']
        
        # Obtén el valor del campo Estatus del formulario
        estatus = request.form['estatus']
        
        # Actualiza los campos en la base de datos
        cursor.execute("UPDATE Maestros SET Nombre_Maestro = ?, Apellido_Maestro = ?, Edad = ?, Fecha_Nacimiento = ?, Numero_Documento = ?, Descripcion = ?, Cargo = ?, Funcion = ?, Nivel_Educativo = ?, Fecha_Ingreso = ?, ID_Nucleo = ?, Estatus = ? WHERE ID_Maestro = ?", 
                       (nombre, apellido, edad, fecha_nacimiento, numero_documento, descripcion, cargo, funcion, nivel_educativo, fecha_ingreso, id_nucleo, estatus, id))
        conn.commit()
        conn.close()
        return redirect('/personal')
    
    # Consulta el maestro con el ID dado para prellenar el formulario
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Maestros WHERE ID_Maestro = ?", (id,))
    maestro = cursor.fetchone()
    conn.close()
    return render_template('editar_maestro.html', maestro=maestro, id=id)


@maestros_bp.route('/eliminar_personal/<int:id>', methods=['GET', 'POST'])
def eliminar_maestro(id):
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()

        # Elimina al alumno con el ID dado
        cursor.execute("DELETE FROM Maestros WHERE ID_Maestro = ?", (id,))

        conn.commit()
        conn.close()

        return redirect('/personal')

    # Consulta el alumno con el ID dado para mostrar los datos antes de eliminarlo
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Maestros WHERE ID_Maestro= ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/personal')

if __name__ == '__main__':
    maestros_bp.run(debug=True)
