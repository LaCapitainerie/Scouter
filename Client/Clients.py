from typing import Union

from Client.Class import Client
from Global.Class import Data


CLIENT_API = "https://preprod.scouter.inn.hts-expert.com/api/client/service/voc"

def get_client(name:str, data:Data) -> tuple[int, Union[Client, None]]:
    """
    Get the client from the Scouter platform

    Args:
        name (str): The client name

    Returns:
        Response: The response object
    """
    
    for key, client in data.items():
        if key == name:
            return 1, Client(client)
    
    return 2, None