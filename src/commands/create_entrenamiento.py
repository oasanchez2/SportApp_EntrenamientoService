import uuid
from .base_command import BaseCommannd
#from ..models.entrenamiento import Entrenamiento
from ..models.entrenamiento import Entrenamiento, Ejercicio
from ..errors.errors import IncompleteParams, InvalidNombreError, EntrenamientoAlreadyExists
from .. import dynamodb_entrenamiento

class CreateEntrenamiento(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      
      posted_entrenamiento = Entrenamiento(str(uuid.uuid4()),self.data['nombre'], self.data['fecha_entrenamiento'], 
                                           self.data['id_usuario'], self.data['estado'],[])
      # Agregar ejercicios al entrenamiento
      for ejercicio_data in self.data.get('ejercicios', []):
          ejercicio = Ejercicio(
              estado=ejercicio_data['estado'],
              id_ejercicio=ejercicio_data['id_ejercicio'],
              nombre=ejercicio_data['nombre'],
              url_imagen=ejercicio_data['url_imagen'],
              numero_repeticiones=ejercicio_data['numero_repeticiones']
          )
          posted_entrenamiento.ejercicios.append(ejercicio)
      #posted_entrenamiento = Entrenamiento(**self.data)
      print(posted_entrenamiento)
      
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNombreError
      
      if self.entrenamiento_exist(self.data['nombre']):
        raise EntrenamientoAlreadyExists()

      dynamodb_entrenamiento.insert_item(posted_entrenamiento)

      return posted_entrenamiento
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def entrenamiento_exist(self, nombre):
    result = dynamodb_entrenamiento.get_Item_nombre(nombre)
    if result is None:
      return False
    else:
      return True
      
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False