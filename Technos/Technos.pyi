from typing import Union

from requests import Session
from Assets.Class import Asset
from Pipeline.Pipeline import Mode
from Technos.Class import Techno


def get_techno(asset: Asset, name:str) -> tuple[int, Union[Techno, None]]: ...
""" Get the technos from the Scouter platform"""

def add_techno(session:Session, asset: Asset, name:str, description:str, vendor:str, version:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]: ...
"""Add a techno to the Scouter platform"""

def add_mass_technos(session:Session, asset: Asset, technos: list[dict], mode:Mode, nolog:bool) -> tuple[int, tuple[int, int]]: ...
"""Add a list of technos to the Scouter platform"""

def delete_techno(session:Session, asset: Asset, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Techno, None]]: ...
"""Delete the techno from the Scouter platform"""