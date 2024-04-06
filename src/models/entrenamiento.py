from marshmallow import  Schema, fields
from sqlalchemy import Column, String, Boolean, DateTime,Integer
from .model import Model, Base
from datetime import datetime, timedelta

class Entrenamiento(Model, Base):
  __tablename__ = 'entrenamiento'

  nombre = Column(String)
  fecha_entrenamiento = Column(DateTime)
  id_usuario = Column(Integer)
  estado = Column(Boolean)

  def __init__(self, nombre, fecha_entrenamiento, id_usuario, estado):
    Model.__init__(self)
    self.nombre = nombre
    self.fecha_entrenamiento = fecha_entrenamiento
    self.id_usuario = id_usuario
    self.estado = estado
    
class EntrenamientoSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  fecha_entrenamiento = fields.DateTime()
  id_usuario = fields.Number()
  estado = fields.Bool()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
 

class EntrenamientoJsonSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  fecha_entrenamiento = fields.DateTime()
  id_usuario = fields.Number()
  estado = fields.Bool()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
  
  
