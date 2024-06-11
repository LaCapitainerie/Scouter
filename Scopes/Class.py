from datetime import datetime
from typing import NamedTuple
from uuid import UUID

from Assets.Class import Asset


class Perimetre(dict):
    id: UUID = "2345678-1234-1234-1234-123456789abc" # type: ignore
    name: str = ""
    companyName: str = ""
    isActive: bool = False
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

    def __init__(self, values: dict):
        self.update(values)

TupleAsset = NamedTuple('Asset', [
    ('id', UUID),
    ('name', str),
    ('description', str),
    ('ip', str),
    ('hostname', str),
    ('url', str),
    ('scopeId', UUID),
    ('createdAt', datetime),
    ('updatedAt', datetime)
])

class Scope(dict):
    id: UUID
    name: str
    clientId: UUID
    createdAt: datetime
    updatedAt: datetime
    client: Perimetre
    #__assets: set[TupleAsset]
    __assets: set[tuple[str, str]]

    def __init__(self, values: dict):
        self.update(values)
        #for each in values.get("assets", []):del each["technologies"]
        #self.__assets = set(map(lambda x:TupleAsset(**x), values.get("assets", [])))
        self.__assets = set(map(lambda x: (x["name"], x["description"]), values.get("assets", [])))

    def __contains__(self, key: Asset) -> bool:
        #return TupleAsset(**key, id="", ip="", hostname="", url="", createdAt="", updatedAt="") in self.__assets # type: ignore)
        return (key["name"], key["description"]) in self.__assets