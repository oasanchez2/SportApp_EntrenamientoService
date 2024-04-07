from .base_command import BaseCommannd
from ..models.entrenamiento import Entrenamiento, EntrenamientoSchema, EntrenamientoJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidNombreError, EntrenamientoAlreadyExists
from .. import dynamodb_entrenamiento

class CreateEntrenamiento(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_entrenamiento = EntrenamientoSchema(
        only=('nombre', 'fecha_entrenamiento', 'id_usuario', 'estado')
      ).load(self.data)
      print(posted_entrenamiento)
      
      if not self.verificar_datos(posted_entrenamiento["nombre"]):
         raise InvalidNombreError
      
      entrenamiento = Entrenamiento(**posted_entrenamiento)
      session = Session()
      
      if self.entrenamiento_exist(session, self.data['nombre']):
        session.close()
        raise EntrenamientoAlreadyExists()

      session.add(entrenamiento)
      session.commit()

      dynamodb_entrenamiento.insert_item(entrenamiento)

      new_entrenamiento = EntrenamientoSchema().dump(entrenamiento)
      session.close()

      return new_entrenamiento
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def entrenamiento_exist(self, session, nombre):
    return len(session.query(Entrenamiento).filter_by(nombre=nombre).all()) > 0
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False