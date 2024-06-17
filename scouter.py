import pandas as pd
from Assets.Assets import add_asset, add_mass_assets, get_asset
from Technos.Technos import add_techno, delete_techno
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
        (add_techno, {"name": "Techno test", "description": "test", "vendor": "test", "version": "test"}),
        delete_techno,

        file="const.json",
        #ams_df=Devices[Devices.Domain.isin(["cnpp.fr"])],
        #ams_df[ams_df.Domain.isin(["cnpp.fr"])].iterrows()
    ).run()

if __name__ == '__main__':
    main()