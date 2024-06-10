import pandas as pd
from Login import Login
from Scopes import add_asset, get_scopes
from Sync import Sync


TECHNOS_INTERNES_ENRÔLEES = "4b3228c4-b02f-43c2-85e2-b7d7db9650c9"


def main():
    
    if not(Session := Login()):
        return
    

    if Sync(session=Session, force=False, file="const.json"):
        return
    


    Devices = pd.read_csv("devices 1.csv", sep=";")
    currentTechnos = pd.read_json("const.json")["Voc"]


    scope_id = get_scopes(Session, currentTechnos, "CNPP", "TECHNOS_INTERNES_ENRÔLEES")

    for _, row in Devices[Devices.Domain.isin(["cnpp.fr"])].iloc[:1].iterrows():
        add_asset(Session, row["Device Name"], "", scope_id)


if __name__ == '__main__':
    main()