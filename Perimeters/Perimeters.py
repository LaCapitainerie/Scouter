

from requests import Session

from Global.Class import Client
from Scopes.Class import Scope


def delete_perimeter(session:Session, client:str, perimeter:str) -> bool:
    """
    Delete the perimeter from the Scouter platform
    
    Args:
        session (Session): The session object
        perimeter (str): The perimeter name
        
    Returns:
        bool: Is the deletion successful
    """
    try:

        r = session.get("https://preprod.scouter.inn.hts-expert.com/api/client/service/voc")

        if r.status_code != 200:
            print("\033[1mFailed\033[0m to get the perimeters")
            return False

        Clients:list[Client] = r.json()

        client_found = next(each for each in Clients if client == each["name"])

        perimeter_found:Scope = next(each for each in client_found["scopes"] if perimeter == each["name"])

        r = session.delete(f"https://preprod.scouter.inn.hts-expert.com/api/scope/{perimeter_found['id']}")

        if r.status_code != 200:
            print("\033[1mFailed\033[0m to delete the perimeter")
            return False
        
        print(f"Perimeter \033[1m{perimeter}\033[0m deleted")

        return True
    
    except StopIteration:
        print(f"Perimeter \033[1m{perimeter}\033[0m not found")
        return False