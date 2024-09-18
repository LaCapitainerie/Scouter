from json import load, dump
from time import time
from typing import Union
from requests import Session as SessionType

from Global.Class import URL


def Login(file:str="const.json", nolog:bool=False) -> Union[SessionType, None]:
    """
    Login to the Scouter platform
    
    Args:
        file (str): The file to login with
        
    Returns:
        Session: The session object
    """


    with open(file, "r") as f:
        d = load(f)
        Session = SessionType()

        if d["account"]["lastSync"] < time() - 3600:

            if not nolog:print("Logging in...")

            account = {
                "email": "admin@me.com",
                "password": "admin"
            }

            Session.get(
                url=f"{URL}/api/user/current"
            )

            login = Session.post(
                url=f"{URL}/api/login",
                json=account,
            )
            if login.status_code == 200:
                d["account"]["lastSync"] = time()
                with open(file, 'w+') as f:
                    dump(d, f)
                if not nolog:print("Login \033[1msuccessful\033[0m")
                return Session
            
            else:
                if not nolog:print("Login \033[1mfailed\033[0m")
                return None
            
        else:

            if not nolog:print("Login not needed")

            Session.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Cookie": d["account"]["adonis-session"]
            })

            return Session





    

    