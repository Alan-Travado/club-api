from flask import Flask
from errors import registrar_manejadores
from routes.canchas import bp as canchas_bp
from routes.deportes import bp as deportes_bp

app = Flask(__name__)
app.json.sort_keys = False

registrar_manejadores(app)
app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)

if __name__ == "__main__":
    app.run(debug=True)