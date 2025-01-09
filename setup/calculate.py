# This file does all of the logic to gather all of the pokemon info. It uses pokeapi to get all of the info.

import requests
import re

# Simple Pokemon class to store all of the info for each pokemon
class Pokemon:

    def __init__(self, name, url, data, image = None, type = None, weaknesses = None):
        self.name = name
        self.url = url
        self.data = data
        self.image = image
        self.type = type
        self.weaknesses = weaknesses

    def printEverything(self):

        print(self.name)
        print(self.url)
        print(self.data)
        print(self.image)
        print(self.type)
        print(self.weaknesses)

    def toDict(self):
        return {
            "name": self.name,
            "url": self.url,
            "data": self.data,
            "image": self.image,
            "type": self.type,
            "weaknesses": self.weaknesses,
        }

        


# Function that takes in the species data from pokeapi and gets all of the info on each variety
def getVarieties(species_data):
    if not species_data:
        return None
    variety_names = []
    variety_dict = species_data['varieties']
    for variety in variety_dict:
        variety_names.append(variety['pokemon']['name'])

    return variety_names

# Function that takes in a pokemon name and gets the data from pokeapi
def getPokemonData(pokemon_name):

    #Replace all instances of a space with a '-' for url compatability and apply regex
    pokemon_name = pokemon_name.replace(' ', '-')
    pattern = r'[^a-zA-Z0-9-]'
    pokemon_name = re.sub(pattern, '', pokemon_name)

    if not pokemon_name:
        return None

    # There are two pokemon named nidoran (male and female) and so this is needed to differentiate between them.
    if(pokemon_name.lower() == "nidoranm" or pokemon_name.lower() == "nidoran male"):
        pokemon_name = "nidoran-m"
    elif(pokemon_name.lower() == "nidoranf" or pokemon_name.lower() == "nidoran female"):
        pokemon_name = "nidoran-f"

    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"

    # First we get the variety info, which gets us the info of the pokemon family.
    # This is then used later to get the info on each individual pokemon.
    species_response = requests.get(species_url)

    if species_response.status_code != 200:
        
        # print(f"{pokemon_name} not found!")

        return None
    
    species_data = species_response.json()
    varieties = getVarieties(species_data)

    pokemon_varieties = []

    for variety in varieties:
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{variety}"
        pokemon_response = requests.get(pokemon_url)
        if pokemon_response.status_code != 200:
            print(f"{pokemon_name} not found!")
            return None
        pokemon_data = pokemon_response.json()
        pokemon_varieties.append(Pokemon(variety, pokemon_url, pokemon_data))

    return pokemon_varieties
    
# Function that returns the type of a pokemon using it's data.
def getType(pokemon):
    if not pokemon:
        return

    types_info = pokemon.data['types']

    pokemon_types = []

    for types in types_info:
        pokemon_types.append(types['type']['name'])

    return pokemon_types
    
# Function that gathers the types of each variety of a pokemon family
def getAllTypes(pokemon_varieties):
    if not pokemon_varieties:
        return None
    
    for pokemon in pokemon_varieties:
        pokemon.type = getType(pokemon)

# Function that calculates each pokemon's weaknesses by collecting info on each type using pokeapi and figuring out what each type is weak to
# and strong against. It then gives it a value 0-5 for each type.
def getWeaknesses(pokemon):
    if not pokemon:
        return None

    effectiveness = {
        'normal': 3,
        'fire': 3,
        'water': 3,
        'electric': 3,
        'grass': 3,
        'ice': 3,
        'fighting': 3,
        'poison': 3,
        'ground': 3,
        'flying': 3,
        'psychic': 3,
        'bug': 3,
        'rock': 3,
        'ghost': 3,
        'dragon': 3,
        'dark': 3,
        'steel': 3,
        'fairy': 3
    }
    
    url = f"https://pokeapi.co/api/v2/type/{pokemon.type[0]}"

    response = requests.get(url)

    data = response.json()
    damage_relations = data['damage_relations']

    for type in damage_relations['double_damage_from']:
        effectiveness[type['name']] += 1
    
    for type in damage_relations['half_damage_from']:
        effectiveness[type['name']] -= 1

    for type in damage_relations['no_damage_from']:
        effectiveness[type['name']] = 0

    
    if len(pokemon.type) == 2:
        url = f"https://pokeapi.co/api/v2/type/{pokemon.type[1]}"

        response = requests.get(url)

        data = response.json()
        damage_relations = data['damage_relations']

        for type in damage_relations['double_damage_from']:
            if effectiveness[type['name']] != 0:
                effectiveness[type['name']] += 1
        
        for type in damage_relations['half_damage_from']:
            if effectiveness[type['name']] != 0:
                effectiveness[type['name']] -= 1

        for type in damage_relations['no_damage_from']:
            effectiveness[type['name']] = 0

    return effectiveness

# Function that takes in a value 0-5 from the previous function and returns a dictionary showing the weaknesses and strengths.
def getEffectiveness(effectiveness):

    immune = []
    superResistant = []
    resistant = []
    neutral = []
    weak = []
    superWeak = []

    for type in effectiveness:

        if effectiveness[type] == 0:
            immune.append(type)
        elif effectiveness[type] == 1:
            superResistant.append(type)
        elif effectiveness[type] == 2:
            resistant.append(type)
        elif effectiveness[type] == 3:
            neutral.append(type)
        elif effectiveness[type] == 4:
            weak.append(type)
        elif effectiveness[type] == 5:
            superWeak.append(type)
        else:
            print("Error: Effectiveness value is not between 0-5\n")    # Should never happen

    return {
        "immune": immune,
        "superResistant": superResistant,
        "resistant": resistant,
        "neutral": neutral,
        "weak": weak,
        "superWeak": superWeak
    }

# Function that gets the type matchups for all varieties of a species.
def getAllEffectiveness(pokemon_varieties):
    for pokemon in pokemon_varieties:
        pokemon.weaknesses = getEffectiveness(getWeaknesses(pokemon))

# Function that gets the image for a pokemon
def getImage(pokemon):
    return pokemon.data['sprites']['front_default']

# Function that gets each image of a pokemon variety
def getAllImages(pokemon_varieties):
    for pokemon in pokemon_varieties:
        pokemon.image = getImage(pokemon)

# Function that calls the above 'all' functions to gather all of the info needed for a pokemon
def getEverything(pokemon_name):
    if not pokemon_name:
        return None
    varieties = getPokemonData(pokemon_name)
    if not varieties:
        return None
    getAllTypes(varieties)
    getAllEffectiveness(varieties)
    getAllImages(varieties)

    return varieties
