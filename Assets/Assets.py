from uuid import UUID
from pandas import DataFrame
from requests import Session

from Scopes.Class import Scope

API = "https://preprod.scouter.inn.hts-expert.com/api/"

def get_assets(session:Session, scope_id:UUID):
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
    


def add_asset(session:Session, name: str, description: str, scope: Scope):
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

    if any(name == each["name"] for each in scope["assets"]):
        print(f"Asset {name} already exists")
        return True

    response = session.post(API+"asset", json=PAYLOAD)

    if response.status_code == 200:
        print(f"Asset {name} added with id {response.json()['id']}")
        return response
    else:
        print("Asset addition failed")
        return None



def add_mass_assets(session:Session, dataframe:DataFrame, scope:Scope):
    """
    Add multiple assets to the Scouter platform

    Args:
        session (Session): The session object
        dataframe (DataFrame): The list of assets
        scope (str): The scope of the asset

    Returns:
        Response: The response object
    """

    installedDevice = map(lambda x: x["name"], scope["assets"])

    for i, row in dataframe[dataframe.Domain.isin(["cnpp.fr"]) & (dataframe["Device Name"] not in installedDevice)].iterrows():
        if i == 3:break
        if not (_ := add_asset(session, row["Device Name"], ".", scope)):
            print(f"Asset {row['Device Name']} not added")
            return True

    return False



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