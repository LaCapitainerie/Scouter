import pandas as pd
from Login import Login
from Scopes.Class import Scope
from Scopes.Scopes import add_asset, delete_asset, get_assets, get_scopes
from Sync import Sync


TECHNOS_INTERNES_ENRÔLEES = "4b3228c4-b02f-43c2-85e2-b7d7db9650c9"


def main():
    
    if not(Session := Login()):
        return
    

    if Sync(session=Session, force=False, file="const.json"):
        return
    

    Devices = pd.read_csv("devices 1.csv", sep=";")
    currentTechnos:list[dict[str, Scope]] = pd.read_json("const.json")["content"]["Voc"]


    scope_id = get_scopes(currentTechnos, "CNPP", "Technos Internes Enrôlées")["id"]


    for _, row in Devices[Devices.Domain.isin(["cnpp.fr"])].iloc[:1].iterrows():
        if not (_ := add_asset(Session, row["Device Name"], ".", scope_id)):
            print(f"Asset {row['Device Name']} not added")
            break


    if not(allAssets := get_assets(Session, scope_id)):
        return
    

    for asset in allAssets:
        print(asset["id"])
        #delete_asset(Session, asset["id"])

    print("Done")


if __name__ == '__main__':
    main()