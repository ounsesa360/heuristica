from PriorityQueue import Node


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
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.len += 1
        return

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
