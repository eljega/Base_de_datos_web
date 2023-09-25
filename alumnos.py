from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import sqlite3
from flask_login import login_manager  # Importa login_manager
from flask_login import LoginManager
from flask_login import current_user, login_required


alumnos_bp = Blueprint('alumnos', __name__)
login_manager = LoginManager()

@alumnos_bp.route('/alumnos', methods=['GET'])
@login_required
def lista_alumnos():
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
    sql_query = "SELECT * FROM Alumnos WHERE 1"

    # Crear una lista de parámetros y una lista de condiciones
    params = []
    condiciones = []

    if current_user.rol != 'supremo':
        # Si el usuario no es supremo, agregar condición de ID_Nucleo
        condiciones.append("ID_Nucleo = ?")
        params.append(current_user.id_nucleo)

    # Agregar condiciones para cada palabra clave
    for palabra_clave in palabras_clave:
        condiciones.append("(Nombre_Alumno LIKE ? OR Apellido_Alumno LIKE ?)")
        params.extend([f"%{palabra_clave}%", f"%{palabra_clave}%"])

    # Combinar todas las condiciones con operador AND
    if condiciones:
        sql_query += " AND " + " AND ".join(condiciones)

    # Ejecutar la consulta
    cursor.execute(sql_query, params)

    # Obtener los resultados
    resultados = cursor.fetchall()


    conn.close()

    return render_template('lista_alumnos.html', alumnos=resultados)




@alumnos_bp.route('/agregar_alumno', methods=['GET', 'POST'])
def agregar_alumno():
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        numero_documento = request.form['numero_documento']
        descripcion = request.form['descripcion']
        id_nucleo = request.form['id_nucleo']
        catedra = request.form['catedra']  # Nuevo campo "Catedra"
        # Resto de los campos
        cursor.execute("INSERT INTO Alumnos (Nombre_Alumno, Apellido_alumno, Edad, Fecha_Nacimiento, Numero_Documento, Descripcion, ID_Nucleo, Catedra) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               (nombre, apellido, edad, fecha_nacimiento, numero_documento, descripcion, id_nucleo, catedra))  # Agrega "catedra" a la tupla
        conn.commit()
        conn.close()

        return redirect('/alumnos')
    return render_template('agregar_alumno.html')

@alumnos_bp.route('/editar_alumno/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        numero_documento = request.form['numero_documento']
        descripcion = request.form['descripcion']
        id_nucleo = request.form['id_nucleo']
        catedra = request.form['catedra']  # Nuevo campo "Catedra"

        # Actualiza los campos en la base de datos
        cursor.execute("UPDATE Alumnos SET Nombre_Alumno = ?, Apellido_alumno = ?, Edad = ?, Fecha_Nacimiento = ?, Numero_Documento = ?, Descripcion = ?, ID_Nucleo = ?, Catedra = ? WHERE ID_Alumno = ?", 
                       (nombre, apellido, edad, fecha_nacimiento, numero_documento, descripcion, id_nucleo, catedra, id))
        conn.commit()
        conn.close()

        return redirect('/alumnos')

    # Consulta el alumno con el ID dado para prellenar el formulario
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Alumnos WHERE ID_Alumno = ?", (id,))
    alumno = cursor.fetchone()
    conn.close()

    return render_template('editar_alumno.html', alumno=alumno, id=id)

@alumnos_bp.route('/eliminar_alumno/<int:id>', methods=['GET', 'POST'])
def eliminar_alumno(id):
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()

        # Elimina al alumno con el ID dado
        cursor.execute("DELETE FROM Alumnos WHERE ID_Alumno = ?", (id,))

        conn.commit()
        conn.close()

        return redirect('/alumnos')

    # Consulta el alumno con el ID dado para mostrar los datos antes de eliminarlo
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Alumnos WHERE ID_Alumno = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/alumnos')


if __name__ == '__main__':
    alumnos_bp.run(debug=True)

