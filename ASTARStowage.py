from DoubleLinkedList import DoubleLinkList
from PriorityQueue import PriorityQueue
from datetime import datetime
import sys

global MAP

class Node:

    def __init__(self,pos_containers, port=0):
        self.value = State(pos_containers,port)
        self.parent = None
        self.cost = 0
        self.heur = 0

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)


class State:

    def __init__(self, pos_containers,port=0):
        self.port = port
        self.pos_containers = pos_containers

    def __str__(self):
        return "Puerto: " + str(self.port) + "\nContenedores: " + str(self.pos_containers)


class ASTAR:

    def __init__(self, heuristic, initial_config):
        self.expanded_states = DoubleLinkList()
        self.node_list = PriorityQueue()
        self.heuristic = heuristic
        self.current = Node(initial_config)
        if heuristic == "same_height_heuristic":
            self.current.heur = same_height_heuristic(self.current)
        elif heuristic == "no_charging_cost_heuristic":
            self.current.heur = no_charging_cost_heuristic(self.current)
        else:
            self.current.heur = None
        self.expanded_nodes = 0
        self.dt = datetime.now()
        self.search()

    def search(self):
        # Mientras haya nodos que expandir
        self.node_list.add_item(self.current)
        while not self.node_list.isEmpty():
            expanding_node = self.node_list.remove_first()

            if self.expanded_states.find_item(expanding_node):
                continue
            self.expanded_states.add_item(expanding_node)
            exp = Node(expanding_node.state.pos_containers, expanding_node.state.port)
            exp.parent = expanding_node.parent
            exp.cost = expanding_node.cost
            if expanding_node.heur == 0:
                dt2 = datetime.now()
                time = dt2-self.dt
                get_solution(exp, time, self.expanded_nodes)
                return
            new_node_list = get_children(exp)
            for node in new_node_list:
                self.node_list.add_item(node)
            self.expanded_nodes += len(new_node_list)
        dt2 = datetime.now()
        time = dt2 - self.dt
        file = open("./ASTAR-tests/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".output", "w+")
        file.write("No se han encontrado soluciones al problema")
        stat_file = open("./ASTAR-tests/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".stat", "w+")
        stat_file.write("Tiempo total: " + str(time) + "\nNodos expandidos: " + str(self.expanded_nodes))

def get_solution(node, time, nodes_expanded):
    actions = ""
    cont=0
    final_cost = node.cost
    while node.parent:
        cont += 1
        containers_on_boat = 0
        parent_containers_on_boat = 0
        for container in node.value.pos_containers:
            if not isinstance(node.value.pos_containers[container][0],int):
                containers_on_boat += 1
            if not isinstance(node.parent.value.pos_containers[container][0],int):
                parent_containers_on_boat += 1
        for container in node.value.pos_containers:
            if node.value.pos_containers[container][0] != node.parent.value.pos_containers[container][0]:
                break
        if containers_on_boat > parent_containers_on_boat:
            actions = "Cargar (" + str(container) + ", " + str(node.value.pos_containers[container][0]) + ")\n" + actions
        elif containers_on_boat < parent_containers_on_boat:
            actions = "Descargar (" + str(container) + ", " + str(node.value.pos_containers[container][0]) + ")\n"+ actions
        else:
            actions = "Navegar (" + str(node.parent.value.port) + ", " + str(node.value.port) + ")\n" + actions
        node = node.parent
    stat = "Tiempo total: " + str(time) + "\nCoste total: " + str(final_cost) + "\nLongitud del plan: " + str(cont) + "\nNodos expandidos: " + str(nodes_expanded)

    file = open("./ASTAR-tests/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".output", "w+")
    file.write(actions)
    stat_file = open("./ASTAR-tests/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".stat", "w+")
    stat_file.write(stat)
    file.close()
    stat_file.close()


def get_possible_charged(node):
    possible = []
    current_port = node.value.port
    for container in node.value.pos_containers:
        if node.value.pos_containers[container][0] == current_port:
            possible.append(container)
    return possible

def get_children(node):
    new_node_list = []
    # Aplicamos operadores según precondiciones
    # De primeras, vemos si hay algun contenedor en el puerto en el que estamos
    possible_charged = get_possible_charged(node)
    # Si no hay contenedores en el puerto, no se pueden cargar
    if len(possible_charged) != 0:
        # Si los hay, cogemos el primero para cargarlo
        for container in possible_charged:
            # Sacamos los posibles nodos que se generan al cargarlo
            # en las distintas posiciones posibles
            new_node_list += cargar(node, container)

    # Si no hay contenedores en el barco, no se puede descargar
    if containers_in_boat(node.value.pos_containers):
        new_node_list += descargar(node)

    # Si el puerto está vacio
    # También hay que comprobar que el barco no tenga elementos de ese puerto
    if no_containers_in_port(node):
        new_node_list += navegar(node)

    return new_node_list

def navegar(node):
    # Que no pueda navegar si tiene contenedores que dejar en ese puerto
    new_node = Node(node.value.pos_containers,node.value.port + 1)
    new_node.cost = node.cost + 3500
    new_node.heur = same_height_heuristic(new_node)
    new_node.parent = node
    return [new_node]

def descargar(node):
    # Cogemos el último container que se ha insertado en el barco
    new_pos_containers = node.value.pos_containers.copy()
    possible_discharged = []
    for container in new_pos_containers:
        if not isinstance(new_pos_containers[container][0], int):
            pos = new_pos_containers[container][0]
            cond = True
            for other_container in new_pos_containers:
                if other_container != container:
                    if not isinstance(new_pos_containers[other_container][0], int):
                        other_pos = new_pos_containers[other_container][0]
                        if other_pos[1] == pos[1]:
                            if other_pos[0] < pos[0]:
                                cond = False
            if cond:
                possible_discharged.append(container)
    new_node_list = []
    for element in possible_discharged:
        new_pos_containers = node.value.pos_containers.copy()
        container = new_pos_containers[element]
        container_height = len(MAP) - container[0][0]
        new_pos_containers[element] = [node.value.port,container[1],container[2]]
        new_node = Node(new_pos_containers, node.value.port)
        new_node.cost = node.cost + 15 + 2 * container_height
        new_node.heur = same_height_heuristic(new_node)
        new_node.parent = node
        new_node_list.append(new_node)
    return new_node_list


def cargar(node,container):
    # Añadimos al Node.pos_containers el container colocado
    new_pos_containers = node.value.pos_containers.copy()
    container_type = new_pos_containers[container][2]
    available_pos_list = set_container(new_pos_containers,container_type)
    new_node_list = []
    for new_pos in available_pos_list:
        new_pos_containers = node.value.pos_containers.copy()
        new_loc = tuple(new_pos)
        new_state = [new_loc, node.value.pos_containers[container][1],node.value.pos_containers[container][2]]
        new_pos_containers[container] = new_state
        # Creamos un nuevo nodo con los valores del antiguo nodo + nuevo
        new_node = Node(new_pos_containers,node.value.port)

        new_node.cost = node.cost + 10 + (len(MAP) - new_pos[0])
        new_node.heur = same_height_heuristic(new_node)
        new_node.parent = node
        new_node_list.append(new_node)

    # Devolvemos la lista de nodos
    return new_node_list


def set_container(pos_containers, container_type):
    available_pos = []
    map = convert_position_matrix(get_map(sys.argv[1], sys.argv[2]))
    # Marcamos los contenedores que ya están colocados como suelo para poder colocar encima
    for element in pos_containers:
        pos_cont = pos_containers[element]
        if isinstance(pos_cont[0],tuple):
            map[pos_cont[0][0]][pos_cont[0][1]] = "F"
    # Buscamos las posiciones donde se puedan colocar
    for i in range(len(map)-1, -1, -1):
        for j in range(len(map[0])-1, -1, -1):
            if map[i - 1][j] != "X" and map[i - 1][j] != "F":
                element = map[i][j]
                if element == "F":
                    if map[i - 1][j] != "E" and container_type == "E":
                        continue
                    available_pos.append([i-1, j])
    return available_pos

def containers_in_boat(pos_containers):
    for container in pos_containers:
        if not isinstance(pos_containers[container][0],int):
            return True
    return False

def no_containers_in_port(node):
    pos_containers = node.value.pos_containers
    for container in pos_containers:
        if isinstance(pos_containers[container][0],int):
            if pos_containers[container][0] != pos_containers[container][1]:
                return False
        else:
            if pos_containers[container][1] == node.value.port:
                return False
    return True

def same_height_heuristic(node):
    # No hay coste adicional por altura
    heur = 0
    # Buscamos hasta que puerto tendremos que ir para los costes de navegación
    # En este caso los node.value tienen la estrcutura de [id,tipo,puerto]
    max_port = 0
    # Cargamos todos los contenedores con su coste
    for container in node.value.pos_containers:
        if (isinstance(node.value.pos_containers[container][0],int)):
            if (node.value.pos_containers[container][0] == 0) or (node.value.pos_containers[container][0] == 1 and node.value.pos_containers[container][1] == 2):
                heur += 25
        else:
            heur += 15
        if (node.value.pos_containers[container][0] != node.value.pos_containers[container][1]):
            if node.value.pos_containers[container][1] > max_port:
                max_port = node.value.pos_containers[container][1]
    if max_port != 0:
        max_port = max_port-node.value.port
        heur += max_port*3500
    return heur


def no_charging_cost_heuristic(node):
    # No existen costes de carga
    value = 0
    max_port = 0
    for key in node.value.pos_containers:
        # Encontramos cual es el puerto más alejado de entre los contenedores que tenemos
        if node.value.port > max_port:
            max_port = node.value.port
        # Obtenemos la altura de cada contenedor para calcular el coste que supondría descargarlo
        # Importante, posiblemente haya que calcular el coste de descarga de todos los container que no están en su puero tambien
        height = len(MAP) - node.value.pos_containers[key][0]
        discharge_cost = 15 + 2 * height
        value += discharge_cost
    navigation_costs = (max_port - node.value.port) * 3500
    value += navigation_costs
    return value

def get_initial_configuration(containers_list):
    init_config = {}
    for container in containers_list:
        # Tenemos un diccionario del tipo {id:[posicion,puerto_destino,tipo]}
        # Donde posicion es su posicion en el barco o en qué puerto está
        init_config[int(container[0])] = [0,int(container[2]),container[1]]
    return init_config

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

def get_pos_containers(map):
    pos_containers = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            if (map[i][j] != "N") and (map[i][j] != "E") and (map[i][j] != "X"):
                pos_containers[int(map[i][j])] = (i, j)
    return pos_containers


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

map = get_map(sys.argv[1],sys.argv[2])
modified_map = convert_position_matrix(map)
MAP = modified_map
initial_containers = get_containers(sys.argv[1], sys.argv[3])
initial_config = get_initial_configuration(initial_containers)
expanded_nodes = 0

sol = ASTAR(sys.argv[4],initial_config)


