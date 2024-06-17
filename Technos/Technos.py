from typing import Union

from requests import Session
from Assets.Class import Asset
from Pipeline.Pipeline import Mode
from Technos.Class import Techno

TECHNOS_API = "https://preprod.scouter.inn.hts-expert.com/api/technology"

def get_techno(asset: Asset, name:str) -> tuple[int, Union[Techno, None]]:

    for techno in asset['technologies']:
        if techno["product"] == name:
            return 1, techno

    return 2, None

def add_techno(session:Session, asset: Asset, name:str, description:str, vendor:str, version:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:

    if (techno := get_techno(asset, name)[1]):
        if not nolog:print(f"Techno \033[1m{name}\033[0m already exists")
        return 0, techno
    
    PAYLOAD:Techno = {
        "assetId": asset["id"],
        "description": description,
        "product": name,
        "type": "a", # o / h / a
        "vendor": vendor,
        "version": version,
    } # type: ignore

    if mode == Mode.PLAN:
        if not nolog:print(f"Techno \033[1m{name}\033[0m would have been added to asset \033[1m{asset['name']}\033[0m")
        return 1, Techno(PAYLOAD)

    response = session.post(TECHNOS_API, json=PAYLOAD)

    if response.status_code == 200:
        techno = Techno(response.json())
        if not nolog:print(f"Techno \033[1m{name}\033[0m added to asset \033[1m{asset['name']}\033[0m")
        return 1, techno
    
    if not nolog:print(f"Techno \033[1m{name}\033[0m could not be added to asset \033[1m{asset['name']}\033[0m")
    return 2, techno

def delete_techno(session:Session, asset: Asset, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:
    
    if not (techno := get_techno(asset, name)[1]):
        if not nolog:print(f"Techno \033[1m{name}\033[0m not found")
        return 2, None
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Techno \033[1m{name}\033[0m would have been deleted")
        return 1, techno

    r = session.delete(f"{TECHNOS_API}/{techno['id']}")

    if r.status_code != 200:
        if not nolog:print("\033[1mFailed\033[0m to delete the techno")
        return 2, None
    
    if not nolog:print(f"Techno \033[1m{techno['name']}\033[0m deleted")

    return 1, techno