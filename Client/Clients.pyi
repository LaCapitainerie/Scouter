from typing import Union
from Global.Class import Data


def get_client(name:str, data:Data) -> tuple[int, Union[str, None]]: ...
"""Get a client ref from the Scouter platform"""