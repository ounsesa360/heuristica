import sys
from ASTAR import ASTAR,Port

def get_map(path, map_name):
    # Creamos una matriz para el mapa
    map = []
    # Abrimos el archivo del mapa
    with open(path + "/" + map_name) as file:
        # Vamos leyendo por filas
        for row in file:
            map_list = []
            # Si no son los espacios o el salto de linea
            for column in row:
                if column != " " and column != "\n":
                    # Lo añadimos a la fila
                    map_list.append(column)
            # Añadimos la fila a la matriz
            map.append(map_list)
    # Devolvemos la matriz
    return map


def convert_position_matrix(position_matrix):
    for i in range(len(position_matrix)-1, -1, -1):
        for j in range(len(position_matrix[0])-1, -1, -1):
            element = position_matrix[i][j]
            if element == "X" and i == len(position_matrix)-1:
                position_matrix[i][j] = "F"
            elif element == "X" and position_matrix[i+1][j] == "F":
                position_matrix[i][j] = "F"
            elif element == "X" and position_matrix[i+1][j] != "F":
                for k in range(i-1, -1, -1):
                    position_matrix[k][j] = "X"
    return position_matrix


def get_containers(path, containers_name):
    container_list = []
    with open(path + "/" + containers_name) as data_file:
        for row in data_file:
            containers = []
            for i in range(len(row)):
                if row[i] != " " and row[i] != "\n":
                    if row[i] == "S":
                        containers.append("N")
                    elif row[i] == "R":
                        containers.append("E")
                    else:
                        containers.append(row[i])
            container_list.append(containers)
    return container_list


containers = get_containers(sys.argv[1], sys.argv[3])
map = get_map(sys.argv[1],sys.argv[2])
modified_map = convert_position_matrix(map)
initial_port = Port(0)
for container in containers:
    initial_port.containers.append(container)
print(initial_port.containers)
