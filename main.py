import requests # permet d'utiliser des API 
import time
import json
import random as r
import matplotlib.pyplot as plt # permet al creation de graphique 

    


class Pokemon:
    def __init__(self, nom="", id=None):
        self.nom = nom
        self.id = id

    def __str__(self):
        try:
            types = ", ".join(self.get_type())
            faiblesses = ", ".join(self.get_faiblesse())
            taille = self.get_taille()
            poids = self.get_poids()

            return (
                f"🧬 Pokémon #{self.id}\n"
                f"Nom        : {self.nom.capitalize()}\n"
                f"Types      : {types}\n"
                f"Taille     : {taille} m\n"
                f"Poids      : {poids} kg\n"
                f"Faiblesses : {faiblesses}"
            )
        except Exception:
            return f"Pokémon(id={self.id}, nom='{self.nom}')"



    def get_id(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.nom.lower()}")
        data = r.json()
        return data["id"]
    
    def get_nom(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        if r.status_code != 200:
            return "Pokémon inconnu"
        data = r.json()
        return data["name"]

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return [t["type"]["name"] for t in data["types"]]
    
    def get_taille(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        if r.status_code != 200:
            return None
        data = r.json()
        return data["height"] / 10  # en mètres
    

    def get_poids(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        if r.status_code != 200:
            return None
        data = r.json()
        return data["weight"] / 10  # en kg


    def get_faiblesse(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        if r.status_code != 200:
            return []

        data = r.json()
        faiblesses = set()

        for t in data["types"]:
            type_name = t["type"]["name"]

            r_type = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}")
            if r_type.status_code != 200:
                continue

            type_data = r_type.json()
            for f in type_data["damage_relations"]["double_damage_from"]:
                faiblesses.add(f["name"])

        return list(faiblesses)



class Pokedex():
    def __init__(self,nom = ""):
        
        self.nom = nom
        self.pokedex = []
        
        pass
    


    def creative_pokedex(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/")
        data = r.json()
        pokedex_lst = []
        for pok in range(1,1351):
            pokemon = Pokemon(nom = "", id = pok)
            pokedex_lst.append(pokemon)
        return pokedex_lst
    
    def ajouter_pokemon(self,pokemon):
        self.pokedex.append(pokemon)

class Game():
    
    def __init__(self,pokedex):
            self.pokedex = pokedex

    def choisir_starter(self):
        starters = ["bulbasaur", "charmander", "squirtle"]

        print("Choisis ton starter :")
        for i, s in enumerate(starters, 1):
            print(f"{i}. {s.capitalize()}")

        choix = int(input("Ton choix (1-3) : "))

        nom = starters[choix - 1]

        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nom}")
        data = r.json()

        pokemon = Pokemon(
            nom=data["name"],
            id=data["id"]
        )

        self.pokedex.ajouter_pokemon(pokemon)

        print(f"\n {pokemon.nom.capitalize()} a été ajouté à ton Pokédex !")

    def afficher_pokedex(self):
        print("\n📖 Ton Pokédex :")
        for p in self.pokedex.pokedex:
            print(p)

    def aventure(self):
        for _ in range(5):
            time.sleep(2)

            if r.randint(0, 11) >= 8:
                id = r.randint(1, 1350)
                pok = Pokemon("", id)

                print(f"⚔️ Un {pok.get_nom().capitalize()} vous attaque !!")
                print("1- Capturer")
                print("2- Fuir")

                choix = int(input("> "))

                if choix == 1:
                    if r.randint(0, 4) >= 2:
                        self.pokedex.ajouter_pokemon(pok)
                        print("🎉 Pokémon capturé !")
                    else:
                        print("❌ Échec de la capture...")
                else:
                    print("🏃 Tu as fui.")
        return
    
Monpoke = Pokedex("MonPoke")


# TEST DU JEU ------------

# game = Game(Monpoke)
# game.choisir_starter()
# game.aventure()
# game.afficher_pokedex()

# ------------------------

#print(game.pokedex.pokedex)

#cheat = Pokedex("Pokedex cheaté ! ")
#cheat = cheat.creative_pokedex()
#print(cheat[6].get_type())
#Charizard = Pokemon(nom = "Charizard")
#Charizard.get_id()
#print(Charizard.get_type())

