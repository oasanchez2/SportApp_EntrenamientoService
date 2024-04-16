import unittest
from unittest.mock import MagicMock, patch
from src.dynamodb_entrenamiento import DynamoDbEntrenamiento
from src.models.entrenamiento import Entrenamiento

class TestDynamodbEntrenamientoService(unittest.TestCase):
    @patch('src.dynamodb_entrenamiento.boto3')
    @patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'your_access_key_id', 'AWS_SECRET_ACCESS_KEY': 'your_secret_access_key'})
    def test_create_table(self, mock_boto3):
        dynamodb_mock = MagicMock()
        mock_boto3.client.return_value = dynamodb_mock

        dynamo_db = DynamoDbEntrenamiento()
        dynamo_db.tablaExits = MagicMock(return_value=False)
        dynamo_db.create_table()

        dynamodb_mock.create_table.assert_called_once()
    
    @patch('src.dynamodb_entrenamiento.boto3')
    @patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'your_access_key_id', 'AWS_SECRET_ACCESS_KEY': 'your_secret_access_key'})
    def test_insert_item(self, mock_boto3):
        dynamodb_mock = MagicMock()
        mock_boto3.client.return_value = dynamodb_mock

        dynamo_db = DynamoDbEntrenamiento()
        entrenamiento = Entrenamiento(id_entrenamiento='1', nombre='Entrenamiento de prueba', fecha_entrenamiento='2024-04-14', id_usuario='usuario123', estado=True,ejercicios=[])
        dynamo_db.insert_item(entrenamiento)

        dynamodb_mock.put_item.assert_called_once()

    @patch('src.dynamodb_entrenamiento.boto3')
    @patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'your_access_key_id', 'AWS_SECRET_ACCESS_KEY': 'your_secret_access_key'})
    def test_get_item(self, mock_boto3):
        dynamodb_mock = MagicMock()
        mock_boto3.client.return_value = dynamodb_mock

        dynamo_db = DynamoDbEntrenamiento()
        id_entrenamiento = '1'
        dynamo_db.get_item(id_entrenamiento)

        dynamodb_mock.get_item.assert_called_once()

    @patch('src.dynamodb_entrenamiento.boto3')
    @patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'your_access_key_id', 'AWS_SECRET_ACCESS_KEY': 'your_secret_access_key'})
    def test_get_item_nombre(self, mock_boto3):
        dynamodb_mock = MagicMock()
        mock_boto3.client.return_value = dynamodb_mock

        dynamo_db = DynamoDbEntrenamiento()
        nombre = 'Entrenamiento de prueba'
        dynamo_db.get_Item_nombre(nombre)

        dynamodb_mock.scan.assert_called_once()

    @patch('src.dynamodb_entrenamiento.boto3')
    @patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'your_access_key_id', 'AWS_SECRET_ACCESS_KEY': 'your_secret_access_key'})
    def test_tablaExits(self, mock_boto3):
        dynamodb_mock = MagicMock()
        mock_boto3.client.return_value = dynamodb_mock

        dynamo_db = DynamoDbEntrenamiento()
        name = 'entrenamiento'
        dynamo_db.tablaExits(name)

        dynamodb_mock.describe_table.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()