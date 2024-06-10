import json
import time
import requests

def Sync(session:requests.Session):

    with open('const.json', "r") as f:
        d = json.load(f)

        if d["lastSync"] < time.time() - 3600:
            print("Syncing...")
            d["lastSync"] = time.time()

            r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

            if r.status_code == 200:
                print("Sync successful")
                d["Voc"] = [{i["name"]: i} for i in r.json()]
                with open('const.json', 'w') as f:
                    print(d)
                    json.dump(d, f)
            else:
                print("Sync failed")
                return

        else:
            print("Syncing not needed")
            
        return