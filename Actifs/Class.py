from datetime import datetime
from uuid import UUID


class Actif(dict):
    name: str
    description: str
    scopeId: UUID
    createdAt: datetime
    updatedAt: datetime
    id: UUID

    def __init__(self, values: dict):
        self.update(values)