import tkinter as tk

import numpy

with open('inputs/input10.txt') as f:
    inputs = f.read()

input_matrix = []
y_matrix = []
x = 0
y = 0
entry_from = None
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

sp_paths = []

neighbours = {'bottom': start_coordinate_x + 1, 'right': start_coordinate_y + 1, 'left': start_coordinate_y - 1,
              'top': start_coordinate_x - 1}

top = ['|', '7', 'F']
bottom = ['|', 'J', 'L']
left = ['-', 'L', 'F']
right = ['-', 'J', '7']

# x-axis
for t in top:
    if input_matrix[neighbours['top']][start_coordinate_y] == t:
        sp_paths.append([neighbours['top'], start_coordinate_y, 'bottom'])
        break
for b in bottom:
    if input_matrix[neighbours['bottom']][start_coordinate_y] == b:
        sp_paths.append([neighbours['bottom'], start_coordinate_y, 'top'])
        break
for le in left:
    if input_matrix[start_coordinate_x][neighbours['left']] == le:
        sp_paths.append([start_coordinate_x, neighbours['left'], 'right'])
        break
for r in right:
    if input_matrix[start_coordinate_x][neighbours['right']] == r:
        sp_paths.append([start_coordinate_x, neighbours['right'], 'left'])
        break


def next_neighbour(current, c_x, c_y, entry):
    global input_matrix
    if current == '7':
        if inputs_matrix[c_x][c_y - 1] in left and entry == 'bottom':
            return c_x, c_y - 1, 'right'
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'left':
            return c_x + 1, c_y, 'top'
    if current == 'F':
        if inputs_matrix[c_x][c_y + 1] in right and entry == 'bottom':
            return c_x, c_y + 1, 'left'
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'right':
            return c_x + 1, c_y, 'top'
    if current == '-':
        if inputs_matrix[c_x][c_y + 1] in right and entry == 'left':
            return c_x, c_y + 1, 'left'
        if inputs_matrix[c_x][c_y - 1] in left and entry == 'right':
            return c_x, c_y - 1, 'right'
    if current == 'L':
        if inputs_matrix[c_x][c_y + 1] in right and entry == 'top':
            return c_x, c_y + 1, 'left'
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'right':
            return c_x - 1, c_y, 'bottom'
    if current == 'J':
        if inputs_matrix[c_x][c_y - 1] in left and entry == 'top':
            return c_x, c_y - 1, 'right'
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'left':
            return c_x - 1, c_y, 'bottom'
    if current == '|':
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'top':
            return c_x + 1, c_y, 'top'
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'bottom':
            return c_x - 1, c_y, 'bottom'
    return None


def travel(sp_paths):
    global x, y, entry_from
    traversed = [[], []]
    count = [1, 1]
    for p_index, path in enumerate(sp_paths):
        if not path:
            continue
        x, y, entry_from = path[0], path[1], path[2]
        c = input_matrix[x][y]
        result = next_neighbour(c, x, y, entry_from)
        if not result:
            sp_paths[p_index] = 0
            continue
        count[p_index] += 1
        new_x, new_y, new_entry_from = result
        if p_index:
            if input_matrix[new_x][new_y] in traversed[p_index - 1]:
                break
        else:
            if input_matrix[new_x][new_y] in traversed[p_index + 1]:
                break
        traversed[p_index].append([new_x, new_y])
        sp_paths[p_index] = [new_x, new_y, new_entry_from]
        return sp_paths


class LargeMatrixViewer:
    def __init__(self, root, matrix, start):
        self.root = root
        self.root.title("Large Matrix Viewer")

        self.matrix = matrix
        self.rows, self.columns = matrix.shape

        self.canvas = tk.Canvas(root, bg="white", width=1400, height=750)
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # self.starting_point = (0, 0)  # Set the starting point here
        self.starting_point = (start[0][0], start[0][1])  # Set the starting point here
        self.start_array = start
        self.animation_speed = 10  # Set the animation speed in milliseconds

        self.traversal_path = []
        self.current_position = self.starting_point

        self.animate_traversal()

        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def animate_traversal(self):
        if self.current_position:
            self.traversal_path.append(self.current_position)
            self.populate_canvas()

            val = travel(self.start_array)
            # Move to the next cell based on the specified direction
            self.current_position = (val[0][0], val[0][1])
            self.start_array = val

            # Add similar conditions for other directions

            self.root.after(self.animation_speed, self.animate_traversal)

    def populate_canvas(self):
        self.canvas.delete("all")  # Clear the canvas

        cell_width = 10
        cell_height = 10

        for i in range(self.rows):
            for j in range(self.columns):
                cell_value = self.matrix[i, j]
                char = cell_value

                if (i, j) == self.starting_point:
                    color = 'green'
                elif (i, j) in self.traversal_path:
                    color = 'red'
                else:
                    color = 'black'

                self.canvas.create_text(j * cell_width + cell_width / 2, i * cell_height + cell_height / 2,
                                        text=char, fill=color, font=('Arial', 8))

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


large_matrix = numpy.array(input_matrix)
root = tk.Tk()
viewer = LargeMatrixViewer(root, large_matrix, sp_paths)
# root.mainloop()
