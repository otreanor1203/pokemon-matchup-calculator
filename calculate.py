import requests
import re


def getType(pokemon_name):


    #Replace all instances of a space with a '-' for url compatability
    pokemon_name = pokemon_name.replace(' ', '-')
    pattern = r'[^a-zA-Z0-9-]'
    pokemon_name = re.sub(pattern, '', pokemon_name)

    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    pokemon_response = requests.get(pokemon_url)

    if pokemon_response.status_code != 200:

        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"

        species_response = requests.get(species_url)

        if species_response.status_code != 200:
            
            print(f"{pokemon_name} not found!")

            return None

        species_data = species_response.json()

        varieties_info = species_data['varieties']

        print(f"{pokemon_name} has varieties!\n")

        return []
    

    # if len(varieties_info) == 1:
    #     pokemon_url = varieties_info[0]['pokemon']['url']

    # else:
    #     print(f"{pokemon_name} has varieties!")

    #     return None

    pokemon_response = requests.get(pokemon_url)

    pokemon_data = pokemon_response.json()

    types_info = pokemon_data['types']

    pokemon_types = []

    for types in types_info:
        pokemon_types.append(types['type']['name'])

    return pokemon_types
    

def getWeaknesses(types):
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
    
    url = f"https://pokeapi.co/api/v2/type/{types[0]}"

    response = requests.get(url)

    if response.status_code != 200:
        
        print("Type not found!\n")

        return None
    


    data = response.json()
    damage_relations = data['damage_relations']

    for type in damage_relations['double_damage_from']:
        effectiveness[type['name']] += 1
    
    for type in damage_relations['half_damage_from']:
        effectiveness[type['name']] -= 1

    for type in damage_relations['no_damage_from']:
        effectiveness[type['name']] = 0

    
    if len(types) == 2:
        url = f"https://pokeapi.co/api/v2/type/{types[1]}"

        response = requests.get(url)

        if response.status_code != 200:
            
            print("Type not found!\n")

            return None
        


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

    #print(effectiveness)

    return effectiveness


def printEffectiveness(effectiveness):
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
            print("Error: Effectiveness value is not between 0-5\n")
        
    print("Immune: ")
    for type in immune:
        print(f"{type} ")
    print("\nDouble Not Effective: ")
    for type in superResistant:
        print(f"{type} ")
    print("\nNot Effective: ")
    for type in resistant:
        print(f"{type} ")
    print("\nNeutral: ")
    for type in neutral:
        print(f"{type} ")
    print("\nSuper Effective: ")
    for type in weak:
        print(f"{type} ")
    print("\nDouble Super Effective: ")
    for type in superWeak:
        print(f"{type} ")


    




