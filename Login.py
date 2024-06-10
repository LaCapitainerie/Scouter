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

    print(f"Login {'successful' if login.status_code == 200 else 'failed'}")

    return Session