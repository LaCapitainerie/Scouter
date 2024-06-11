from typing import Union

from requests import Session
from Scopes.Class import Perimetre, Scope

def add_scope(session:Session, perimeter:Perimetre, scopeName:str) -> Union[Scope, None]:
    """
    Add a scope to the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (Perimetre): The perimeter object
        scopeName (str): The scope name
        
    Returns:
        Scope: The scope object
    """
    try:

        r = session.post(f"https://preprod.scouter.inn.hts-expert.com/api/asset", json={
            "name": scopeName,
            "description": ".",
            "scopeId": perimeter["id"]
        })

        if r.status_code != 200:
            print("\033[1mFailed\033[0m to add the scope")
            return None

        scope = Scope(r.json())

        print(f"Scope \033[1m{scope['name']}\033[0m added")

        return scope
    
    except StopIteration:
        print(f"Perimeter \033[1m{perimeter['name']} not found")
        return None


def get_scope(session:Session, perimeter:Perimetre, scopeName:str) -> Union[Scope, None]:
    """
    Get the asset from the Scouter platform
    
    Args:
        session (Session): The session object
        dataframe (Series): The dataframe object
        perimeter (str): The perimeter
        scopeName (str): The asset name
        
    Returns:
        Asset: The asset object
    """
    try:

        r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

        if r.status_code != 200:
            print("\033[1mFailed\033[0m to get the scopes")
            return None
        
        df:list[Perimetre] = r.json()

        assets:Scope = Scope(next(filter(lambda x: scopeName == x["name"], perimeter["scopes"])))

        print("Scope found :\033[1m", assets["name"], "\033[0m")

        return assets
    
    except StopIteration:
        print(f"Scope \033[1m{scopeName}\033[0m not found")
        return None


def delete_scope(session:Session, scopeName:str) -> bool:
    """
    Delete the scope from the Scouter platform
    
    Args:
        session (Session): The session object
        scope (str): The scope name
        
    Returns:
        bool: Is the deletion successful
    """
    try:

        r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

        if r.status_code != 200:
            print("Failed to get the scopes")
            return False
        
        df:list[Perimetre] = r.json()

        perimeter_found = next(each for each in df if scopeName in each["name"])
        
        r = session.delete(f"https://preprod.scouter.inn.hts-expert.com/scope/{perimeter_found['id']}")
        
        if r.status_code == 200:
            print("Perimeter \033[1mdeleted")
            return True
        else:
            print("Perimeter deletion \033[1mfailed")
            return False
    
    except StopIteration:
        print(f"Perimeter \033[1m{scopeName} not found")
        return False