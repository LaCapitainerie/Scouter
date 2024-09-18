# Used to sync the data from the Scouter platform
from time import time
from json import load, dump
from typing import Union
from requests import Session
from os import walk
from difflib import get_close_matches

from Global.Class import URL, Data



def get_data(session:Session, file:str, mode:str, force:bool=False, nolog:bool=False) -> tuple[int, Union[Data, None]]:
    """
    Sync the data from the Scouter platform
    
    Args:
        session (Session): The session object
        force (bool): Force the sync
        file (str): The file to sync with
        
    Returns:
        bool: Is the sync failed
    """

    try:
        with open(file, "r") as f:
            d = load(f)

            if force or (d["content"]["lastSync"] < time() - 3600 and mode != "Plan"):
                if not nolog:print("Syncing...")
                d["content"]["lastSync"] = time()

                r = session.get(f"{URL}/api/client/service/voc")

                if r.status_code == 200:
                    if not nolog:print("Sync \033[1msuccessful\033[0m")
                    d["content"]["Voc"] = {i["name"]: i for i in r.json()}
                    with open(file, 'w+') as f:
                        dump(d, f)
                else:
                    if not nolog:print("Sync \033[1mfailed\033[0m")
                    return 2, None

            else:
                if not nolog:print("Syncing \033[1mnot needed\033[0m")

            return 1, d["content"]["Voc"]

    except FileNotFoundError:
        filenames = next(walk("."), (None, None, []))[2] 
        print(f"File \033[1m{file}\033[0m not found. Did you mean to write \033[1m{get_close_matches(file, filenames)[0]}\033[0m ?")
        return 2, None