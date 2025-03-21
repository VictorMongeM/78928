from flask import Flask, render_template, redirect, url_for
from productos import Producto
from flask import request
from flask import Response

app = Flask(__name__)


productos = [Producto("Computadora",55), Producto("Impresora", 78), Producto("Monitor", 45)]

# Ruta de inicio
@app.route('/')
def inicio():
    return render_template('productos.html', productos = productos)

@app.route('/editar/<producto>/<precio>')
def editar(producto,precio):
    print(producto, precio)
    return render_template('editar.html', producto = producto, precio = precio)

# Por defecto el metodo activo es get, hay que cambiarlo a post
@app.route('/guardar', methods=['POST'])
def guardar():
    # requesr.form.get() es una forma de obtener los datos enviados por el formulario
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    i = 0
    for e in productos:
        if e.nombre == n:
            # Si el producto ya existe, se actualiza el precio
            productos[i] = Producto(n, p)
            print(f"{e.nombre} {e.precio}")
        i += 1
    
    # Importante retornar estatus 302 para que el navegador haga una redirección
    return Response("guardado", headers={'Location': '/'}, status=302)

# Eliminar un producto
@app.route('/eliminar/<producto>')
def eliminar(producto):
    print(producto)
    i = 0
    for e in productos:
        if e.nombre == producto:
            productos.pop(i)
        i += 1
    return Response("eliminado", headers={'Location': '/'}, status=302)

# Agregar un producto
@app.route('/agregar', methods=['POST'])
def agregar():
    n = request.form.get('nombre')
    p = request.form.get('precio')
    print(n, p)
    productos.append(Producto(n, p))
    # Implementación directa de Response("guardado", headers={'Location': '/'}, status=302)
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)