import tkinter as tk
import numpy

with open('./inputs/input10.txt') as f:
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
        input_matrix.append(y_matrix)
        y_matrix = []
        x += 1
        y = 0
        continue
    y_matrix.append(input1)
input_matrix.append(y_matrix)

top = ['|', '7', 'F']
bottom = ['|', 'J', 'L']
left = ['-', 'L', 'F']
right = ['-', 'J', '7']

sp_paths = []  # List to store the starting points

# Finding the starting paths from 'S'
if input_matrix[start_coordinate_x - 1][start_coordinate_y] in top:
    sp_paths.append([start_coordinate_x - 1, start_coordinate_y, 'bottom'])
if input_matrix[start_coordinate_x + 1][start_coordinate_y] in bottom:
    sp_paths.append([start_coordinate_x + 1, start_coordinate_y, 'top'])
if input_matrix[start_coordinate_x][start_coordinate_y - 1] in left:
    sp_paths.append([start_coordinate_x, start_coordinate_y - 1, 'right'])
if input_matrix[start_coordinate_x][start_coordinate_y + 1] in right:
    sp_paths.append([start_coordinate_x, start_coordinate_y + 1, 'left'])


def next_neighbour(c_x, c_y, entry):
    global input_matrix, left, right, bottom, top
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


traversed = [[], []]


def travel(s_paths):
    global traversed
    for p_index, path in enumerate(s_paths):
        if not path:
            continue
        x_coordinate, y_coordinate, entry_point = path[0], path[1], path[2]
        result = next_neighbour(x_coordinate, y_coordinate, entry_point)
        if not result:
            s_paths[p_index] = 0
            continue
        new_x_coordinate, new_y_coordinate, new_entry_point = result
        if p_index:
            if (new_x_coordinate, new_y_coordinate) in traversed[p_index - 1]:
                return None
        else:
            if (new_x_coordinate, new_y_coordinate) in traversed[p_index + 1]:
                return None
        traversed[p_index].append((new_x_coordinate, new_y_coordinate))
        s_paths[p_index][0], s_paths[p_index][1], s_paths[p_index][2] = result
    return s_paths


class LargeMatrixViewer:
    def __init__(self, root, matrix, start):
        self.root = root
        self.root.title("Large Matrix Viewer")

        self.matrix = matrix
        self.rows, self.columns = matrix.shape

        # Counter for length travelled by each path indicated with different colors
        self.path_count = {'blue': 1, 'red': 1}
        self.counter = tk.Canvas(root, bg="white", width=1400, height=20)
        self.counter.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.canvas = tk.Canvas(root, bg="white", width=1400, height=750)
        self.canvas.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # self.starting_point = (0, 0)  # Set the starting point here
        self.starting_points = start  # Set the starting point here
        self.starting_p = [(s_point[0], s_point[1]) for s_point in self.starting_points]
        self.animation_speed = 10  # Set the animation speed in milliseconds

        self.traversal_path = []
        self.current_positions = self.starting_points

        self.c_maps = {}  # dict to store object id of each cell on the canvas created by create_text
        self.p_maps = {}  # dict to store object id of counter cells on the canvas created by create_text

        self.canvas_done = False

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.animate_traversal()

    def animate_traversal(self):
        if not self.canvas_done:
            self.create_the_canvas()
            self.canvas_done = True
        else:
            for pindex, pos in enumerate(self.current_positions):
                if pos:
                    if pindex % 2 == 0:
                        color = 'red'
                    else:
                        color = 'blue'
                    self.path_count[color] += 1
                    self.traversal_path.append((pos[0], pos[1]))
                    self.update_canvas(pos[0], pos[1], color)

        prev = self.current_positions

        # Move to the next cell based on the specified direction
        self.current_positions = travel(self.current_positions)
        if self.current_positions:
            self.root.after(self.animation_speed, self.animate_traversal)
        else:
            if prev[0]:
                p_x, p_y = prev[0][0], prev[0][1]
            else:
                p_x, p_y = prev[1][0], prev[1][1]

            for p_c in self.path_count:
                update_text = f'{p_c}:{self.path_count[p_c] + 1}'
                self.counter.itemconfigure(self.p_maps[p_c], text=update_text)

            c_item = self.c_maps[str(p_x) + ',' + str(p_y)]
            self.canvas.itemconfigure(c_item, fill='green')
            self.canvas.update()

    def update_canvas(self, a, b, c):
        c_item = self.c_maps[str(a) + ',' + str(b)]
        self.canvas.itemconfigure(c_item, fill=c)
        update_text = f'{c}:{self.path_count[c]}'
        self.counter.itemconfigure(self.p_maps[c], text=update_text)
        self.canvas.update()

    def create_the_canvas(self):
        cell_width = 10
        cell_height = 10

        for i in range(self.rows):
            for j in range(self.columns):
                char = self.matrix[i, j]

                if (i, j) in self.starting_p:
                    color = 'green'
                else:
                    color = 'black'

                # Each cell filled with characters from the 2d matrix
                self.c_maps[str(i) + ',' + str(j)] = self.canvas.create_text(j * cell_width + cell_width / 2,
                                                                             i * cell_height + cell_height / 2,
                                                                             text=char, fill=color, font=('Consolas', 7, 'bold'))
        # Counter set on Canvas
        m = 100
        for c_index, co in enumerate(self.path_count):
            p_count = f'{co}:{self.path_count[co]}'
            self.p_maps[co] = self.counter.create_text(m, 12, text=p_count, fill='black', font=('Consolas', 9, 'bold'))
            m = m * 4

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


large_matrix = numpy.array(input_matrix)
rt = tk.Tk()
viewer = LargeMatrixViewer(rt, large_matrix, sp_paths)
rt.mainloop()
