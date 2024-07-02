from dataclasses import dataclass
from model.object import ArtObject
@dataclass
class Connessione:
    obj1: ArtObject
    obj2: ArtObject
    peso: int

