from flask import Flask, jsonify, request, Blueprint
from ..commands.create_entrenamiento import CreateEntrenamiento
from ..commands.get_entrenamiento import GetEntrenamiento
from ..commands.get_entrenamientos_user import GetEntrenamientosUser
from ..commands.reset import Reset

entrenamientos_blueprint = Blueprint('entrenamientos', __name__)

@entrenamientos_blueprint.route('/entrenamientos', methods = ['POST'])
def create():
    entrenamiento = CreateEntrenamiento(request.get_json()).execute()
    return jsonify(entrenamiento), 201

@entrenamientos_blueprint.route('/entrenamientos/<id>', methods = ['GET'])
def show(id):
    """ Authenticate(auth_token()).execute() """
    entrenamiento = GetEntrenamiento(id).execute() 
    return jsonify(entrenamiento)

@entrenamientos_blueprint.route('/entrenamientos/user/<id>', methods = ['GET'])
def show_user(id):
    """ Authenticate(auth_token()).execute() """
    entrenamiento = GetEntrenamientosUser(id).execute() 
    return jsonify(entrenamiento)

@entrenamientos_blueprint.route('/entrenamientos/ping', methods = ['GET'])
def ping():
    return 'pong'

@entrenamientos_blueprint.route('/entrenamientos/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization