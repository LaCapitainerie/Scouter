import pandas as pd
from Assets.Assets import add_mass_assets
from Global.Login import Login
from Pipeline.Pipeline import Pipeline
from Scopes.Class import Scope
from Scopes.Scopes import get_scope
from Global.Sync import Sync


def main():


    Devices = pd.read_csv("devices 1.csv", sep=";")


    #Pipeline(
    #    Login,
    #    Sync,
    #    get_scope,
    #    add_mass_assets,
    #    
    #    file="const.json", 
    #    perimetre="CNPP", 
    #    scopeName="Technos Internes Enrôlées",
    #    ams_df=Devices[Devices.Domain.isin(["cnpp.fr"])],
    #).run()


    if not(Session := Login()):
        return
    

    if not Sync(session=Session, force=True, file="const.json"):
        return


    if not(scope := get_scope(Session, "CNPP", "Technos Internes Enrôlées")):
        return


    if add_mass_assets(Session, Devices[Devices.Domain.isin(["cnpp.fr"])], scope):
        return




    print("Done")


if __name__ == '__main__':
    main()