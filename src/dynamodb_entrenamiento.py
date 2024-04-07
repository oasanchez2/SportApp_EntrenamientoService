import boto3
import os
from .models.entrenamiento import Entrenamiento
from botocore.exceptions import ClientError

# Crear una instancia de cliente DynamoDB
dynamodb = boto3.client('dynamodb',
                        region_name='us-east-1',
                        aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
table_name = 'entrenamiento'

# Funciones para interactuar con DynamoDB

def create_table():
    if not tablaExits(table_name):

        table = dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id_entrenamiento',
                        'AttributeType': 'N',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'id_entrenamiento',
                        'KeyType': 'HASH'  # Clave de partición
                    }
                ],        
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
                } 
            )
          
        print(f'Tabla {table_name} creada correctamente.')
    else:
        print(f"La tabla '{table_name}' ya existe.")

def insert_item(entrenamiento: Entrenamiento):
    item = {
        'id_entrenamiento': {'N': str(entrenamiento.id) },  # Atributo de clave, S indica tipo de String
        'nombre': {'S': entrenamiento.nombre },
        'fecha_entrenamiento': {'S': entrenamiento.fecha_entrenamiento.strftime('%Y-%m-%d %H:%M:%S')},  # Datetime conversion
        'id_usuario': {'N': str(entrenamiento.id_usuario) },
        'estado': {'BOOL': entrenamiento.estado }
        # Puedes agregar más atributos según la definición de tu tabla
    }
    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print('Ítem insertado correctamente.')

def get_item(id_entrenamiento):
    key = {
        'id_entrenamiento': {'N': str(id_entrenamiento) }  # Clave de búsqueda
    }
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    item = response.get('Item')
    return item

def tablaExits(name):
    try:
        response = dynamodb.describe_table(TableName=name)
        print(response)
        return True
    except ClientError as err:
        print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            return False