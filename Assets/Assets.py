from collections import deque
from typing import Any, Iterable, Sequence, Union
from requests import Session

from Assets.Class import Asset
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode

API = "https://preprod.scouter.inn.hts-expert.com/api/"

def get_asset(perimeter:Perimeter, name:str) -> tuple[int, Union[Asset, None]]:
    """
    Get the assets from the Scouter platform

    Args:
        session (Session): The session object
        scope_id (str): The scope id

    Returns:
        Response: The response object
    """
    
    for asset in perimeter.get("assets", []):
        if asset["name"] == name:
            return 1, Asset(asset)
        
    return 2, None

def add_asset(session:Session, perimeter: Perimeter, name: str, description: str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]:
    """
    Add an asset to the Scouter platform

    Args:
        session (Session): The session object
        name (str): The name of the asset
        description (str): The description of the asset
        scope (str): The scope of the asset

    Returns:
        Response: The response object
    """

    
    PAYLOAD:Asset = {
        "name": name,
        "description": description,
        "scopeId": perimeter["id"]
    }  # type: ignore

    if (asset := get_asset(perimeter, name)[1]):
        if not nolog:print(f"Asset \033[1m{name}\033[0m already exists")
        return 0, asset

    if mode == Mode.PLAN:
        if not nolog:print(f"Asset \033[1m{name}\033[0m would have been added")
        return 1, Asset({"name": name, "description": description, "id": "NoId", "technologies": []})
    
    response = session.post(API+"asset", json=PAYLOAD)

    if response.status_code == 200:
        asset = Asset(response.json())
        if not nolog:print(f"Asset \033[1m{name}\033[0m added with id \033[1m{asset['id']}\033[0m")
        return 1, asset
    
    else:
        if not nolog:print("Asset addition \033[1mfailed\033[0m")
        return 2, None

def add_mass_assets(session:Session, perimeter:Perimeter, column:Sequence[Any], mode:Mode, nolog:bool) -> tuple[int, tuple[int, Iterable[Asset], int]]:
    """
    Add multiple assets to the Scouter platform

    Args:
        session (Session): The session object
        ams_df (DataFrame): The list of assets
        scope (str): The scope of the asset

    Returns:
        Response: The response object
    """

    Already = 0
    Added = deque()
    Error = 0

    for row in column:
        Rcode, asset = add_asset(session, perimeter, row, ".", nolog=True, mode=mode)
        if Rcode == 0:
            Already += 1
            if not nolog:print(f"Asset {row} already exists")
        elif Rcode == 1:
            Added.append(asset)
            if not nolog:print(f"Asset {row} added")
        elif Rcode == 2:
            Error += 1
            if not nolog:print(f"Asset {row} addition failed")

    if not nolog:print(f"\033[1m{Added}\033[0m assets added, \033[1m{Already}\033[0m already existed, \033[1m{Error}\033[0m errors")

    return 1, (Already, Added, Error)

def delete_asset(session:Session, perimeter:Perimeter, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]:
    """
    Delete an asset from the Scouter platform

    Args:
        session (Session): The session object
        asset_id (str): The asset id

    Returns:
        Response: The response object
    """

    if not (asset := get_asset(perimeter, name)[1]):
        if not nolog:print(f"Asset {name} not found")
        return 2, None
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Asset {asset['id']} would have been deleted")
        return 1, asset

    response = session.delete(f"{API}asset/{asset['id']}")

    if response.status_code == 200:
        if not nolog:print(f"Asset {asset['id']} deleted")
        return 1, asset
    else:
        if not nolog:print("Asset deletion failed")
        return 2, None