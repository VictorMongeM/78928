from flask import Flask, render_template, redirect, url_for
from productos import Producto
from flask import request
from flask import Response
import sqlite3

app = Flask(__name__)

#productos = [Producto("Computadora",55), Producto("Impresora", 78), Producto("Monitor", 45)]

# Ruta de inicio
@app.route('/')
def inicio():
    con = conexion()
    # fetchall() obtiene todos los registros
    productos = con.execute('SELECT * FROM productos').fetchall()
    print(productos)
    con.close()
    return render_template('productos.html', productos = productos)

#@app.route('/editar/<producto>/<precio>')
@app.route('/editar/<id>')
def editar(id):
    print(id)
    con = conexion()
    # fetchone() obtiene un solo registro
    p = con.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    con.close()
    # Se regresa el producto como un diccionario
    return render_template('editar.html', producto = p)

# Por defecto el metodo activo es get, hay que cambiarlo a post
@app.route('/guardar', methods=['POST'])
def guardar():
    # requesr.form.get() es una forma de obtener los datos enviados por el formulario
    n = request.form.get('nombre')
    p = request.form.get('precio')
    id = request.form.get('id')
    print(id, n, p)
    
    con = conexion()
    con.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?', (n, p, id))
    con.commit()
    con.close()

    # Importante retornar estatus 302 para que el navegador haga una redirección
    return Response("guardado", headers={'Location': '/'}, status=302)

# Eliminar un producto
@app.route('/eliminar/<id>')
def eliminar(id):
    print(id)
    con = conexion()
    con.execute('DELETE FROM productos WHERE id = ?', (id,))
    con.commit()
    con.close()
    return Response("eliminado", headers={'Location': '/'}, status=302)

# Agregar un producto
@app.route('/agregar', methods=['POST'])
def agregar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    con = conexion()
    con.execute('INSERT INTO productos (nombre, precio) VALUES (?, ?)', (n, p))
    con.commit()
    con.close()
    #productos.append(Producto(n, p))
    # Implementación directa de Response("guardado", headers={'Location': '/'}, status=302)
    return redirect(url_for('inicio'))

def conexion():
    con = sqlite3.connect('basedatos.db')
    # Se configura para que los datos se puedan acceder por nombre de columna
        # row_factory es una propiedad de la conexión
        # sqlite3.Row es una clase que permite acceder a los datos por nombre de columna
        # Si no se pone nos regresa la tupla no el diccionario
    con.row_factory = sqlite3.Row
    return con

def iniciar_db():
    con = conexion()
    # No se usa cursor porque se puede acceder a la base de datos directamente
    con.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
    ''')
    # Importante hacer commit para que los cambios se guarden
    con.commit()
    con.close()

if __name__ == '__main__':
    iniciar_db()
    app.run(host = '0.0.0.0', debug = True)