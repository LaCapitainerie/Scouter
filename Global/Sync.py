import json
import time
import requests
from os import walk
import difflib



def Sync(session:requests.Session, file:str, force=False):
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
            d = json.load(f)

            if force or d["content"]["lastSync"] < time.time() - 3600:
                print("Syncing...")
                d["content"]["lastSync"] = time.time()

                r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

                if r.status_code == 200:
                    print("Sync successful")
                    d["content"]["Voc"] = [{i["name"]: i} for i in r.json()]
                    with open(file, 'w') as f:
                        json.dump(d, f)
                else:
                    print("Sync failed")
                    return False

            else:
                print("Syncing not needed")

            return True

    except FileNotFoundError:
        filenames = next(walk("."), (None, None, []))[2] 
        print(f"File \033[1m{file}\033[0m not found. Did you mean to write \033[1m{difflib.get_close_matches(file, filenames)[0]}\033[0m ?")
        return False