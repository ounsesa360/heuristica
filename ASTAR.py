from DoubleLinkedList import DoubleLinkList
from PriorityQueue import PriorityQueue
import sys

global MAP
global INITIAL_PORT
global PORTS
# PORTS[0] = lista de contenedores en el puerto 0, del estado inicial todos los que hay que cargar
# PORTS[1] = lista de contenedores en el puerto 1, son los contenedores del puerto 2 que han sido recolocados
# Los contenedores del puerto 1 que se descarguen en este pueden ser descartados ya del problema
# PORTS[2] no sé para qué existe

class Node:

    def __init__(self, port=0, pos_containers={}):
        self.value = State(port, pos_containers)
        self.parent = None
        self.cost = 0
        self.heur = 0

    def __str__(self):
        return self.value


class State:

    def __init__(self, port=0, pos_containers={}):
        self.port = port
        self.pos_containers = pos_containers

    def __str__(self):
        return "Puerto: " + str(self.port) + "\nContenedores: " + str(self.pos_containers)


class ASTAR:

    def __init__(self, heuristic):
        self.expanded_nodes = DoubleLinkList()
        self.node_list = PriorityQueue()
        self.heuristic = heuristic
        self.current = Node()
        self.search()

    def search(self):
        # Mientras haya nodos que expandir
        self.current.heuristic = same_height_heuristic(self.current)
        print(self.current.heuristic)
        self.node_list.add_item(self.current)
        while not self.node_list.isEmpty():
            expanding_node = self.node_list.remove_first()
            expanding_node = Node(expanding_node.state.port,expanding_node.state.pos_containers)
            new_node_list = get_children(expanding_node)
            for node in new_node_list:
                self.node_list.add_item(node)



def get_children(node):
    new_node_list = []
    # Aplicamos operadores según precondiciones
    port_dll = PORTS[node.value.port]
    # Si no hay contenedores en el puerto, no se pueden cargar
    if not port_dll.isEmpty():
        # Si los hay, cogemos el primero para cargarlo
        container = port_dll.remove_first()
        # Sacamos los posibles nodos que se generan al cargarlo
        # en las distintas posiciones posibles
        new_node_list += cargar(node, container)
        # Y lo añadimos a la lista de nuevos nodos
        #for new_node in new_node_list:
        #    new_node_list.append(new_node)

    # Si no hay contenedores en el barco, no se puede descargar
    if len(node.value.pos_containers) != 0:
        new_node_list += descargar(node)
    # Si el puerto está vacio
    # También hay que comprobar que el barco no tenga elementos de ese puerto
    if port_dll.isEmpty():
        new_node_list += navegar(node)
    return new_node_list


def navegar(node):
    # Que no pueda navegar si tiene contenedores que dejar en ese puerto
    for container in node.value.pos_containers:
        if node.value.pos_containers[container][2] == node.value.port:
            return []
    new_node = Node(node.value.port + 1, node.value.pos_containers)
    new_node.cost = node.cost + 3500
    new_node.heur = same_height_heuristic(new_node)
    new_node.parent = node
    return [new_node]

def descargar(node):
    # Cogemos el último container que se ha insertado en el barco
    container = node.value.pos_containers.popitem()
    # Si coincide con el puerto al que tiene que ir
    if container[1][2] == node.value.port:
        # Se ha entregado bien, haremos sus operaciones correspondientes
        pass
    else:
        # Va a ser recolocado, lo insertamos en el puerto para luego volver a cargarlo
        PORTS[node.value.port].add_item(container)
    new_node = Node(node.value.port,node.value.pos_containers)
    new_node.cost = node.cost + 15 + 2 * (len(MAP)-container[1][0])
    new_node.heur = same_height_heuristic(node)
    new_node.parent = node
    return [new_node]


def cargar(node,container):
    # Añadimos al Node.pos_containers el container colocado
    new_pos_containers = node.value.pos_containers
    print(container) #######################################
    available_pos_list = set_container(new_pos_containers)
    new_node_list = []
    for new_pos in available_pos_list:
        new_pos_containers[int(container[0])] = new_pos
        # Creamos un nuevo nodo con los valores del antiguo nodo + nuevo
        new_node = Node(node.value.port,new_pos_containers)
        new_node.cost = node.cost + 10 * (len(MAP) - new_pos[0])
        new_node.heur = same_height_heuristic(new_node)
        new_node.parent = node
        new_node_list.append(new_node)

    # Devolvemos la lista de nodos
    return new_node_list



def set_container(pos_containers):
    map = MAP
    available_pos = []
    for element in pos_containers:
        pos_cont = pos_containers[element]
        map[pos_cont[0]][pos_cont[1]] = "F"
    for i in range(len(map)-1, -1, -1):
        for j in range(len(map[0])-1, -1, -1):
            element = map[i][j]
            if element == "F" and map[i - 1][j] != "F" and map[i - 1][j] != "X":
                available_pos.append((i-1,j))
    return available_pos



def same_height_heuristic(node):
    # No hay coste adicional por altura
    heur = 0
    # Buscamos hasta que puerto tendremos que ir para los costes de navegación
    max_port = 0
    # En este caso los node.value tienen la estrcutura de [id,tipo,puerto]
    containers_list = PORTS[node.value.port]
    aux_node = containers_list.head
    while aux_node.next:
        if int(aux_node.value[2]) > max_port:
            max_port = int(aux_node.value[2])
        aux_node = aux_node.next
    heur += max_port*3500
    # Cargamos todos los contenedores con su coste
    heur += containers_list.len * 25
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
        height = len(MAP) - node.value.pos_containers[key][0]
        discharge_cost = 15 + 2 * height
        value += discharge_cost
    navigation_costs = (max_port - node.value.port) * 3500
    value += navigation_costs
    return value



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
initial_port = DoubleLinkList()
initial_containers = get_containers(sys.argv[1], sys.argv[3])
for container in initial_containers:
    initial_port.add_item(container)
first_port = DoubleLinkList()
PORTS = [initial_port,first_port]

sol = ASTAR(1)
sol.search()


