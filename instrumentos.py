from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import sqlite3
from flask_login import login_manager  # Importa login_manager
from flask_login import LoginManager
from flask_login import current_user, login_required

instrumentos_bp = Blueprint('instrumentos', __name__)
login_manager = LoginManager()

@instrumentos_bp.route('/instrumentos', methods=['GET'])
@login_required
def lista_instrumentos():
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
    sql_query = "SELECT * FROM Instrumentos WHERE 1"

    # Crear una lista de parámetros y una lista de condiciones
    params = []
    condiciones = []

    if current_user.rol != 'supremo':
        # Si el usuario no es supremo, agregar condición de ID_Nucleo
        condiciones.append("ID_Nucleo = ?")
        params.append(current_user.id_nucleo)

    # Agregar condiciones para cada palabra clave
    for palabra_clave in palabras_clave:
        condiciones.append("(Modelo LIKE ? OR Color LIKE ? OR Numero_Serial LIKE ?)")
        params.extend([f"%{palabra_clave}%", f"%{palabra_clave}%", f"%{palabra_clave}%"])

    # Combinar todas las condiciones con operador AND
    if condiciones:
        sql_query += " AND " + " AND ".join(condiciones)

    # Ejecutar la consulta
    cursor.execute(sql_query, params)

    # Obtener los resultados
    resultados = cursor.fetchall()

    conn.close()

    return render_template('lista_instrumentos.html', instrumentos=resultados)

@instrumentos_bp.route('/instrumentos/agregar_instrumento', methods=['GET', 'POST'])
def agregar_instrumento():
    if request.method == 'POST':
        # Lógica para agregar un instrumento a la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        
        item = request.form['item']
        marca = request.form['marca']
        cantidad = request.form['cantidad']
        modelo = request.form['modelo']
        medida = request.form['medida']
        color = request.form['color']
        serial = request.form['serial']
        inventario = request.form['inventario']
        accesorio = request.form['accesorio']
        condicion = request.form['condicion']
        ubicacion = request.form['ubicacion']
        procedencia = request.form['procedencia']
        comodato_vigente = request.form['comodato_vigente']
        descripcion = request.form['descripcion']
        id_nucleo = request.form["id_nucleo"]

        # Insertar el nuevo instrumento en la base de datos
        cursor.execute("INSERT INTO Instrumentos (Item, Marca, Cantidad, Modelo, Medida, Color, Numero_Serial, Numero_Inventario, Accesorio, Condicion, Ubicacion, Procedencia, Comodato_Vigente, Descripcion, ID_Nucleo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (item, marca, cantidad, modelo, medida, color, serial, inventario, accesorio, condicion, ubicacion, procedencia, comodato_vigente, descripcion, id_nucleo))

        conn.commit()
        conn.close()
        return redirect('/instrumentos')
    
    return render_template('agregar_instrumentos.html')


@instrumentos_bp.route('/instrumentos/editar_instrumento/<int:id>', methods=['GET', 'POST'])
def editar_instrumento(id):
    if request.method == 'POST':
        # Lógica para editar un instrumento en la base de datos
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()
        
        item = request.form['item']
        marca = request.form['marca']
        cantidad = request.form['cantidad']
        modelo = request.form['modelo']
        medida = request.form['medida']
        color = request.form['color']
        serial = request.form['serial']
        inventario = request.form['inventario']
        accesorio = request.form['accesorio']
        condicion = request.form['condicion']
        ubicacion = request.form['ubicacion']
        procedencia = request.form['procedencia']
        comodato_vigente = request.form['comodato_vigente']
        descripcion = request.form['descripcion']
        id_nucleo = request.form["id_nucleo"]
        
        # Actualiza los campos en la base de datos
        cursor.execute("UPDATE Instrumentos SET Item = ?, Marca = ?, Cantidad = ?, Modelo = ?, Medida = ?, Color = ?, Numero_Serial = ?, Numero_Inventario = ?, Accesorio = ?, Condicion = ?, Ubicacion = ?, Procedencia = ?, Comodato_Vigente = ?, Descripcion = ?, ID_Nucleo = ? WHERE ID_Instrumento= ?", 
                       (item, marca, cantidad, modelo, medida, color, serial, inventario, accesorio, condicion, ubicacion, procedencia, comodato_vigente, descripcion, id_nucleo, id))
        conn.commit()
        conn.close()
        return redirect('/instrumentos')
    
    # Consulta el instrumento con el ID dado para prellenar el formulario
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Instrumentos WHERE ID_Instrumento = ?", (id,))
    instrumento = cursor.fetchone()
    conn.close()
    return render_template('editar_instrumentos.html', instrumento=instrumento, id=id)

@instrumentos_bp.route('/instrumentos/eliminar_instrumento/<int:id>', methods=['GET', 'POST'])
def eliminar_instrumento(id):
    if request.method == 'POST':
        conn = sqlite3.connect("sistema_musical.db")
        cursor = conn.cursor()

        # Elimina el instrumento con el ID dado
        cursor.execute("DELETE FROM Instrumentos WHERE ID_Instrumento = ?", (id,))

        conn.commit()
        conn.close()

        return redirect('/instrumentos')

    # Consulta el instrumento con el ID dado para mostrar los datos antes de eliminarlo
    conn = sqlite3.connect("sistema_musical.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Instrumentos WHERE ID_Instrumento = ?", (id,))
    instrumento = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('eliminar_instrumento.html', instrumento=instrumento)



if __name__ == '__main__':
    instrumentos_bp.run(debug=True)
