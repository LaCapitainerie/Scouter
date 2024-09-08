from typing import Union

from requests import Session
from Global.Class import Data
from Perimeters.Class import Perimeter
from Pipeline.Pipeline import Mode


def get_perimeter(client:str, name:str, data:Data, nolog:bool) -> tuple[int, Union[Perimeter, None]]: ...
""" Get the perimeters from the Scouter platform"""

def add_perimeter(session:Session, client:str, name:str, data:Data, mode:Mode, nolog:bool) -> tuple[int, Union[Perimeter, None]]: ...
"""Add a perimeter to the Scouter platform"""

def delete_perimeter(session:Session, client: str, name:str, data:Data, mode:Mode, nolog:bool, force:bool=False) -> tuple[int, Union[Perimeter, None]]: ...
"""Delete the perimeter from the Scouter platform"""