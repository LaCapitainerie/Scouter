import pandas as pd
from requests import get
from Assets.Assets import add_asset, add_mass_assets
from Global.Login import Login
from Perimeters.Perimeters import add_perimeter, delete_perimeter, get_perimeter
from Pipeline.Pipeline import Pipeline
from Global.Sync import get_data


def main():


    # Devices = pd.read_csv("devices 1.csv", sep=";")

    TIE = "Technos Internes Enrôlées"

    Pipeline(
        Login,
        get_data,
        #(get_state, {"client": "CNPP", "perimeter": "Technos Internes Enrôlées", "name": "test"}),
        #(add_perimeter, {"client": "CNPP", "name": "test"}),
        #(delete_perimeter, {"client": "CNPP", "name": "test"}),
        #get_perimeter,
        #add_scope,


        file="const.json",

        #ams_df=Devices[Devices.Domain.isin(["cnpp.fr"])],
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




    print("Done")


if __name__ == '__main__':
    main()