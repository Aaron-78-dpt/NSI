import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

url_types = "https://pokeapi.co/api/v2/type"
types_data = requests.get(url_types).json()

class Pokemon:
    def __init__(self, nom="", id=None):
        self.nom = nom
        self.id = id

    def get_id(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["id"]

    def get_nom(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["name"].upper()

    def get_nom_fr(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{self.id}")
        data = r.json()
        for entry in data["names"]:
            if entry["language"]["name"] == "fr":
                return entry["name"].upper()
        return self.get_nom()

    def get_type(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return [t["type"]["name"].upper() for t in data["types"]]

    def get_color(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{self.id}")
        data = r.json()
        return data["color"]["name"]

    def get_image_hd(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["sprites"]["other"]["official-artwork"]["front_default"]

    def get_image_hd_shiny(self):
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.id}")
        data = r.json()
        return data["sprites"]["other"]["official-artwork"]["front_shiny"]

P = Pokemon(id=100)

pokemon_name_en = P.get_nom()
pokemon_name_fr = P.get_nom_fr()
highlight_types = P.get_type()
pokemon_color = P.get_color()
img_hd = P.get_image_hd()
img_hd_shiny = P.get_image_hd_shiny()

types = []
counts = []

for t in types_data["results"]:
    type_name = t["name"]
    type_url = t["url"]

    type_info = requests.get(type_url).json()
    nb_pokemon = len(type_info["pokemon"])

    types.append(type_name.upper())
    counts.append(nb_pokemon)

colors = []
for t in types:
    if t in highlight_types:
        colors.append(pokemon_color)
    else:
        colors.append("gold")

fig = plt.figure(figsize=(14, 12))

ax_img1 = plt.subplot2grid((2, 2), (0, 0))
ax_img2 = plt.subplot2grid((2, 2), (0, 1))

ax_graph = plt.subplot2grid((2, 2), (1, 0), colspan=2)

if img_hd:
    img_data = requests.get(img_hd).content
    img = Image.open(BytesIO(img_data))
    ax_img1.imshow(img)
    ax_img1.axis("off")
    ax_img1.set_title(f"{pokemon_name_fr} (Normal HD)")

if img_hd_shiny:
    img_data = requests.get(img_hd_shiny).content
    img = Image.open(BytesIO(img_data))
    ax_img2.imshow(img)
    ax_img2.axis("off")
    ax_img2.set_title(f"{pokemon_name_fr} (Shiny HD)")

ax_graph.bar(types, counts, color=colors, edgecolor="black")
ax_graph.set_xticklabels(types, rotation=45)
ax_graph.set_ylabel("Nombre de Pokémon")
ax_graph.set_title(f"Types de {pokemon_name_fr} ({pokemon_name_en})")

plt.tight_layout()
plt.show()

print("ID :", P.get_id())
print("Nom anglais :", pokemon_name_en)
print("Nom français :", pokemon_name_fr)
print("Types :", highlight_types)
print("Couleur officielle :", pokemon_color)
print("Image HD :", img_hd)
print("Image HD shiny :", img_hd_shiny)
