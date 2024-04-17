from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EntrenamientoNotFoundError
from ..dynamodb_entrenamiento import DynamoDbEntrenamiento

class GetEntrenamientosUser (BaseCommannd):
  def __init__(self, id_usuario):
    if id_usuario and id_usuario.strip():
      self.id_usuario = id_usuario
    else:
      raise InvalidParams()
  
  def execute(self):
    result  = DynamoDbEntrenamiento().get_Items_user(self.id_usuario)
    if result is None:
      raise EntrenamientoNotFoundError()
    
    return result