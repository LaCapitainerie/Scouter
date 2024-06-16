

from typing import Union
from requests import Session

from Global.Class import Data
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode

PERIMETER_API = "https://preprod.scouter.inn.hts-expert.com/api/scope"

def add_perimeter(session:Session, client:str, name:str, data:Data, mode:Mode, nolog:bool) -> bool:
    """
    Add a perimeter to the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        name (str): The perimeter name
        
    Returns:
        Perimeter: The perimeter
    """

    if get_perimeter(client, name, data, nolog):
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m already exists")
        return False

    if not (client_found := data.get(client)):
        if not nolog:print(f"\033[1mFailed\033[0m to fetch client called \033[1m{client}\033[0m when adding the perimeter {name}")
        return False
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m would have been added")
        return True
    
    r = session.post(PERIMETER_API, json={
        "name": name,
        "clientId": client_found["id"]
    })

    if r.status_code != 200:
        if not nolog:print("\033[1mFailed\033[0m to add the perimeter")
        return False

    perimeter = Perimeter(r.json())

    if not nolog:print(f"Perimeter \033[1m{perimeter['name']}\033[0m added")

    return True

def get_perimeter(client:str, name:str, data:Data, nolog:bool) -> Union[Perimeter, None]:
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
        return None

    for perimeter in client_found["scopes"]:
        if perimeter["name"] == name:
            return Perimeter(perimeter)

    return None

def delete_perimeter(session:Session, client: str, name:str, data:Data, mode:Mode, nolog:bool) -> bool:
    """
    Delete the perimeter from the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (str): The perimeter name
        
    Returns:
        bool: Is the deletion successful
    """

    # Get the perimeter to see if exist
    if not (perimeter := get_perimeter(client, name, data, nolog)):
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m not found")
        return False
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Perimeter \033[1m{name}\033[0m would have been deleted")
        return True

    r = session.delete(f"{PERIMETER_API}/{perimeter['id']}")

    if r.status_code != 200:
        if not nolog:print("\033[1mFailed\033[0m to delete the perimeter")
        return False
    
    if not nolog:print(f"Perimeter \033[1m{perimeter['name']}\033[0m deleted")

    return True