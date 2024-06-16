import pandas as pd
from requests import get
from Assets.Assets import add_asset, add_mass_assets, get_asset
from Global.Login import Login
from Perimeters.Perimeters import add_perimeter, delete_perimeter, get_perimeter
from Pipeline.Pipeline import Mode, Pipeline
from Global.Sync import get_data


def main():


    # Devices = pd.read_csv("devices 1.csv", sep=";")

    TIE = "Technos Internes Enrôlées"

    Pipeline(
        Mode.EXECUTE,
        True,
        Login,
        get_data,
        (add_perimeter, {"client": "CNPP", "name": "Test"}),
        (add_asset, {"name": "test2", "description": "test"}),


        file="const.json",
        #ams_df=Devices[Devices.Domain.isin(["cnpp.fr"])],
        #ams_df[ams_df.Domain.isin(["cnpp.fr"])].iterrows()
    ).run()

    

    """
    if not(Session := Login()):
        return
    
    add_perimeter(Session, "CNPP", "test")
    
    if not(Peri := get_perimeters(Session, "CNPP", "test")):
        return

    delete_perimeter(Session, Peri)
    """
    

    #if not Sync(session=Session, force=True, file="const.json"):
    #    return


    #if not(scope := get_scope(Session, "CNPP", "Technos Internes Enrôlées")):
    #    return


    #if add_mass_assets(Session, Devices[Devices.Domain.isin(["cnpp.fr"])], scope):
    #    return

if __name__ == '__main__':
    main()