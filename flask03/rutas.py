from flask import Blueprint

rutas_bp = Blueprint('rutas', __name__)

@rutas_bp.route('/ruta1')
def ruta1():
        return "Ruta 1"

@rutas_bp.route('/ruta2')
def ruta2():
        return "Ruta 2"