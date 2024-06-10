import json
import time
import requests
from os import walk
import difflib



def Sync(session:requests.Session, force=False, file="const.json"):

    try:
        with open(file, "r") as f:
            d = json.load(f)

            if force or d["lastSync"] < time.time() - 3600:
                print("Syncing...")
                d["lastSync"] = time.time()

                r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

                if r.status_code == 200:
                    print("Sync successful")
                    d["Voc"] = [{i["name"]: i} for i in r.json()]
                    with open(file, 'w') as f:
                        print(d)
                        json.dump(d, f)
                else:
                    print("Sync failed")
                    return True

            else:
                print("Syncing not needed")

            return False
    except FileNotFoundError:
        filenames = next(walk("."), (None, None, []))[2] 
        print(f"File not found. Did you mean to write \033[1m{difflib.get_close_matches(file, filenames)[0]}\033[0m ?")
        return True