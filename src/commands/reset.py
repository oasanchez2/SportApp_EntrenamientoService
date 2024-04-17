from .base_command import BaseCommannd
from ..dynamodb_entrenamiento import DynamoDbEntrenamiento

class Reset(BaseCommannd):  
  def execute(self):
    DynamoDbEntrenamiento().deleteTable()
    DynamoDbEntrenamiento().create_table()