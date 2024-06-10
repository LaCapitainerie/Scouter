from datetime import datetime
from typing import Union
from uuid import UUID


class Client(dict):
    id: UUID = "2345678-1234-1234-1234-123456789abc" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

    def __init__(self, values: dict):
        self.update(values)

class Scope(dict):
    id: UUID
    name: str
    clientId: UUID
    createdAt: datetime
    updatedAt: datetime
    client: Client
    assets: list['Asset']

    def __init__(self, values: dict):
        self.update(values)

class Asset(dict):
    name: str
    description: str
    scopeId: UUID
    createdAt: datetime
    updatedAt: datetime
    id: UUID

    def __init__(self, values: dict):
        self.update(values)