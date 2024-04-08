from typing import Optional
from datetime import datetime

class Entrenamiento():

  def __init__(self, id_entrenamiento: str, nombre: str, fecha_entrenamiento: datetime, id_usuario: str, estado: bool):
    self.id_entrenamiento = id_entrenamiento
    self.nombre = nombre
    self.fecha_entrenamiento = fecha_entrenamiento
    self.id_usuario = id_usuario
    self.estado = estado

  def to_dict(self):
        return {
            "id_entrenamiento": self.id_entrenamiento,
            "nombre": self.nombre,
            "fecha_entrenamiento": self.fecha_entrenamiento,
            "id_usuario": self.id_usuario,
            "estado": self.estado
        }
  
