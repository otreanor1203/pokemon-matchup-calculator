from calculate import *

user_pokemon = input("Enter a pokemon: ")

user_type = getType(user_pokemon)

if user_type:
    weakness = getWeaknesses(user_type)
    printEffectiveness(weakness)