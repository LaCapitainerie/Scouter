from datetime import datetime
from uuid import UUID


class Perimeter(dict):
    id: UUID = "2345678-1234-1234-1234-123456789abc" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

    def __init__(self, values: dict):
        self.update(values)