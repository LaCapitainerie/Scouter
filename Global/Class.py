from datetime import datetime
from uuid import UUID

from Perimeters.Class import Perimetre

class Client(dict):
    id: UUID = "2345678-1234-1234-1234-123456789abc" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    services: list[Perimetre] = []
    technologies: list = []
    scopes: list[Perimetre] = []

    def __init__(self, values: dict):
        self.update(values)

class ClientNotFound(Exception):
    pass

class Data(dict):
    ...