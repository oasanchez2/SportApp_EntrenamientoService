import unittest
from unittest.mock import patch, MagicMock

from flask import Flask
from src.blueprints.entrenamiento import entrenamientos_blueprint, auth_token
from src.commands.create_entrenamiento import CreateEntrenamiento
from src.commands.get_entrenamiento import GetEntrenamiento
from src.commands.reset import Reset

app = Flask(__name__)
app.register_blueprint(entrenamientos_blueprint)

class TestEntrenamientos(unittest.TestCase):
    '''
    @patch('flask.request')
    def test_create_entrenamiento_exito(self, mock_request):
        mock_request.get_json.return_value = {'nombre': 'Entrenamiento de pierna'}
        mock_entrenamiento = MagicMock()
        mock_entrenamiento.id = 1
        # Reemplazar con la implementación real de CreateEntrenamiento
        with patch.object(CreateEntrenamiento, 'execute', return_value=mock_entrenamiento):
            response = app.test_client().post('/entrenamientos', json={'nombre': 'Entrenamiento de pierna'})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'id': 1})

    @patch('flask.request')
    def test_create_entrenamiento_falta_informacion(self, mock_request):
        mock_request.get_json.return_value = {}
        response = app.test_client().post('/entrenamientos')
        self.assertEqual(response.status_code, 400)  # Código de error para peticiones malformadas

    @patch('flask.request')
    def test_show_entrenamiento_exito(self, mock_request):
        # Simular autorización (reemplazar con autenticación real)
        mock_request.headers = {'Authorization': 'token'}
        mock_entrenamiento = MagicMock()
        mock_entrenamiento.id = 1
        mock_entrenamiento.nombre = 'Entrenamiento de pierna'
        # Reemplazar con la implementación real de GetEntrenamiento
        with patch.object(GetEntrenamiento, 'execute', return_value=mock_entrenamiento):
            response = app.test_client().get('/entrenamientos/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'id': 1, 'nombre': 'Entrenamiento de pierna'})

    @patch('flask.request')
    def test_show_entrenamiento_falta_autorizacion(self, mock_request):
        mock_request.headers = {}
        response = app.test_client().get('/entrenamientos/1')
        self.assertEqual(response.status_code, 401)  # Código de error para no autorizado

    @patch('flask.request')
    def test_show_entrenamiento_id_invalido(self, mock_request):
        # Simular autorización (reemplazar con autenticación real)
        mock_request.headers = {'Authorization': 'token'}
        response = app.test_client().get('/entrenamientos/invalid_id')
        self.assertEqual(response.status_code, 404)  # Código de error para no encontrado

    def test_ping(self):
        response = app.test_client().get('/entrenamientos/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'pong')

    def test_reset(self):
        # Reemplazar con la implementación real de Reset
        with patch.object(Reset, 'execute'):
            response = app.test_client().post('/entrenamientos/reset')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'OK'})

    def test_auth_token_con_autorizacion(self):
        headers = {'Authorization': 'token'}
        authorization = auth_token(headers)
        self.assertEqual(authorization, 'token')

    def test_auth_token_sin_autorizacion(self):
        headers = {}
        authorization = auth_token(headers)
        self.assertEqual(authorization, None)
    '''
