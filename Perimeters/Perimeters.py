

from typing import Union
from requests import Session

from Global.Class import Data
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode

PERIMETER_API = "https://preprod.scouter.inn.hts-expert.com/api/scope"

def add_perimeter(session:Session, client:str, name:str, data:Data, mode:Mode, nolog:bool) -> tuple[int, Union[Perimeter, None]]:
    """
    Add a perimeter to the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        name (str): The perimeter name
        
    Returns:
        Perimeter: The perimeter
    """

    if (perimeter := get_perimeter(client, name, data, nolog)[1]):
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m already exists")
        return 0, perimeter

    if not (client_found := data.get(client)):
        if not nolog:print(f"\033[1mFailed\033[0m to fetch client called \033[1m{client}\033[0m when adding the perimeter {name}")
        return 2, None
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m would have been added")
        return 1, Perimeter({"name": name, "id": "NoId", "assets": []})
    
    r = session.post(PERIMETER_API, json={
        "name": name,
        "clientId": client_found["id"]
    })

    if r.status_code != 200:
        if not nolog:print("\033[1mFailed\033[0m to add the perimeter")
        return 2, None

    perimeter = Perimeter(r.json())

    if not nolog:print(f"Perimeter \033[1m{perimeter['name']}\033[0m added")

    return 1, perimeter

def get_perimeter(client:str, name:str, data:Data, nolog:bool) -> tuple[int, Union[Perimeter, None]]:
    """
    Get the perimeters from the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        
    Returns:
        list[Scope]: The perimeters
    """

    if not (client_found := data.get(client)):
        if not nolog:print(f"\033[1mFailed\033[0m to fetch client called \033[1m{client}\033[0m when adding the perimeter {name}")
        return 2, None

    for perimeter in client_found["scopes"]:
        if perimeter["name"] == name:
            return 1, Perimeter(perimeter)

    return 2, None

def delete_perimeter(session:Session, client: str, name:str, data:Data, mode:Mode, nolog:bool) -> tuple[int, Union[Perimeter, None]]:
    """
    Delete the perimeter from the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (str): The perimeter name
        
    Returns:
        bool: Is the deletion successful
    """

    # Get the perimeter to see if exist
    if not (perimeter := get_perimeter(client, name, data, nolog)[1]):
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m not found")
        return 2, None
    
    if perimeter.assets:
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m still has assets")
        return 2, None
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m would have been deleted")
        return 1, perimeter

    r = session.delete(f"{PERIMETER_API}/{perimeter['id']}")

    if r.status_code != 200:
        if not nolog:print("\033[1mFailed\033[0m to delete the perimeter")
        return 2, None
    
    if not nolog:print(f"Perimeter \033[1m{perimeter['name']}\033[0m deleted")

    return 1, perimeter