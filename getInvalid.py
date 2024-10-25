from calculate import getType, getPokemonData

file = open('names.txt', 'r')

namesList = file.readlines()

invalidNames = open('invalidNames.txt', 'w')

# print(namesList)

for name in namesList:
    data = getPokemonData(name[:-1])
    if not data:
        print(f"{name[:-1].upper()} DID NOT WORK!!!!!!!!!!")
    else:
        type = getType(data[0])
        if not type:
            print(f"{name[:-1].upper()} DID NOT WORK!!!!!!!!!!")
            invalidNames.write(f"{name}")
        elif type == ['variety']:
            print(f"{name[:-1]} has varieties!")
            invalidNames.write(f"{name}")
        else:
            print(f"{name[:-1]}: Good!")