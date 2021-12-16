from DoubleLinkedList import DoubleLinkList


class State:

    def __init__(self):
        self.port = 0
        self.pos_containers = {}
        self.ev_value = evaluation_function()


class Port:

    def __init__(self, number):
        self.containers = []
        self.port = number


class ASTAR:

    def __init__(self, heuristic):
        self.state = State()
        self.heuristic = heuristic
        self.operators = 3
        self.cost = 0

    def navegar(self):
        # Que la lista del puerto 0 esté vacía
        # if self.state.port == 0:
        if self.state.port == 1:
            for container in self.state.pos_containers:
                if self.state.pos_containers[container][2] == 1:
                    return False
        # Que si en puerto 1, no navegar y dejar atrás contenedores del puerto 2

        if 0 <= self.state.port < 2:
            self.state.port += 1
            self.cost = 3500
            return True
        return False

    def cargar(self, container):
        # Si puerto 1, no cargar contenedores del 1
        # Generamos el nodo dentro del operador, y calculamos la funcion de evaluacion asociada a ese nodo desde aqui

        if self.state.port == 2:
            return False

    def descargar(self, container):
        if self.state.port == 0:
            return False
