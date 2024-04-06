from .base_command import BaseCommannd
from ..models.entrenamiento import Entrenamiento, EntrenamientoSchema, EntrenamientoJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, InvalidParams, EntrenamientoNotFoundError

class GetEntrenamiento (BaseCommannd):
  def __init__(self, entrenamiento_id):
    if self.is_integer(entrenamiento_id):
      self.entrenamiento_id = int(entrenamiento_id)
    elif self.is_float(entrenamiento_id):
      self.entrenamiento_id = int(float(entrenamiento_id))
    else:
      raise InvalidParams()
  
  def execute(self):
    session = Session()

    if len(session.query(Entrenamiento).filter_by(id=self.entrenamiento_id).all()) <= 0:
      session.close()
      raise EntrenamientoNotFoundError()
    
    entrenamiento = session.query(Entrenamiento).filter_by(id=self.entrenamiento_id).one()
    schema = EntrenamientoSchema()
    entrenamiento = schema.dump(entrenamiento)

    session.close()

    return entrenamiento
  
      
  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False