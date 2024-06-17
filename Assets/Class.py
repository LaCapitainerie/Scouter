from datetime import datetime
from uuid import UUID

from Technos.Class import Techno


class Asset(dict):
    name: str = ""
    description: str = ""
    scopeId: UUID = "" # type: ignore
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    id: UUID = "" # type: ignore
    technologies: list[Techno] = []

    def __init__(self, values: dict):
        self.update(values)