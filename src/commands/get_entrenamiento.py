from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, EntrenamientoNotFoundError
from .. import dynamodb_entrenamiento

class GetEntrenamiento (BaseCommannd):
  def __init__(self, entrenamiento_id):
    if entrenamiento_id and entrenamiento_id.strip():
      self.entrenamiento_id = entrenamiento_id
    else:
      raise InvalidParams()
  
  def execute(self):

    result  = dynamodb_entrenamiento.get_item(self.entrenamiento_id)
    if result is None:
      raise EntrenamientoNotFoundError()
    
    return result