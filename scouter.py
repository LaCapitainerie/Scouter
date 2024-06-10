import time
import requests
import pandas as pd
import json


TECHNOS_INTERNES_ENRÔLEES = "4b3228c4-b02f-43c2-85e2-b7d7db9650c9"



        

def main():
    Session = requests.Session()

    with open('const.json') as f:
        d = json.load(f)
        c = d["cookie"]
        if c["value"] == "" or c["startedat"] + c["timestamp"] < time.time():
            print("Cookie expired")

            account = {
                "email": "admin@me.com",
                "password": "admin"
            }

            Session.get(
                url="https://preprod.scouter.inn.hts-expert.com/api/user/current"
            )

            login = Session.post(
                url="https://preprod.scouter.inn.hts-expert.com/api/login",
                json=account,
            )

            if login.status_code == 200:
                print("Login successful")
                c["value"] = login.cookies.get_dict().get("adonis-session")
                c["startedat"] = time.time()
                c["timestamp"] = 7200
                with open('const.json', 'w') as f:
                    json.dump(d, f)
            else:
                print("Login failed")
                return
        else:
            print("Cookie is still valid")
            Session.cookies.set("adonis-session", c["value"])

    df = pd.read_csv("devices 1.csv", sep=";")

    def add_asset(name: str, description: str, scope: str):
        URL = "https://preprod.scouter.inn.hts-expert.com/api/api/asset"
        
        PAYLOAD = {
            "name": name,
            "description": description,
            "scope": scope
        }

        response = Session.post(URL, json=PAYLOAD)

        return response
    
    for _index, row in df[df.Domain.isin(["cnpp.fr"])].iloc[:5].iterrows():
        Device_Name = row["Device Name"]
        description = ""
        print(Device_Name, description, TECHNOS_INTERNES_ENRÔLEES)
        # add_asset(name, description, scope)
    
    #r = add_asset("p24-21577-6virt", "", TECHNOS_INTERNES_ENRÔLEES)
    #print(r.text)


if __name__ == '__main__':
    main()