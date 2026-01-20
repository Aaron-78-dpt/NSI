import requests
import matplotlib.pyplot as plt

# Étape 1 : récupérer la liste des types
url_types = "https://pokeapi.co/api/v2/type"
types_data = requests.get(url_types).json()

types = []
counts = []

# Étape 2 : pour chaque type, compter les Pokémon
for t in types_data["results"]:
    type_name = t["name"]
    type_url = t["url"]

    # Récupérer les Pokémon du type
    type_info = requests.get(type_url).json()
    nb_pokemon = len(type_info["pokemon"])

    types.append(type_name.upper())
    counts.append(nb_pokemon)

# Étape 3 : diagramme en barres
plt.figure(figsize=(12, 6))
plt.bar(types, counts, color="skyblue", edgecolor="black")
plt.xticks(rotation=45)
plt.ylabel("Nombre de Pokémon")
plt.title("Nombre de Pokémon par type")
plt.tight_layout()
plt.show()
