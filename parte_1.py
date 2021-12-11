from constraint import *
import sys
problem = Problem()

# Se anyaden las variables al problema. Existen diferentes formas de hacerlo mediante las funciones addVariable y addVariables
#
# Ejemplos:
# problem.addVariable('a', [1, 2])		Crea la variable 'a' que tiene como dominio [1, 2]
# problem.addVariables("ab", [1, 2, 3])		Crea las variables 'a' y 'b', ambas con el dominio [1, 2, 3]
# problem.addVariables(['a', 'b'], range(3))	Crea las variables 'a' y 'b', ambas con el dominio [0, 1, 2]
#
# Para el problema del grupo de alumnos que tienen que hacer un documento de Ingenieria del Software tenemos 6 variables
# (J, M, A, Y, R, F), todas tienen como dominio [1, 2, 3] salvo Juan puesto que el enunciado dice que no tiene conocimientos
# para hacer la primera parte, luego su dominio sera [2, 3], y Maria que solo quiere trabajar en la tercera parte, luego su
# dominio sera [3]
#

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
				floor.append((i, j))
	return floor

def get_available_position(map):
	available_regular_pos = []
	available_refrigerate_pos = []
	for i in range (len(map)):
		for j in range (len(map[0])):
			if map[i][j] == "N":
				available_regular_pos.append((i, j))
			if map[i][j] == "E":
				available_regular_pos.append((i, j))
				available_refrigerate_pos.append((i, j))
	return available_regular_pos, available_refrigerate_pos

def not_floating(*args):
	containers = list(args)
	for i in containers:
		cond = False
		row = i[0]
		column = i[1]
		if (row+1,column) in floor:
			cond = True
		else:
			for k in containers:
				if i != k:
					other_row = k[0]
					other_column = k[1]
					if column == other_column and other_row == row + 1:
						cond = True
						break
			if not cond:
				return False
	return True

def not_reorganizing(*args):
	containers = list(args)
	print(containers)
	for i in containers:
		cond = False
		row = i[0]
		column = i[1]
		print(containers_map[containers.index(i)])
		print("a")
		for k in containers:
			if i != k:
				if containers_map[containers.index(i)][2] == 2:
					pass


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
	print(containers_map)

mapa = get_map(sys.argv[1], sys.argv[2])
modified_map = convert_position_matrix(mapa)
global containers_map
containers_map = get_containers(sys.argv[1], sys.argv[3])
regular_containers = get_regular_containers(containers_map)
refrigerate_containers = get_refrigerate_containers(containers_map)
available_regular_pos, available_refrigerate_pos = get_available_position(modified_map)
add_domains(regular_containers, refrigerate_containers, available_regular_pos, available_refrigerate_pos)
get_floor(modified_map)
print_data()

container_id_list = []
for container in regular_containers:
	container_id_list.append(container[0])
for container in refrigerate_containers:
	container_id_list.append(container[0])
problem.addConstraint(AllDifferentConstraint(), container_id_list)
problem.addConstraint(not_floating,container_id_list)
problem.addConstraint(not_reorganizing,container_id_list)
print("Sacamos solución")
print(problem.getSolutions())

# o todas las soluciones:







"""problem.addVariables(['A', 'Y', 'R', 'F'], [1, 2, 3])
problem.addVariable('J', [2, 3])
problem.addVariable('M', [3])

# A continuacion se anyaden las restricciones del problema mediante la funcion addConstraint proporcionada por la libreria
#
# Ejemplos:
# problem.addConstraint(lambda a, b: a > b, ('a', 'b'))		Crea una funcion lambda que recibe dos parametros que se corresponden
# con los valores de las variables 'a' y 'b', y comprueba que 'a' es mayor que 'b'. Tambien se podria haber creado una funcion para
# comprobar este hecho:
#
# def greater(a, b):
#    if a > b:
#	return True
#
# problem.addConstraint(greater, ('a', 'b'))
#
# En este caso vamos a modelar en primer lugar la restriccion de que Alfredo y Ruben no quieren trabajar juntos, es decir,
# RA,R = [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]. Se puede hacer de varias formas. Una de ellas es definir una funcion, por ejemplo,
# notEqual, que compruebe que el valor de una variable es diferente de la de la otra:

def notEqual(a, b):
	if a != b:
		return True

problem.addConstraint(notEqual, ('A', 'R'))

# Tambien se puede crear una funcion lambda para hacer esta comprobacion:

problem.addConstraint(lambda a, b: a != b, ('A', 'R'))


# Por ultimo, la libreria ofrece la funcion AllDifferentConstraint que precisamente comprueba que el valor de una variable es diferente a las de las otras:

problem.addConstraint(AllDifferentConstraint(), ['A', 'R'])

# Lo anterior, son tres formas diferentes de modelar la misma restriccion RA,R = [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]
# Ahora modelamos la restriccion de que Ruben y Felisa quieren trabajar en la misma parte RR,F={(1,1),(2,2),(3,3)}

problem.addConstraint(lambda a, b: a == b, ('R', 'F'))


# Por ultimo, modelamos la restriccion de que Yara hace una parte posterior a la que haga Ruben, RR,Y={(1,2),(1,3),(2,3)}

def consecutive(a, b):
	if b > a:
		return True

problem.addConstraint(consecutive, ('R', 'Y'))

# Una vez modelado el problema, podemos recuperar una de las soluciones:

print(problem.getSolution())

# o todas las soluciones:

print(problem.getSolutions())

"""