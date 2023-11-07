from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import sqlite3
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import current_user, login_required

nucleos_bp = Blueprint('nucleos', __name__)
login_manager = LoginManager()

@nucleos_bp.route('/nucleos', methods=['GET'])
@login_required
def lista_nucleos():
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
    sql_query = "SELECT * FROM Nucleos WHERE 1"

    # Crear una lista de parámetros y una lista de condiciones
    params = []
    condiciones = []

    if current_user.rol != 'supremo':
        # Si el usuario no es supremo, agregar condición de ID_Nucleo
        condiciones.append("Codigo = ?")
        params.append(current_user.id_nucleo)

    # Agregar condiciones para cada palabra clave
    for palabra_clave in palabras_clave:
        condiciones.append("(Nombre_Nucleo LIKE ? OR Codigo LIKE ? OR Direccion LIKE ?)")
        params.extend([f"%{palabra_clave}%", f"%{palabra_clave}%", f"%{palabra_clave}%"])

    # Combinar todas las condiciones con operador AND
    if condiciones:
        sql_query += " AND " + " AND ".join(condiciones)

    # Ejecutar la consulta
    cursor.execute(sql_query, params)

    # Obtener los resultados
    resultados = cursor.fetchall()

    conn.close()

    return render_template('lista_nucleos.html', nucleos=resultados)

@nucleos_bp.route('/nucleos/agregar_nucleo', methods=['GET', 'POST'])
def agregar_nucleo():
    if request.method == 'POST':
        # Lógica para agregar un nucleo a la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        fecha_apertura = request.form['fecha_apertura']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        estatus_inmueble = request.form['estatus_inmueble']
        infraestructura = request.form['infraestructura']

        cursor.execute("INSERT INTO Nucleos (Nombre_Nucleo, Codigo, Fecha_Apertura, Direccion, Telefono, Estatus_Inmueble, Infraestructura) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (nombre, codigo, fecha_apertura, direccion, telefono, estatus_inmueble, infraestructura))

        conn.commit()
        conn.close()
        return redirect('/nucleos')
    return render_template('agregar_nucleos.html')

@nucleos_bp.route('/nucleos/editar_nucleo/<int:id>', methods=['GET', 'POST'])
def editar_nucleo(id):
    if request.method == 'POST':

        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        fecha_apertura = request.form['fecha_apertura']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        estatus_inmueble = request.form['estatus_inmueble']
        infraestructura = request.form['infraestructura']
        
        # Actualiza los campos en la base de datos
        cursor.execute("UPDATE Nucleos SET Nombre_Nucleo = ?, Codigo = ?, Fecha_Apertura = ?, Direccion = ?, Telefono = ?, Estatus_Inmueble = ?, Infraestructura = ? WHERE ID_Nucleo = ?", 
                       (nombre, codigo, fecha_apertura, direccion, telefono, estatus_inmueble, infraestructura, id))
        conn.commit()
        conn.close()
        return redirect('/nucleos')
    
    # Consulta el nucleo con el ID dado para prellenar el formulario
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Nucleos WHERE ID_Nucleo = ?", (id,))
    nucleo = cursor.fetchone()
    conn.close()
    return render_template('editar_nucleos.html', nucleo=nucleo, id=id)

@nucleos_bp.route('/eliminar_nucleos/<int:id>', methods=['GET', 'POST'])
def eliminar_nucleo(id):
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()

        # Elimina el núcleo con el ID dado
        cursor.execute("DELETE FROM Nucleos WHERE ID_Nucleo = ?", (id,))

        conn.commit()
        conn.close()

        return redirect('/nucleos')

    # Consulta el núcleo con el ID dado para mostrar los datos antes de eliminarlo
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Nucleos WHERE ID_Nucleo = ?", (id,))
    conn.commit()
    conn.close()
    return render_template('/nucleos')


if __name__ == '__main__':
    nucleos_bp.run(debug=True)
