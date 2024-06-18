from datetime import datetime
from uuid import UUID

from Perimeters.Class import Perimeter


class Client(dict):
    id: UUID = "" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    scopes: list[Perimeter] = []
    services: list[dict] = []
    technologies: list = []
    updatedAt: datetime = datetime.now()

    def __init__(self, values: dict):
        self.update(values)

class ClientNotFound(Exception):
    pass