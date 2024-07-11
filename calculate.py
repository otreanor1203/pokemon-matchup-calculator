import requests
import re

def getVariety(species_data, name_length, debug):
    variety_names = []
    variety_names_short = []
    if(species_data == "nidoran"):
        variety_names_short.append("m")
        variety_names_short.append("f")
    else:
        variety_dict = species_data['varieties']
        for variety in variety_dict:
            variety_names.append(variety['pokemon']['name'])

        
        for name in variety_names:
            if 'gmax' not in name:
                variety_names_short.append(name[name_length+1:])

    if debug:
        return variety_names_short[0]
    
    print("This pokemon has varieties: \n")
    for name in variety_names_short:
        print(f"{name}\n")
    

    user_variety = input("Which variety would you like?\n")
    while user_variety not in variety_names_short:
        user_variety = input("Please enter a valid variety:")
    
    return user_variety


    

def getType(pokemon_name):

    #Replace all instances of a space with a '-' for url compatability and apply regex
    pokemon_name = pokemon_name.replace(' ', '-')
    pattern = r'[^a-zA-Z0-9-]'
    pokemon_name = re.sub(pattern, '', pokemon_name)

    if(pokemon_name.lower() == "nidoranm" or pokemon_name.lower() == "nidoran male"):
        pokemon_name = "nidoran_m"
    elif(pokemon_name.lower() == "nidoranf" or pokemon_name.lower() == "nidoran female"):
        pokemon_name = "nidoran_f"
    elif(pokemon_name.lower() == "nidoran"):
        gender = getVariety("nidoran", len(pokemon_name), False)
        if gender == "m":
            pokemon_name = "nidoran-m"
        else:
            pokemon_name = "nidoran-f"

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

        user_variety = getVariety(species_data, len(pokemon_name), False)
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}-{user_variety}"
    

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
        
        print("Type not found!\n") # should not happen ever

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

    print("---------------------------------------------")
    print("Immune: ")
    for type in immune:
        print(f"{type} ")
    if not immune:
        print("N/A")
    print("\nDouble Not Effective: ")
    for type in superResistant:
        print(f"{type} ")
    if not superResistant:
        print("N/A")
    print("\nNot Effective: ")
    for type in resistant:
        print(f"{type} ")
    if not resistant:
        print("N/A")
    print("\nNeutral: ")
    for type in neutral:
        print(f"{type} ")
    if not neutral:
        print("N/A")
    print("\nSuper Effective: ")
    for type in weak:
        print(f"{type} ")
    if not weak:
        print("N/A")
    print("\nDouble Super Effective: ")
    for type in superWeak:
        print(f"{type} ")
    if not superWeak:
        print("N/A")

    print("---------------------------------------------\n")


    




