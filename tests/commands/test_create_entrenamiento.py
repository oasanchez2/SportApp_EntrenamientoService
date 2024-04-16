import unittest
from unittest.mock import MagicMock, patch
from src.commands.create_entrenamiento import CreateEntrenamiento, Entrenamiento, Ejercicio
from src.errors.errors import IncompleteParams, InvalidNombreError, EntrenamientoAlreadyExists
from src.dynamodb_entrenamiento import DynamoDbEntrenamiento

class TestCreateEntrenamiento(unittest.TestCase):

    def setUp(self):
        self.mock_data = {
            'nombre': 'Entrenamiento de prueba',
            'fecha_entrenamiento': '2024-04-14',
            'id_usuario': 'usuario123',
            'estado': True,
            'ejercicios': [
                {
                    'estado': True,
                    'id_ejercicio': 'ejercicio123',
                    'nombre': 'Ejercicio de prueba',
                    'url_imagen': 'https://example.com/ejercicio.jpg',
                    'numero_repeticiones': 10
                }
            ]
        }

    @patch('src.commands.create_entrenamiento.DynamoDbEntrenamiento')
    def test_execute_success(self, mock_dynamo):
        mock_dynamo_instance = MagicMock()
        mock_dynamo.return_value = mock_dynamo_instance
        # Simulamos que el entrenamiento no existe
        mock_dynamo_instance.get_Item_nombre.return_value = None

        create_entrenamiento = CreateEntrenamiento(self.mock_data)
        result = create_entrenamiento.execute()

        mock_dynamo_instance.insert_item.assert_called_once_with(result)
        self.assertEqual(result.nombre, 'Entrenamiento de prueba')

    @patch('src.commands.create_entrenamiento.DynamoDbEntrenamiento')
    def test_execute_invalid_nombre(self, mock_dynamo):
        mock_dynamo_instance = MagicMock()
        mock_dynamo.return_value = mock_dynamo_instance

        invalid_data = self.mock_data.copy()
        invalid_data['nombre'] = ''

        create_entrenamiento = CreateEntrenamiento(invalid_data)
        with self.assertRaises(InvalidNombreError):
            create_entrenamiento.execute()

        mock_dynamo_instance.insert_item.assert_not_called()

    @patch('src.commands.create_entrenamiento.DynamoDbEntrenamiento')
    def test_execute_entrenamiento_exists(self, mock_dynamo):
        mock_dynamo_instance = MagicMock()
        mock_dynamo.return_value = mock_dynamo_instance
        mock_dynamo_instance.get_Item_nombre.return_value = [Entrenamiento("id", "nombre", "fecha", "id_usuario", True, [])]

        create_entrenamiento = CreateEntrenamiento(self.mock_data)
        with self.assertRaises(EntrenamientoAlreadyExists):
            create_entrenamiento.execute()

        mock_dynamo_instance.insert_item.assert_not_called()

    def test_entrenamiento_exist_true(self):
        create_entrenamiento = CreateEntrenamiento(self.mock_data)
        create_entrenamiento.entrenamiento_exist = MagicMock(return_value=True)

        result = create_entrenamiento.entrenamiento_exist('Entrenamiento de prueba')

        self.assertTrue(result)

    def test_entrenamiento_exist_false(self):
        create_entrenamiento = CreateEntrenamiento(self.mock_data)
        create_entrenamiento.entrenamiento_exist = MagicMock(return_value=False)

        result = create_entrenamiento.entrenamiento_exist('Entrenamiento de prueba')

        self.assertFalse(result)

    def test_verificar_datos_valid(self):
        create_entrenamiento = CreateEntrenamiento(self.mock_data)

        result = create_entrenamiento.verificar_datos('Entrenamiento de prueba')

        self.assertTrue(result)

    def test_verificar_datos_invalid(self):
        create_entrenamiento = CreateEntrenamiento(self.mock_data)

        result = create_entrenamiento.verificar_datos('')

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
