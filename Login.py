import requests


def Login():
    Session = requests.Session()

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
        print("Login successful")
        return Session
    else:
        print("Login failed")
        return None