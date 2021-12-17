class Node:
    def __init__(self, value=None):
        self.next = None
        self.prev = None
        self.value = value

class DoubleLinkList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def __str__(self):
        node = self.head
        res = ""
        while node.next:
            res += str(node.value)
            node = node.next
        return res

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

    def remove_first(self):
        if self.head is None:
            print("No puedes borrar de una lista vacía, estupido")
            return
        elif self.len == 1:
            node = self.head
            self.head = None
            self.tail = None
            self.len -= 1
            return node.value
        else:
            node = self.head
            node.next.prev = None
            self.head = self.head.next
            self.len -= 1
            return node.value

    def isEmpty(self):
        if self.len == 0:
            return True
        return False
