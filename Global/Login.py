import json
import time
import requests


def Login(file:str="const.json"):
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

            print("Logging in...")

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
                with open(file, 'w') as f:
                    json.dump(d, f)
                print("Login successful")
                return Session
            
            else:
                print("Login failed")
                return None
            
        else:

            print("Login not needed")

            Session.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Cookie": d["account"]["adonis-session"]
            })

            return Session





    

    