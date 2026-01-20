import requests # permet d'utiliser des API 
import json
import matplotlib.pyplot as plt # permet al creation de graphique 
import numpy as np


class Pokemon():
    def __init__(self,nom = "",id  = ""):
        
        self.nom = nom
        self.id = id

        pass

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/type/{id}/")

Charizard = Pokemon(35)



import requests

class Pokemon:
    def __init__(self, nom="", id=None):
        self.nom = nom
        self.id = id

    def get_id(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["id"]

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return [t["type"]["name"] for t in data["types"]]

    def graphique()

Charizard = Pokemon(id=6)

print(Charizard.get_id())
print(Charizard.get_type())
