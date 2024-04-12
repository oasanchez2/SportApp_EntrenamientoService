from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Ejercicio:
    estado: bool
    id_ejercicio: str
    nombre: str
    url_imagen: str
    numero_repeticiones: int

@dataclass
class Entrenamiento:
    id_entrenamiento: str
    nombre: str
    fecha_entrenamiento: datetime
    id_usuario: str
    estado: bool
    ejercicios: List[Ejercicio]
