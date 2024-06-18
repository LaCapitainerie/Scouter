from typing import Union

from requests import Session
from Assets.Class import Asset
from Pipeline.Pipeline import Mode
from Technos.Class import Techno

TECHNOS_API = "https://preprod.scouter.inn.hts-expert.com/api/technology"

def get_techno(asset: Asset, name:str) -> tuple[int, Union[Techno, None]]:
    """
    Get a techno from an asset
    
    Args:
        asset (Asset): The asset object
        name (str): The techno name
        
    Returns:
        tuple[int, Union[Techno, None]]: The response code and the techno object
    """
    for techno in asset.get("technologies", []):
        if techno["product"] == name:
            return 1, techno

    return 2, None

def add_techno(session:Session, asset: Asset, name:str, description:str, vendor:str, version:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:
    """
    Add a techno to the Scouter platform
    
    Args:
        session (Session): The session object
        asset (Asset): The asset object
        name (str): The techno name
        description (str): The techno description
        vendor (str): The techno vendor
        version (str): The techno version
        mode (Mode): The mode
        nolog (bool): The nolog flag
        
    Returns:
        tuple[int, Union[Techno, None]]: The response code and the techno object
    """

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

def add_mass_technos(session:Session, asset: Asset, technos: list[dict], mode:Mode, nolog:bool) -> tuple[int, tuple[int, int]]:
    """
    Add a list of technos to the Scouter platform

    Args:
        session (Session): The session object
        asset (Asset): The asset object
        technos (list[dict]): The list of technos to add

    Returns:
        tuple[int, tuple[int, int]]: The response code and the number of added technos
    """

    added = 0
    total = len(technos)

    for techno in technos:
        r = add_techno(session, asset, **techno, mode=mode, nolog=nolog)
        if r[0] == 1:
            added += 1

    return 1, (added, total)

def delete_techno(session:Session, asset: Asset, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]:
    """
    Delete a techno from the Scouter platform
    
    Args:
        session (Session): The session object
        asset (Asset): The asset object
        name (str): The techno name
        mode (Mode): The mode
        nolog (bool): The nolog flag
        
    Returns:
        tuple[int, Union[Techno, None]]: The response code and the techno object
    """

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