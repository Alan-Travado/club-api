from flask import Flask
from errors import registrar_manejadores
from routes.bloqueos import bp as bloqueos_bp
from routes.canchas import bp as canchas_bp
from routes.deportes import bp as deportes_bp
from routes.reservas import bp as reservas_bp
from routes.socios import bp as socios_bp

app = Flask(__name__)
app.json.sort_keys = False

registrar_manejadores(app)
app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(bloqueos_bp)

if __name__ == "__main__":
    app.run(debug=True)
