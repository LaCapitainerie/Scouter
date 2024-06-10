from re import S
import requests
import pandas as pd
from Login import Login
from Sync import Sync


TECHNOS_INTERNES_ENRÔLEES = "4b3228c4-b02f-43c2-85e2-b7d7db9650c9"


def main():
    
    Session = Login()

    Sync(Session)



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
    
    #for _index, row in df[df.Domain.isin(["cnpp.fr"])].iloc[:1].iterrows():
    #    Device_Name = row["Device Name"]
    #    description = ""
    #    print(Device_Name, description, TECHNOS_INTERNES_ENRÔLEES)
        # add_asset(name, description, scope)
    
    #r = add_asset("test d'asset", "", TECHNOS_INTERNES_ENRÔLEES)
    #print(r.text)


if __name__ == '__main__':
    main()