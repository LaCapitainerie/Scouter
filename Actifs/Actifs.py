from typing import Sequence, Union
from requests import Session

from Actifs.Class import Actif
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode

API = "https://preprod.scouter.inn.hts-expert.com/api/"

def get_actif(perimeter:Perimeter, name:str) -> Union[Actif, None]:
    """
    Get the actifs from the Scouter platform

    Args:
        session (Session): The session object
        scope_id (str): The scope id

    Returns:
        Response: The response object
    """

    for actif in perimeter.get("actifs", []):
        if actif["name"] == name:
            return Actif(actif)
        
    return None
    


def add_actif(session:Session, perimeter: Perimeter, name: str, description: str, mode:Mode, nolog:bool) -> bool:
    """
    Add an actif to the Scouter platform

    Args:
        session (Session): The session object
        name (str): The name of the actif
        description (str): The description of the actif
        scope (str): The scope of the actif

    Returns:
        Response: The response object
    """

    
    PAYLOAD:Actif = {
        "name": name,
        "description": description,
        "scopeId": perimeter["id"]
    }  # type: ignore

    if get_actif(perimeter, name):
        if not nolog:print(f"Actif \033[1m{name}\033[0m already exists")
        return False

    if mode == Mode.PLAN:
        if not nolog:print(f"Actif \033[1m{name}\033[0m would have been added")
        return True
    
    response = session.post(API+"actif", json=PAYLOAD)

    if response.status_code == 200:
        if not nolog:print(f"Actif \033[1m{name}\033[0m added with id \033[1m{response.json()['id']}\033[0m")
        return True
    
    else:
        if not nolog:print("Actif addition \033[1mfailed\033[0m")
        return False



def add_mass_actifs(session:Session, scope:Perimeter, ams_df:Sequence, mode:Mode, nolog:bool) -> tuple[int, int]:
    """
    Add multiple actifs to the Scouter platform

    Args:
        session (Session): The session object
        ams_df (DataFrame): The list of actifs
        scope (str): The scope of the actif

    Returns:
        Response: The response object
    """

    AlreadyAdded = 0

    for _, row in ams_df:
        if not (_ := add_actif(session, scope, row["Device Name"], ".", nolog=True, mode=mode)):
            AlreadyAdded += 1

    if not nolog:print(f"\033[1m{len(ams_df) - AlreadyAdded}\033[0m actifs added, \033[1m{AlreadyAdded}\033[0m already existed")

    return AlreadyAdded, len(ams_df)



def delete_actif(session:Session, perimeter:Perimeter, name:str, mode:Mode, nolog:bool) -> bool:
    """
    Delete an actif from the Scouter platform

    Args:
        session (Session): The session object
        actif_id (str): The actif id

    Returns:
        Response: The response object
    """

    if not (actif := get_actif(perimeter, name)):
        if not nolog:print(f"Actif {name} not found")
        return False
    
    if mode == Mode.PLAN:
        if not nolog:print(f"Actif {actif['id']} would have been deleted")
        return True

    response = session.delete(f"{API}actif/{actif['id']}")

    if response.status_code == 200:
        if not nolog:print(f"Actif {actif['id']} deleted")
        return True
    else:
        if not nolog:print("Actif deletion failed")
        return False