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
