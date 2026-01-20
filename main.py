import requests # permet d'utiliser des API 
import json
import matplotlib.pyplot as plt # permet al creation de graphique 
import numpy as np


class Pokemon:
    def __init__(self, nom="", id=None):
        self.nom = nom
        self.id = id

    def get_id(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.nom.lower()}")
        data = r.json()
        return data["id"]
    
    def get_nom(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["name"]

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return [t["type"]["name"] for t in data["types"]]

class Pokedex():
    def __init__(self,nom = ""):
        
        self.nom = nom
        
        pass
    
    def creer_pokedex(self):
        pokedex = []
        return pokedex

    def creative_pokedex(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/")
        data = r.json()
        pokedex_lst = []
        for pok in range(1,1351):
            pokemon = Pokemon(nom = "", id = pok)
            pokedex_lst.append(pokemon)
        return pokedex_lst
    
    def ajouter_pokemon(self,pokemon):
        self.


    pass


cheat = Pokedex("Pokedex cheaté ! ")
cheat = cheat.creative_pokedex()
print(cheat[6].get_type())
Charizard = Pokemon(nom = "Charizard")
Charizard.get_id()
#print(Charizard.get_type())
