# This file was used early in development to determine what pokemon worked when looking them up in pokeapi
# and which ones needed to get their name modified (nidoran, mr. mime, etc). It writes to a file all of the names
# that pokeapi couldn't find, which became 0 when I handled each one.
# Must run this file from the testingandsetup directory.

from calculate import getType, getPokemonData

file = open('names.txt', 'r')

namesList = file.readlines()

invalidNames = open('invalidNames.txt', 'w')


for name in namesList:
    data = getPokemonData(name[:-1])
    if not data:
        print(f"{name[:-1].upper()} DID NOT WORK!!!!!!!!!!")
        invalidNames.write(f"{name}")
    else:
        type = getType(data[0])
        if type == ['variety']:
            print(f"{name[:-1]} has varieties!")
            invalidNames.write(f"{name}")
        else:
            print(f"{name[:-1]}: Good!")

file.close()
invalidNames.close()