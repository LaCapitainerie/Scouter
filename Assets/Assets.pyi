from collections.abc import Iterable, Sequence
from typing import Any, Union

from requests import Session
from Assets.Class import Asset
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode


def get_asset(perimeter:Perimeter, name:str) -> tuple[int, Union[Asset, None]]: ...
"""Get the assets from the Scouter platform"""

def add_asset(session:Session, perimeter: Perimeter, name: str, description: str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]: ...
"""Add an asset to the Scouter platform"""

def add_mass_assets(session:Session, perimeter:Perimeter, column:Sequence[Any], mode:Mode, nolog:bool) -> tuple[int, tuple[int, Iterable[Asset], int]]: ...
"""Add multiple assets in one take to the Scouter platform"""

def delete_asset(session:Session, perimeter:Perimeter, name:str, mode:Mode, nolog:bool) -> tuple[int, Union[Asset, None]]: ...
"""Delete an asset from the Scouter platform"""