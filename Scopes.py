from pandas import Series
from requests import Session

def get_scopes(session:Session, dataframe:Series, perimetre:str, scope:str) -> str:

    return dataframe[perimetre][scope][lambda x: x["name"] == scope]["id"]


def add_asset(session:Session, name: str, description: str, scope: str):
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



    URL = "https://preprod.scouter.inn.hts-expert.com/api/api/asset"
    
    PAYLOAD = {
        "name": name,
        "description": description,
        "scope": scope
    }

    response = session.post(URL, json=PAYLOAD)

    return response