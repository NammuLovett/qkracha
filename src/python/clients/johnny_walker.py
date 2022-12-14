from os import getenv
from random import choice

import requests


walterone_host = getenv("WALTERONE_HOST", "http://192.168.1.55:8000")
walterone_username = getenv("WALTERONE_USERNAME", "qkracha")
walterone_password = getenv("WALTERONE_PASSWORD", "LosCucarachas")
walterone_match = getenv("WALTERONE_MATCH", "2")

auth = (walterone_username, walterone_password)

move_endpoint = f"{walterone_host}/moves/"
find_endpoint = f"{walterone_host}/finds/?match={walterone_match}"
attack_endpoint = f"{walterone_host}/attacks/"


def attack(ias):
    if ias:
        data = {
            "match": walterone_match,
            "attack_to": choice(ias)
        }
        response = requests.post(attack_endpoint, auth=auth, data=data)
        if response.status_code == 400:
            print(response.content)
        print(response.json())


def find_zone():
    response_find = requests.get(find_endpoint, auth=auth)
    find_data = response_find.json()
    attack(find_data['ias'])
    print(find_data)
    return find_data['neighbours_zones']


def move_to_zone():
    data = {
        "match": walterone_match,
        "to_zone": choice(find_zone())
    }
    response = requests.post(move_endpoint, auth=auth, data=data)
    print(response.json())
    return response.status_code


while move_to_zone() in [201, 400]:
    pass
