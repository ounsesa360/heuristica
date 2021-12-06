import sys

file = open(sys.argv[1])
mapa = list(file.read())
def get_containers():
    a = 3
    b = 2
    return a,b

print(get_containers())