import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from api.service.redis_client import RedisClient


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": "GET"}})

auth = HTTPTokenAuth()

# Checkout token
@auth.verify_token
def verify_token(token):
    expected_token = os.getenv('COINSNARK_TOKEN')
    if not expected_token:
        return False 

    return token == expected_token


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Data not found'}), 404


# Middleware para negar solicitações com parâmetros
def no_parameter_middleware(func):
    def wrapper(*args, **kwargs):
        if request.args:
            return jsonify({'error': 'No parameters allowed'}), 400
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/exrates')
@auth.login_required
@no_parameter_middleware
def get_exrates():
    # Instância RedisClient com os parâmetros de conexão
    redis_client = RedisClient(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        password=os.getenv('REDIS_KEY')
    )
    
    exrates_data = redis_client.get_exrates()
    if exrates_data:
        # Convertendo as chaves e valores para strings
        exrates_data_str = {key.decode('utf-8'): value.decode('utf-8') for key, value in exrates_data.items()}
        return jsonify(exrates_data_str)
    else:
        return jsonify({'error': 'Data not found'}), 404
