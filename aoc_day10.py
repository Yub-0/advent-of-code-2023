from collections import deque

with open('inputs/input10.txt') as f:
    inputs = f.read()

input_matrix = []
y_matrix = []
x = 0
y = 0
start_coordinate_x, start_coordinate_y = 0, 0

for input1 in inputs:
    if input1 == 'S':
        start_coordinate_x, start_coordinate_y = x, y
    y += 1
    if input1 == '\n':
        x += 1
        input_matrix.append(y_matrix)
        y_matrix = []
        y = 0
        continue
    y_matrix.append(input1)
input_matrix.append(y_matrix)

top = ['|', '7', 'F']
bottom = ['|', 'J', 'L']
left = ['-', 'L', 'F']
right = ['-', 'J', '7']
starting_paths = []
# x-axis

if input_matrix[start_coordinate_x - 1][start_coordinate_y] in top:
    starting_paths.append([start_coordinate_x - 1, start_coordinate_y, 'bottom'])
if input_matrix[start_coordinate_x + 1][start_coordinate_y] in bottom:
    starting_paths.append([start_coordinate_x + 1, start_coordinate_y, 'top'])
if input_matrix[start_coordinate_x][start_coordinate_y - 1] in left:
    starting_paths.append([start_coordinate_x, start_coordinate_y - 1, 'right'])
if input_matrix[start_coordinate_x][start_coordinate_y + 1] in right:
    starting_paths.append([start_coordinate_x, start_coordinate_y + 1, 'left'])


def next_neighbour(c_x, c_y, entry):
    global input_matrix, left, right, top, bottom
    current = input_matrix[c_x][c_y]
    if current == '7':
        if input_matrix[c_x][c_y - 1] in left and entry == 'bottom':
            return c_x, c_y - 1, 'right'
        if input_matrix[c_x + 1][c_y] in bottom and entry == 'left':
            return c_x + 1, c_y, 'top'
    if current == 'F':
        if input_matrix[c_x][c_y + 1] in right and entry == 'bottom':
            return c_x, c_y + 1, 'left'
        if input_matrix[c_x + 1][c_y] in bottom and entry == 'right':
            return c_x + 1, c_y, 'top'
    if current == '-':
        if input_matrix[c_x][c_y + 1] in right and entry == 'left':
            return c_x, c_y + 1, 'left'
        if input_matrix[c_x][c_y - 1] in left and entry == 'right':
            return c_x, c_y - 1, 'right'
    if current == 'L':
        if input_matrix[c_x][c_y + 1] in right and entry == 'top':
            return c_x, c_y + 1, 'left'
        if input_matrix[c_x - 1][c_y] in top and entry == 'right':
            return c_x - 1, c_y, 'bottom'
    if current == 'J':
        if input_matrix[c_x][c_y - 1] in left and entry == 'top':
            return c_x, c_y - 1, 'right'
        if input_matrix[c_x - 1][c_y] in top and entry == 'left':
            return c_x - 1, c_y, 'bottom'
    if current == '|':
        if input_matrix[c_x + 1][c_y] in bottom and entry == 'top':
            return c_x + 1, c_y, 'top'
        if input_matrix[c_x - 1][c_y] in top and entry == 'bottom':
            return c_x - 1, c_y, 'bottom'
    return None


def aoc_d10_p1():
    global starting_paths
    s_paths = starting_paths
    traversed = [[(starting_paths[0][0], starting_paths[0][1])], [(starting_paths[1][0], starting_paths[1][1])]]
    flag = True
    while flag:
        for index, path in enumerate(s_paths):
            if not path:
                continue
            x1, y1, entry_point = path
            result = next_neighbour(x1, y1, entry_point)
            if not result:
                s_paths[index] = 0
                continue
            new_x, new_y, new_entry_from = result
            if index:
                if (new_x, new_y) in traversed[index - 1]:
                    flag = False
            else:
                if (new_x, new_y) in traversed[index + 1]:
                    flag = False
            traversed[index].append((new_x, new_y))
            s_paths[index][0], s_paths[index][1], s_paths[index][2] = result

    print(len(traversed[0]), len(traversed[1]))


aoc_d10_p1()
