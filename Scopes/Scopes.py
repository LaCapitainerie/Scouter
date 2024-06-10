from uuid import UUID
import uuid
from requests import Session

from Scopes.Class import Asset, Scope

API = "https://preprod.scouter.inn.hts-expert.com/api/"



def get_scopes(dataframe:list[dict[str, Scope]], perimetre:str, scopeName:str) -> Scope:
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
    
    scope = tuple(next(each for each in dataframe if perimetre in each.keys()).values())[0]
    
    scopesList:list[Scope] = scope["scopes"]

    assets:Scope = Scope(next(filter(lambda x: scopeName == x["name"], scopesList)))

    return assets



def get_assets(session:Session, scope_id:uuid.UUID):
    """
    Get the assets from the Scouter platform

    Args:
        session (Session): The session object
        scope_id (str): The scope id

    Returns:
        Response: The response object
    """

    response = session.get(f"https://preprod.scouter.inn.hts-expert.com/api/scope/{scope_id}")

    if response.status_code == 200:
        print(f"Assets retrieved")
        return response.json()["assets"]
    else:
        print("Assets retrieval failed")
        return None
    


def add_asset(session:Session, name: str, description: str, scope: UUID):
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

    
    PAYLOAD = {
        "name": name,
        "description": description,
        "scopeId": scope
    }

    response = session.post(API+"asset", json=PAYLOAD)

    if response.status_code == 200:
        print(f"Asset {name} added with id {response.json()['id']}")
        return response
    else:
        print("Asset addition failed")
        return None



def delete_asset(session:Session, asset_id:str):
    """
    Delete an asset from the Scouter platform

    Args:
        session (Session): The session object
        asset_id (str): The asset id

    Returns:
        Response: The response object
    """

    response = session.delete(f"{API}asset/{asset_id}")

    if response.status_code == 200:
        print(f"Asset {asset_id} deleted")
        return response
    else:
        print("Asset deletion failed")
        return None