import pandas as pd
from Assets.Assets import add_mass_assets
from Global.Login import Login
from Scopes.Class import Scope
from Scopes.Scopes import get_scope
from Global.Sync import Sync


def main():
    
    if not(Session := Login()):
        return
    

    if Sync(session=Session, force=True, file="const.json"):
        return
    

    Devices = pd.read_csv("devices 1.csv", sep=";")
    currentTechnos:list[dict[str, Scope]] = pd.read_json("const.json")["content"]["Voc"]


    if not(scope := get_scope(currentTechnos, "CNPP", "Technos Internes Enrôlées")):
        return


    if add_mass_assets(Session, Devices[Devices.Domain.isin(["cnpp.fr"])], scope):
        return




    print("Done")


if __name__ == '__main__':
    main()