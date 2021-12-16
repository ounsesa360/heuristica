class Node:
    def __init__(self, value=0):
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