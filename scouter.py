from cv2 import add
import pandas as pd
from Assets.Assets import add_asset, add_mass_assets, delete_asset, get_asset
from Client.Clients import get_client
from Technos.Technos import add_techno, delete_techno
from Global.Login import Login
from Perimeters.Perimeters import add_perimeter, delete_perimeter, get_perimeter
from Pipeline.Pipeline import Mode, Pipeline
from Global.Sync import get_data


def main():

    Devices = pd.read_csv("devices 1.csv", sep=";")

    Loop = Devices[Devices.Domain.isin(["cnpp.fr"])]["Device Name"].iloc[:5].values

    Pipeline(
        Mode.EXECUTE,
        True,
        Login,
        get_data,

        (get_client, {"name": "CNPP"}),

        (add_perimeter, {"client": "CNPP", "name": "Test Perimetre"}),
        (add_mass_assets, {"ams_df": Loop}),

        file="const.json",
        #ams_df=Devices[Devices.Domain.isin(["cnpp.fr"])],
        #ams_df[ams_df.Domain.isin(["cnpp.fr"])].iterrows()
    ).run()

    """
    (add_perimeter, {"client": "CNPP", "name": "Test Perimetre"}),
    delete_perimeter,
    delete_perimeter,
    add_perimeter,


    (add_asset, {"name": "test2", "description": "test"}),
    delete_asset,
    delete_asset,
    add_asset,


    (add_techno, {"name": "Techno test", "description": "test", "vendor": "test", "version": "test"}),
    delete_techno,
    delete_techno,
    add_techno,
    """

if __name__ == '__main__':
    main()