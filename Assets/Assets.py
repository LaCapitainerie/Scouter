from typing import Union
from uuid import UUID
from pandas import DataFrame
from requests import Session

from Assets.Class import Asset
from Scopes.Class import Scope

API = "https://preprod.scouter.inn.hts-expert.com/api/"

def get_assets(session:Session, scope_id:UUID) -> Union[Asset, None]:
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
    


def add_asset(session:Session, name: str, description: str, scope: Scope, force=False, silent=False) -> bool:
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
        "scopeId": scope["id"]
    }  # type: ignore

    if not force and PAYLOAD in scope:
        if not silent:print(f"Asset \033[1m{name}\033[0m already exists")
        return False

    response = session.post(API+"asset", json=PAYLOAD)

    if response.status_code == 200:
        if not silent:print(f"Asset \033[1m{name}\033[0m added with id \033[1m{response.json()['id']}\033[0m")
        return True
    
    else:
        if not silent:print("Asset addition \033[1mfailed\033[0m")
        return False



def add_mass_assets(session:Session, ams_df:DataFrame, scope:Scope) -> bool:
    """
    Add multiple assets to the Scouter platform

    Args:
        session (Session): The session object
        ams_df (DataFrame): The list of assets
        scope (str): The scope of the asset

    Returns:
        Response: The response object
    """

    AlreadyAdded = 0

    for _, row in ams_df[ams_df.Domain.isin(["cnpp.fr"])].iterrows():
        if not (_ := add_asset(session, row["Device Name"], ".", scope, silent=True)):
            AlreadyAdded += 1

    print(f"\033[1m{len(ams_df) - AlreadyAdded}\033[0m assets added, \033[1m{AlreadyAdded}\033[0m already existed")

    return True



def delete_asset(session:Session, asset_id:str) -> bool:
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
        return True
    else:
        print("Asset deletion failed")
        return False