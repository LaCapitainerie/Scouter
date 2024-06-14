

from typing import Union
from requests import Session

from Global.Class import Client
from Perimeters.Class import Perimetre

def add_perimeter(session:Session, client:str, perimeter_name:str) -> bool:
    """
    Add a perimeter to the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        perimeter_name (str): The perimeter name
        
    Returns:
        Perimeter: The perimeter
    """
    r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

    if r.status_code != 200:
        print("\033[1mFailed\033[0m to get the perimeters")
        return False

    Clients:list[Client] = r.json()

    client_found = next(each for each in Clients if client == each["name"])

    r = session.post(f"https://preprod.scouter.inn.hts-expert.com/api/scope", json={
        "name": perimeter_name,
        "clientId": client_found["id"]
    })

    if r.status_code != 200:
        print("\033[1mFailed\033[0m to add the perimeter")
        return False

    perimeter = Perimetre(r.json())

    print(f"Perimeter \033[1m{perimeter['name']}\033[0m added")

    return True

def get_perimeter(session:Session, client:str, perimeter_name:str) -> Union[Perimetre, None]:
    """
    Get the perimeters from the Scouter platform
    
    Args:
        session (Session): The session object
        client (str): The client name
        
    Returns:
        list[Scope]: The perimeters
    """
    r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

    if r.status_code != 200:
        print("\033[1mFailed\033[0m to get the perimeters")
        return None

    Clients:list[Client] = r.json()

    client_found = next(each for each in Clients if client == each["name"])

    perimeters = next(Perimetre(each) for each in client_found["scopes"] if perimeter_name == each["name"])

    return perimeters

def delete_perimeter(session:Session, perimeter:Perimetre) -> bool:
    """
    Delete the perimeter from the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (str): The perimeter name
        
    Returns:
        bool: Is the deletion successful
    """
    try:

        r = session.delete(f"https://preprod.scouter.inn.hts-expert.com/api/scope/{perimeter['id']}")

        if r.status_code != 200:
            print("\033[1mFailed\033[0m to delete the perimeter")
            return False
        
        print(f"Perimeter \033[1m{perimeter['name']}\033[0m deleted")

        return True
    
    except StopIteration:
        print(f"Perimeter \033[1m{perimeter['name']}\033[0m not found")
        return False