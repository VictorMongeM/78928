from flask import Flask
# uso de blueprint, permite modularizar los endpoints
from rutas import rutas_bp

app = Flask(__name__)
# Registro del blueprint
app.register_blueprint(rutas_bp)

@app.route('/')
def inicio():
    return "Página de inicio"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)