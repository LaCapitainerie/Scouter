import json
import time
from typing import Union
import requests


def Login(file:str="const.json", nolog:bool=False) -> Union[requests.Session, None]:
    """
    Login to the Scouter platform
    
    Args:
        file (str): The file to login with
        
    Returns:
        Session: The session object
    """


    with open(file, "r+") as f:
        d = json.load(f)
        Session = requests.Session()

        if d["account"]["lastSync"] < time.time() - 3600:

            if not nolog:print("Logging in...")

            account = {
                "email": "admin@me.com",
                "password": "admin"
            }

            Session.get(
                url="https://preprod.scouter.inn.hts-expert.com/api/user/current"
            )

            login = Session.post(
                url="https://preprod.scouter.inn.hts-expert.com/api/login",
                json=account,
            )
            if login.status_code == 200:
                d["account"]["lastSync"] = time.time()
                with open(file, 'w+') as f:
                    json.dump(d, f)
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





    

    