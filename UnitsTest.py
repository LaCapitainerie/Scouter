from Assets.Assets import add_asset, add_mass_assets, delete_asset
from Client.Clients import get_client
from Global.Login import Login
from Global.Sync import get_data
from Perimeters.Perimeters import add_perimeter, delete_perimeter
from Pipeline.Pipeline import Mode, Pipeline, Run
from Technos.Technos import add_techno, delete_techno

def UnitsTest():

    Return = Pipeline(
        Mode.PLAN,
        False,

        Login,
        get_data,

        (get_client, {"name": "CNPP"}),

        (add_perimeter, {"name": "Test Perimetre"}),
        delete_perimeter,
        delete_perimeter,
        add_perimeter,

        (add_mass_assets, {"column": ["test1", "test2", "test3"]}),

        (add_asset, {"name": "test2", "description": "test"}),
        delete_asset,
        delete_asset,
        add_asset,


        (add_techno, {"name": "Techno test", "description": "test", "vendor": "test", "version": "test"}),
        delete_techno,
        delete_techno,
        add_techno,

        (delete_perimeter, {"force": True}),

        file="const.json"
    ).run()

    if not Return:
        return False

    Attendu = [
        Run.INFO,
        Run.STAY,
        Run.WARNING,
        Run.WARNING,
        Run.STAY,
        Run.INFO,
        "\t",
        Run.STAY,
        Run.REMOVED,
        Run.WARNING,
        Run.ADDED,
        Run.ADDED,
        Run.WARNING,
        Run.WARNING,
        Run.ADDED,
        Run.WARNING
    ]

    return (Return != Attendu)


UnitsTest()

