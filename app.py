from flask import Flask,jsonify
from models import init_db,db
from routes.auth_routes import auth_bp
from routes.buku_routes import buku_bp
from config import Config
from flasgger import Swagger
from utils.response import error_message

app = Flask(__name__)
app.config.from_object(Config)

Swagger(app)
init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(buku_bp)

@app.route('/')
def home():
    return {"message": "API Active"}

@app.errorhandler(404)
def not_found_error(error):
    return error_message(message="Endpoint tidak ditemukan", status_code=404)

@app.errorhandler(500)
def internal_error(error):
    return error_message(message="Terjadi kesalahan pada server", status_code=500)

if __name__ == '__main__':
    app.run(debug=True)