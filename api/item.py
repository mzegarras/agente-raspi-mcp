from pydantic import BaseModel
from enum import Enum

# A basic string-valued Enum
class Accion(str, Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

class DoorRequest(BaseModel):
    houseId: str
    doorId: str
    accion: Accion