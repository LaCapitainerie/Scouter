from typing import Union
from Scopes.Class import Asset, Scope


def get_scope(dataframe:list[dict[str, Scope]], perimetre:str, scopeName:str) -> Union[Scope, None]:
    """
    Get the asset from the Scouter platform
    
    Args:
        session (Session): The session object
        dataframe (Series): The dataframe object
        perimetre (str): The perimetre
        scopeName (str): The asset name
        
    Returns:
        Asset: The asset object
    """
    try:
        scope = tuple(next(each for each in dataframe if perimetre in each.keys()).values())[0]
        
        scopesList:list[Scope] = scope["scopes"]

        assets:Scope = Scope(next(filter(lambda x: scopeName == x["name"], scopesList)))

        return assets
    
    except StopIteration:
        print(f"Scope {scopeName} not found")
        return None


