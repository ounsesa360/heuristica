import sys


class State:

    def __init__(self):
        self.port = 0
        self.pos_containers = {}


class InitialState(State):
    def __init__(self):
        super().__init__()
        self.map = self.get_map(sys.argv[1], sys.argv[2])
        self.pos_containers = self.get_pos_containers()

    def get_map(self, path, map_name):
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

    def get_pos_containers(self):
        pos_containers = {}
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if (self.map[i][j] != "N") and (self.map[i][j] != "E") and (self.map[i][j] != "X"):
                    pos_containers[int(self.map[i][j])] = (i, j)
        return pos_containers


class Node:
    def __init__(self, value = 0):
        self.next = None
        self.prev = None
        self.value = value


class DoubleLinkList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def add_item(self, element):
        new_node = Node(element)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.len += 1
        else:
            node = self.head
            value = new_node.value
            while True:
                if node.value > value:
                    # Nuevo nodo.next apunta a nodo en el que estamos iterando
                    new_node.next = node
                    # El previo del nuevo nodo será el antiguo previo del nodo en el que estamos iterando
                    new_node.prev = node.prev
                    # Que el nodo previo al que recorremos apunte al nuevo nodo
                    node.prev.next = new_node
                    # Que el nodo sobre el que iteramos apunte con su prev al nuevo nodo
                    node.prev = new_node
                    if self.head == node:
                        self.head = new_node
                    self.len += 1
                    return

                elif node.next is None:
                    node.next = new_node
                    new_node.prev = node.next
                    self.tail = new_node
                    self.len += 1
                    return

                node = node.next

    def remove_item(self, element):
        if self.head is None:
            print("No puedes borrar de una lista vacía, estupido")
            return
        else:
            node = self.head
            while True:
                if node.value == element:
                    node.prev.next = node.next
                    node.next.prev = node.prev
                    del node
                    self.len -= 1
                    return
                node = node.next


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

State()
containers = get_containers(sys.argv[1], sys.argv[3])
print(containers)