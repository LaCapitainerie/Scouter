from datetime import datetime
from uuid import UUID

from Assets.Class import Asset


class Perimeter(dict):
    id: UUID = "2345678-1234-1234-1234-123456789abc" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    assets: list[Asset] = []

    def __init__(self, values: dict):
        self.update(values)