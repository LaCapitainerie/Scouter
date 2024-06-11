from typing import Union

from requests import Session
from Scopes.Class import Perimetre, Scope


def get_scope(session:Session, perimetre:str, scopeName:str) -> Union[Scope, None]:
    """
    Get the asset from the Scouter platform
    
    Args:
        session (Session): The session object
        dataframe (Series): The dataframe object
        perimetre (str): The perimetre
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

        scope = next(each for each in df if perimetre in each["name"])
        
        scopesList:list[Scope] = scope["scopes"]

        assets:Scope = Scope(next(filter(lambda x: scopeName == x["name"], scopesList)))

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

        perimetre_found = next(each for each in df if scopeName in each["name"])
        
        r = session.delete(f"https://preprod.scouter.inn.hts-expert.com/scope/{perimetre_found['id']}")
        
        if r.status_code == 200:
            print("Perimeter \033[1mdeleted")
            return True
        else:
            print("Perimeter deletion \033[1mfailed")
            return False
    
    except StopIteration:
        print(f"Perimeter \033[1m{scopeName} not found")
        return False