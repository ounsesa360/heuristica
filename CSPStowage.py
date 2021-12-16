from constraint import *
import sys
problem = Problem()

def get_map(path, map_name):
	#Creamos una matriz para el mapa
	map = []
	#Abrimos el archivo del mapa
	with open(path + "/" + map_name) as file:
		#Vamos leyendo por filas
		for row in file:
			map_list = []
			#Si no son los espacios o el salto de linea
			for column in row:
				if column != " " and column != "\n":
					#Lo añadimos a la fila
					map_list.append(column)
			#Añadimos la fila a la matriz
			map.append(map_list)
	#Devolvemos la matriz
	return map

def get_containers(path, containers_name):
	container_list = []
	with open(path +"/" + containers_name) as data_file:
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


def get_regular_containers(containers_map):
	regular_containers = []
	for container in containers_map:
		if container[1] == "N":
			regular_containers.append(container)
	return regular_containers


def get_refrigerate_containers(containers_map):
	refrigerate_containers = []
	for container in containers_map:
		if container[1] == "E":
			refrigerate_containers.append(container)
	return refrigerate_containers


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

def get_floor(map):
	global floor
	floor = []
	for i in range(len(map)):
		for j in range(len(map[0])):
			if map[i][j] == "F":
				floor.append((j, i))
	return floor

def get_available_position(map):
	available_regular_pos = []
	available_refrigerate_pos = []
	for i in range (len(map)):
		for j in range (len(map[0])):
			if map[i][j] == "N":
				available_regular_pos.append((j, i))
			if map[i][j] == "E":
				available_regular_pos.append((j, i))
				available_refrigerate_pos.append((j, i))
	return available_regular_pos, available_refrigerate_pos

def not_floating(*args):
	containers = list(args)
	for i in containers:
		cond = False
		row = i[1]
		column = i[0]
		if (column,row+1) not in floor:
			for k in containers:
				if i != k:
					other_row = k[1]
					other_column = k[0]
					if column == other_column:
						if other_row == row + 1:
							cond = True
							break
			if not cond:
				return False
	return True

def not_reorganizing(*args):
	for i in range(len(args)):
		for j in range(len(args)):
			column = args[i][0]
			other_column = args[j][0]
			if i != j and column == other_column:
				puerto = containers_map[i][2]
				other_puerto = containers_map[j][2]
				if puerto > other_puerto:
					row = args[i][1]
					other_row = args[j][1]
					if row < other_row:
						return False
	return True

def get_containers_id(containers_map):
	container_id_list = []
	for i in containers_map:
		container_id_list.append(i[0])
	return container_id_list


def add_domains(regular_containers, refrigerate_containers, available_regular_pos, available_refrigerate_pos):
	for container in regular_containers:
		problem.addVariable(container[0], available_regular_pos)

	for container in refrigerate_containers:
		problem.addVariable(container[0], available_refrigerate_pos)


def print_data():
	print("Mapa modificado")
	for i in range(len(modified_map)):
		print(modified_map[i])

	print("Contenedores")
	for i in range(len(containers_map)):
		print(containers_map[i])

	print("Contenedores normales")
	for i in range(len(regular_containers)):
		print(regular_containers[i])

	print("Contenedores refrigerados")
	for i in range(len(refrigerate_containers)):
		print(refrigerate_containers[i])

	print("Posiciones disponibles cont. normal")
	for i in range(len(available_regular_pos)):
		print(available_regular_pos[i])

	print("Posiciones disponibles cont. refrigerados")
	for i in range(len(available_refrigerate_pos)):
		print(available_refrigerate_pos[i])

mapa = get_map(sys.argv[1], sys.argv[2])
modified_map = convert_position_matrix(mapa)
global containers_map
containers_map = get_containers(sys.argv[1], sys.argv[3])
container_id_list = get_containers_id(containers_map)
regular_containers = get_regular_containers(containers_map)
refrigerate_containers = get_refrigerate_containers(containers_map)
available_regular_pos, available_refrigerate_pos = get_available_position(modified_map)
add_domains(regular_containers, refrigerate_containers, available_regular_pos, available_refrigerate_pos)
get_floor(modified_map)
print_data()

problem.addConstraint(AllDifferentConstraint(), container_id_list)
problem.addConstraint(not_floating,container_id_list)
soluciones = problem.getSolutions()
file = open("./CSP-tests/"+sys.argv[2]+"-"+sys.argv[3]+".output", "w")
if len(soluciones) != 0:
	problem.addConstraint(not_reorganizing,container_id_list)
	soluciones2 = problem.getSolutions()
	if len(soluciones2) != 0:
		file.write("Numero de soluciones encontradas: " + str(len(soluciones2)) + "\n")
		for solucion in soluciones2:
			file.write(str(solucion)+"\n")
	else:
		file.write("No se han encontrado soluciones sin reordenamiento.\nNumero de soluciones con reordenamiento encontradas: " + str(len(soluciones)) + "\n")
		for solucion in soluciones:
			file.write(str(solucion)+"\n")
else:
	file.write("No existen soluciones al problema")