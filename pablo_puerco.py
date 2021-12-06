position_matrix = [["N", "N","N", "N"],
                   ["N", "N", "N", "N"],
                   ["E", "N", "N", "E"],
                   ["X", "E", "E", "X"],
                   ["X", "X", "X", "X"]]

i = len(position_matrix)
j = len(position_matrix[0])
not_floor_list = []
for i in reversed(position_matrix):
    for j in reversed(position_matrix[0]):
        element = position_matrix[i][j]
        if element == "X" and j not in not_floor_list:
            position_matrix[i][j]="F"
        elif element =="X" and position_matrix[i][j-1]!="F":
            not_floor_list.append(j)

print(position_matrix)