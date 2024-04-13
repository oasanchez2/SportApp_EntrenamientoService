import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
#from .models.entrenamiento import Entrenamiento
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

        dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id_entrenamiento',
                        'AttributeType': 'S',
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
          
        # Espera hasta que la tabla exista
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)
        print(f'Tabla {table_name} creada correctamente.')
    else:
        print(f"La tabla '{table_name}' ya existe.")

def insert_item(entrenamiento: Entrenamiento):
    item = {
        "id_entrenamiento": {'S':  entrenamiento.id_entrenamiento },
        'nombre': {'S': entrenamiento.nombre },
        'fecha_entrenamiento': {'S': entrenamiento.fecha_entrenamiento},  # Datetime conversion
        'id_usuario': {'S': entrenamiento.id_usuario },
        'estado': {'BOOL': entrenamiento.estado },
        'ejercicios': {'L': [
            {
                'M': {
                    'estado': {'BOOL': ejercicio.estado},
                    'id_ejercicio': {'S': ejercicio.id_ejercicio},
                    'nombre': {'S': ejercicio.nombre},
                    'url_imagen': {'S': ejercicio.url_imagen},
                    'numero_repeticiones': {'N': str(ejercicio.numero_repeticiones)}
                }
            }
            for ejercicio in entrenamiento.ejercicios
        ]}
        # Puedes agregar más atributos según la definición de tu tabla
    }
    result = dynamodb.put_item(
        TableName=table_name,
        Item=item,
        ReturnConsumedCapacity='TOTAL'
    )
    print('Ítem insertado correctamente.')

def get_item(id_entrenamiento):
    key = {
        'id_entrenamiento': {'S': str(id_entrenamiento) }  # Clave de búsqueda
    }
    response = dynamodb.get_item(
        TableName=table_name,
        Key=key
    )
    item = response.get('Item')
    if not item:
        return None
    
    # Extrae los valores de cada campo
    id_entrenamiento = item['id_entrenamiento']['S']
    nombre = item['nombre']['S']
    fecha_entrenamiento = item['fecha_entrenamiento']['S']
    id_usuario = item['id_usuario']['S']
    estado = item['estado']['BOOL']

    # Extrae los ejercicios del item
    ejercicios = []
    if 'ejercicios' in item:
        for ejercicio_item in item['ejercicios']['L']:
            ejercicio = {
                'estado': ejercicio_item['M']['estado']['BOOL'],
                'id_ejercicio': ejercicio_item['M']['id_ejercicio']['S'],
                'nombre': ejercicio_item['M']['nombre']['S'],
                'url_imagen': ejercicio_item['M']['url_imagen']['S'],
                'numero_repeticiones': int(ejercicio_item['M']['numero_repeticiones']['N'])
            }
            ejercicios.append(ejercicio)

    # Crea una instancia de la clase Entrenamiento
    entrenamiento = Entrenamiento(id_entrenamiento,nombre, fecha_entrenamiento, id_usuario, estado, ejercicios=ejercicios)

    return entrenamiento

def get_Item_nombre(nombre):
    
    # Parámetros para la operación de escaneo
    parametros = {
        'TableName': table_name,
        'FilterExpression': '#nombre = :nombre',
        'ExpressionAttributeNames': {
            '#nombre': 'nombre'
        },
        'ExpressionAttributeValues': {
            ':nombre': {'S': nombre}
        }
    }
    
    # Realizar el escaneo
    response = dynamodb.scan(**parametros)
    print(response)
    # Obtener los items encontrados
    items = response.get('Items', [])
    if not items:
        return None
    
    # Procesar los items encontrados
    resultados = []
    for item in items:
        id_entrenamiento = item['id_entrenamiento']['S']
        nombre = item['nombre']['S']
        fecha_entrenamiento = item['fecha_entrenamiento']['S']
        id_usuario = item['id_usuario']['S']
        estado = item['estado']['BOOL']

        # Extrae los ejercicios del item
        ejercicios = []
        if 'ejercicios' in item:
            for ejercicio_item in item['ejercicios']['L']:
                ejercicio = {
                    'estado': ejercicio_item['M']['estado']['BOOL'],
                    'id_ejercicio': ejercicio_item['M']['id_ejercicio']['S'],
                    'nombre': ejercicio_item['M']['nombre']['S'],
                    'url_imagen': ejercicio_item['M']['url_imagen']['S'],
                    'numero_repeticiones': int(ejercicio_item['M']['numero_repeticiones']['N'])
                }
                ejercicios.append(ejercicio)

        entrenamiento = Entrenamiento(id_entrenamiento,nombre, fecha_entrenamiento, id_usuario, estado,  ejercicios=ejercicios)
        resultados.append(entrenamiento)

    return resultados

def tablaExits(name):
    try:
        response = dynamodb.describe_table(TableName=name)
        print(response)
        return True
    except ClientError as err:
        print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            return False

def deleteTable():
    # Eliminar la tabla
    dynamodb.delete_table(TableName=table_name)

    # Esperar hasta que la tabla no exista
    dynamodb.get_waiter('table_not_exists').wait(TableName=table_name)