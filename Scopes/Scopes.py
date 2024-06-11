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
            print("Failed to get the scopes")
            return None
        
        df:list[Perimetre] = r.json()

        scope = next(each for each in df if perimetre in each["name"])
        
        scopesList:list[Scope] = scope["scopes"]

        assets:Scope = Scope(next(filter(lambda x: scopeName == x["name"], scopesList)))

        print("Scope found : ", assets["name"])

        return assets
    
    except StopIteration:
        print(f"Scope {scopeName} not found")
        return None


