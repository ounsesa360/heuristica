class Node:
    def __init__(self, heur=None,cost=None,state=None, parent = None):
        self.next = None
        self.prev = None
        self.heur = heur
        self.cost = cost
        self.value = self.heur + self.cost
        self.state = state
        self.parent = parent

class State:

    def __init__(self, port=0, pos_containers={}):
        self.port = port
        self.pos_containers = pos_containers

    def __str__(self):
        return "Puerto: " + str(self.port) + "\nContenedores: " + str(self.pos_containers)

    def __repr__(self):
        return self.__str__() ###############################


class PriorityQueue:

    def __init__(self):
        self.head = None
        self.tail = None ##############dudoso
        self.len = 0



    def add_item(self, element):
        new_node = Node(element.heur,element.cost,element.value, element.parent)
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
                    if node.prev:
                        node.prev.next = new_node
                    # Que el nodo sobre el que iteramos apunte con su prev al nuevo nodo
                    node.prev = new_node
                    if self.head == node:
                        self.head = new_node
                    self.len += 1
                    return

                elif node.next is None:
                    node.next = new_node
                    new_node.prev = node
                    self.tail = new_node ##############dudoso
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
                    self.len -= 1
                    return node
                node = node.next

    def remove_first(self):
        if self.head is None:
            print("No puedes borrar de una lista vacía, estupido")
            return
        elif self.len == 1:
            node = self.head
            self.head = None
            self.tail = None
            self.len -= 1
            return node
        else:
            node = self.head
            node.next.prev = None
            self.head = self.head.next
            self.len -= 1
            return node

    def isEmpty(self):
        if self.len == 0:
            return True
        return False
