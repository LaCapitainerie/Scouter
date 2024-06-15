

from typing import Union
from requests import Session

from Global.Class import Client, Data
from Perimeters.Class import Perimetre

PERIMETER_API = "https://preprod.scouter.inn.hts-expert.com/fr/voc/client/"

def add_perimeter(session:Session, client:str, name:str, data:Data) -> bool:
    """
    Add a perimeter to the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        name (str): The perimeter name
        
    Returns:
        Perimeter: The perimeter
    """

    if get_perimeter(client, name, data):
        print(f"Perimeter \033[1m{name}\033[0m already exists")
        return False

    if not (client_found := data.get(client)):
        print(f"\033[1mFailed\033[0m to fetch client called \033[1m{client}\033[0m when adding the perimeter {name}")
        return False

    r = session.post(f"https://preprod.scouter.inn.hts-expert.com/api/scope", json={
        "name": name,
        "clientId": client_found["id"]
    })

    if r.status_code != 200:
        print("\033[1mFailed\033[0m to add the perimeter")
        return False

    perimeter = Perimetre(r.json())

    print(f"Perimeter \033[1m{perimeter['name']}\033[0m added")

    return True

def get_perimeter(client:str, name:str, data:Data) -> Union[Perimetre, None]:
    """
    Get the perimeters from the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        
    Returns:
        list[Scope]: The perimeters
    """

    if not (client_found := data.get(client)):
        print(f"\033[1mFailed\033[0m to fetch client called \033[1m{client}\033[0m when adding the perimeter {name}")
        return None

    for perimeter in client_found["scopes"]:
        if perimeter["name"] == name:
            return perimeter

    return None

def delete_perimeter(session:Session, client: str, name:str, data:Data) -> bool:
    """
    Delete the perimeter from the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (str): The perimeter name
        
    Returns:
        bool: Is the deletion successful
    """

    # Get the perimeter to see if exist
    if not (perimeter := get_perimeter(client, name, data)):
        print(f"Perimeter \033[1m{name}\033[0m not found")
        return False

    r = session.delete(f"https://preprod.scouter.inn.hts-expert.com/api/scope/{perimeter['id']}")

    if r.status_code != 200:
        print("\033[1mFailed\033[0m to delete the perimeter")
        return False
    
    print(f"Perimeter \033[1m{perimeter['name']}\033[0m deleted")

    return True