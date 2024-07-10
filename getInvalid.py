from calculate import getType

file = open('names.txt', 'r')

namesList = file.readlines()

invalidNames = open('invalidNames3.txt', 'w')

for name in namesList:
    if not getType(name[:-1]):
        invalidNames.write(f"{name}")
    else:
        print(f"{name[:-1]}: Good!")