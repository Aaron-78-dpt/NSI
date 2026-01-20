import requests
import time
import random as r
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


# ---------------------------------------------------------
#  FONCTION : Animation fade-in du graphique
# ---------------------------------------------------------
def fade_in_bars(ax, types, counts, colors, title, steps=40, delay=0.05):
    for alpha in range(1, steps + 1):
        ax.clear()
        ax.bar(types, counts, color=colors, edgecolor="black", alpha=alpha/steps)
        ax.set_xticklabels(types, rotation=45)
        ax.set_ylabel("Nombre de Pokémon")
        ax.set_title(title)
        plt.pause(delay)


# ---------------------------------------------------------
#  CLASSE POKÉMON
# ---------------------------------------------------------
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
        return r.json()["name"]

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        return [t["type"]["name"] for t in r.json()["types"]]

    def get_taille(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        return r.json()["height"] / 10

    def get_poids(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        return r.json()["weight"] / 10

    def get_faiblesse(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        faiblesses = set()

        for t in data["types"]:
            type_name = t["type"]["name"]
            r_type = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}")
            type_data = r_type.json()
            for f in type_data["damage_relations"]["double_damage_from"]:
                faiblesses.add(f["name"])

        return list(faiblesses)

    # --- IMAGES HD ---
    def get_image_hd(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        return r.json()["sprites"]["other"]["official-artwork"]["front_default"]

    def get_image_hd_shiny(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        return r.json()["sprites"]["other"]["official-artwork"]["front_shiny"]


# ---------------------------------------------------------
#  CLASSE POKEDEX
# ---------------------------------------------------------
class Pokedex:
    def __init__(self, nom=""):
        self.nom = nom
        self.pokedex = []

    def ajouter_pokemon(self, pokemon):
        self.pokedex.append(pokemon)


# ---------------------------------------------------------
#  CLASSE GAME
# ---------------------------------------------------------
class Game:
    def __init__(self, pokedex):
        self.pokedex = pokedex
        self.first_captured = None  # IMPORTANT

    def choisir_starter(self):
        starters = ["bulbasaur", "charmander", "squirtle"]

        print("Choisis ton starter :")
        for i, s in enumerate(starters, 1):
            print(f"{i}. {s.capitalize()}")

        choix = int(input("Ton choix (1-3) : "))
        nom = starters[choix - 1]

        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nom}")
        data = r.json()

        pokemon = Pokemon(nom=data["name"], id=data["id"])
        self.pokedex.ajouter_pokemon(pokemon)

        print(f"\n{pokemon.nom.capitalize()} a été ajouté à ton Pokédex !")

    def afficher_pokedex(self):
        print("\n📖 Ton Pokédex :")
        for p in self.pokedex.pokedex:
            print(p)

    def aventure(self):
        for _ in range(5):
            time.sleep(1)

            if r.randint(0, 11) >= 8:
                id = r.randint(1, 1350)
                pok = Pokemon("", id)

                print(f"⚔️ Un {pok.get_nom().capitalize()} apparaît !!")
                print("1- Capturer")
                print("2- Fuir")

                choix = int(input("> "))

                if choix == 1:
                    if r.randint(0, 4) >= 2:
                        self.pokedex.ajouter_pokemon(pok)
                        print("🎉 Pokémon capturé !")

                        if self.first_captured is None:
                            self.first_captured = pok
                    else:
                        print("❌ Échec de la capture...")
                else:
                    print("🏃 Tu as fui.")

        return self.first_captured


# ---------------------------------------------------------
#  AFFICHAGE FINAL : IMAGES + GRAPHIQUE
# ---------------------------------------------------------
def afficher_graphique(pokemon):
    # Récupération des types globaux
    url_types = "https://pokeapi.co/api/v2/type"
    types_data = requests.get(url_types).json()

    types = []
    counts = []

    for t in types_data["results"]:
        type_name = t["name"]
        type_url = t["url"]

        type_info = requests.get(type_url).json()
        nb_pokemon = len(type_info["pokemon"])

        types.append(type_name.upper())
        counts.append(nb_pokemon)

    # Couleurs
    highlight_types = [t.upper() for t in pokemon.get_type()]
    colors = ["gold" if t not in highlight_types else "red" for t in types]

    # Images HD
    img_hd = pokemon.get_image_hd()
    img_hd_shiny = pokemon.get_image_hd_shiny()

    # FIGURE
    fig = plt.figure(figsize=(14, 12))

    ax_img1 = plt.subplot2grid((2, 2), (0, 0))
    ax_img2 = plt.subplot2grid((2, 2), (0, 1))
    ax_graph = plt.subplot2grid((2, 2), (1, 0), colspan=2)

    # Image normale
    img_data = requests.get(img_hd).content
    ax_img1.imshow(Image.open(BytesIO(img_data)))
    ax_img1.axis("off")
    ax_img1.set_title(f"{pokemon.get_nom().capitalize()} (Normal HD)")

    # Image shiny
    img_data = requests.get(img_hd_shiny).content
    ax_img2.imshow(Image.open(BytesIO(img_data)))
    ax_img2.axis("off")
    ax_img2.set_title(f"{pokemon.get_nom().capitalize()} (Shiny HD)")

    # Graphique animé
    title = f"Types de {pokemon.get_nom().capitalize()}"
    fade_in_bars(ax_graph, types, counts, colors, title)

    plt.tight_layout()
    plt.show()

#lancement du jeu
Monpoke = Pokedex("MonPoke")
game = Game(Monpoke)

game.choisir_starter()
captured = game.aventure()

if captured:
    print("\n📊 Affichage du Pokémon capturé !")
    afficher_graphique(captured)
else:
    print("\n📊 Aucun Pokémon capturé, affichage du starter.")
    afficher_graphique(Monpoke.pokedex[0])
