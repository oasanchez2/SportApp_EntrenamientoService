from .base_command import BaseCommannd
from .. import dynamodb_entrenamiento

class Reset(BaseCommannd):  
  def execute(self):
    dynamodb_entrenamiento.deleteTable()
    dynamodb_entrenamiento.create_table()