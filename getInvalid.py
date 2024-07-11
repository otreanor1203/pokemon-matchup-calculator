from calculate import getType

file = open('names.txt', 'r')

namesList = file.readlines()

invalidNames = open('invalidNames.txt', 'w')

for name in namesList:
    type = getType(name[:-1])
    if not type:
        invalidNames.write(f"{name}")
    elif type == ['variety']:
        print(f"{name[:-1]} has varieties!")
        invalidNames.write(f"{name}")
    else:
        print(f"{name[:-1]}: Good!")