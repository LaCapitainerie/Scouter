from typing import Union

from Client.Class import Client
from Global.Class import Data


CLIENT_API = "https://preprod.scouter.inn.hts-expert.com/api/client/service/voc"

def get_client(name:str, data:Data) -> tuple[int, Union[str, None]]:
    """
    Get the client from the Scouter platform

    Args:
        name (str): The client name

    Returns:
        Response: The response object
    """
    
    for key in data.keys():
        if key == name:
            return 1, key
    
    return 2, None