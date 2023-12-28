import tkinter as tk
from collections import deque
import numpy
from PIL import Image, ImageTk

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

top = ['|', '7', 'F']
bottom = ['|', 'J', 'L']
left = ['-', 'L', 'F']
right = ['-', 'J', '7']

# x-axis
if input_matrix[start_coordinate_x - 1][start_coordinate_y] in top:
    sp_paths.append([start_coordinate_x - 1, start_coordinate_y, 'bottom'])
if input_matrix[start_coordinate_x + 1][start_coordinate_y] in bottom:
    sp_paths.append([start_coordinate_x + 1, start_coordinate_y, 'top'])
if input_matrix[start_coordinate_x][start_coordinate_y - 1] in left:
    sp_paths.append([start_coordinate_x, start_coordinate_y - 1, 'right'])
if input_matrix[start_coordinate_x][start_coordinate_y + 1] in right:
    sp_paths.append([start_coordinate_x, start_coordinate_y + 1, 'left'])


def next_neighbour(current, c_x, c_y, entry):
    global input_matrix, left, right, bottom, top
    if current == '7':
        e = inputs_matrix[c_x][c_y - 1]
        if e in left and entry == 'bottom':
            if e == '-':
                ex = 'left'
            elif e == 'L':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y - 1, 'right', ex
        e = inputs_matrix[c_x + 1][c_y]
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'left':
            if e == '|':
                ex = 'bottom'
            elif e == 'J':
                ex = 'left'
            else:
                ex = 'right'
            return c_x + 1, c_y, 'top', ex
    if current == 'F':
        e = inputs_matrix[c_x][c_y + 1]
        if e in right and entry == 'bottom':
            if e == '-':
                ex = 'right'
            elif e == 'J':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y + 1, 'left', ex
        e = inputs_matrix[c_x + 1][c_y]
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'right':
            if e == '|':
                ex = 'bottom'
            elif e == 'J':
                ex = 'left'
            else:
                ex = 'right'
            return c_x + 1, c_y, 'top', ex
    if current == '-':
        e = inputs_matrix[c_x][c_y + 1]
        if inputs_matrix[c_x][c_y + 1] in right and entry == 'left':
            if e == '-':
                ex = 'right'
            elif e == 'J':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y + 1, 'left', ex
        e = inputs_matrix[c_x][c_y - 1]
        if inputs_matrix[c_x][c_y - 1] in left and entry == 'right':
            if e == '-':
                ex = 'left'
            elif e == 'L':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y - 1, 'right', ex
    if current == 'L':
        e = inputs_matrix[c_x][c_y + 1]
        if inputs_matrix[c_x][c_y + 1] in right and entry == 'top':
            if e == '-':
                ex = 'right'
            elif e == 'J':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y + 1, 'left', ex

        e = inputs_matrix[c_x - 1][c_y]
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'right':
            if e == '|':
                ex = 'top'
            elif e == '7':
                ex = 'left'
            else:
                ex = 'right'
            return c_x - 1, c_y, 'bottom', ex
    if current == 'J':
        e = inputs_matrix[c_x][c_y - 1]
        if inputs_matrix[c_x][c_y - 1] in left and entry == 'top':
            if e == '-':
                ex = 'left'
            elif e == 'L':
                ex = 'top'
            else:
                ex = 'bottom'
            return c_x, c_y - 1, 'right', ex
        e = inputs_matrix[c_x - 1][c_y]
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'left':
            if e == '|':
                ex = 'top'
            elif e == '7':
                ex = 'left'
            else:
                ex = 'right'
            return c_x - 1, c_y, 'bottom', ex
    if current == '|':
        e = inputs_matrix[c_x + 1][c_y]
        if inputs_matrix[c_x + 1][c_y] in bottom and entry == 'top':
            if e == '|':
                ex = 'bottom'
            elif e == 'J':
                ex = 'left'
            else:
                ex = 'right'
            return c_x + 1, c_y, 'top', ex

        e = inputs_matrix[c_x - 1][c_y]
        if inputs_matrix[c_x - 1][c_y] in top and entry == 'bottom':
            if e == '|':
                ex = 'top'
            elif e == '7':
                ex = 'left'
            else:
                ex = 'right'
            return c_x - 1, c_y, 'bottom', ex
    return None


traversed = []
potential_inside_points = deque([])


def get_inside_points(x1, y1, c_neigh):
    global potential_inside_points, traversed
    if c_neigh == 'bottom':
        x1 = x1 + 1
    elif c_neigh == 'top':
        x1 = x1 - 1
    elif c_neigh == 'left':
        y1 = y1 - 1
    elif c_neigh == 'right':
        y1 = y1 + 1
    return x1, y1


def travel(path, rule, c_ne):
    global x, y, entry_from, traversed, potential_inside_points
    check_ne = c_ne
    edge = ['J', 'L', '7', 'F']
    x, y, entry_from, exit_at = path[0], path[1], path[2], path[3]
    c = input_matrix[x][y]
    result = next_neighbour(c, x, y, entry_from)
    if not result:
        return 0
    new_x, new_y, new_entry_from, new_exit_at = result
    if (new_x, new_y) in potential_inside_points:
        potential_inside_points.remove((new_x, new_y))
    new_point = input_matrix[new_x][new_y]
    if new_point == 'S':
        return 0
    p_i = None
    if new_point in edge:
        r = f'{new_entry_from[0]}-{new_exit_at[0]}'
        check_ne = rule[r]
        if new_point == 'L' and new_entry_from[0] == 'r':
            potential_inside_points.append((new_x + 1, new_y))
            potential_inside_points.append((new_x, new_y - 1))
        if new_point == 'J' and new_entry_from[0] == 't':
            potential_inside_points.append((new_x, new_y + 1))
            potential_inside_points.append((new_x + 1, new_y))
        if new_point == '7' and new_entry_from[0] == 'l':
            potential_inside_points.append((new_x, new_y + 1))
            potential_inside_points.append((new_x - 1, new_y))
        if new_point == 'F' and new_entry_from[0] == 'b':
            potential_inside_points.append((new_x, new_y - 1))
            potential_inside_points.append((new_x - 1, new_y))
    else:
        p_i = get_inside_points(new_x, new_y, check_ne)
        if p_i not in traversed:
            potential_inside_points.append(p_i)
        else:
            p_i = None
    traversed.append((new_x, new_y))
    path[0], path[1], path[2], path[3] = result
    # print(len(potential_inside_points))
    return path, check_ne, p_i


class LargeMatrixViewer:
    def __init__(self, root, matrix, start):
        self.root = root
        self.root.title("Large Matrix Viewer")
        self.rules = {
            'b-l': 'bottom', 'r-b': 'right', 't-r': 'top', 'l-t': 'left', 'b-r': 'top', 'l-b': 'right', 't-l': 'bottom',
            'r-t': 'left',
        }
        self.matrix = matrix
        self.rows, self.columns = matrix.shape
        self.path_count = {'blue': 1, 'red': 1}
        self.check_neighbour_at = 'bottom'
        self.counter = tk.Canvas(root, bg="white", width=1400, height=20)
        self.counter.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.image_map = {
            'I': None,
            'J': None,
            'L': None,
            'F': None,
            '7': None,
            'd': None
        }
        for key in self.image_map:
            path = 'C:/Users/yub/Desktop/img/' + key + '.png'
            img = Image.open(path)
            img = img.resize((10, 10), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_map[key] = img

        self.canvas = tk.Canvas(root, bg="white", width=1400, height=750)

        self.canvas.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.starting_points = start  # Set the starting point here

        self.animation_speed = 10  # Set the animation speed in milliseconds

        self.traversal_path = []
        self.current_positions = self.starting_points

        self.c_maps = {}  # dict for matrix cells created by create_text
        self.p_maps = {}  # dict for counter cells created by create_text

        self.canvas_done = False
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.animate_traversal()

    def animate_traversal(self):
        global potential_inside_points, traversed

        prev = self.current_positions

        if not self.canvas_done:
            self.create_the_canvas()
            self.canvas_done = True
        else:
            res = travel(self.current_positions, self.rules, self.check_neighbour_at)
            if res:
                self.current_positions, self.check_neighbour_at, pot_in_path = res
                color = 'red'
                self.path_count[color] += 1
                self.traversal_path.append((self.current_positions[0], self.current_positions[1]))
                self.update_canvas(self.current_positions[0], self.current_positions[1], color)
            else:
                self.current_positions = None
        if self.current_positions:
            self.root.after(self.animation_speed, self.animate_traversal)
        else:
            p_x, p_y = prev[0], prev[1]
            p_c = 'red'
            update_text = f'{p_c}:{self.path_count[p_c] + 1}'
            self.counter.itemconfigure(self.p_maps[p_c], text=update_text)
            c_item = self.c_maps[str(p_x) + ',' + str(p_y)]['cell']
            self.canvas.itemconfigure(c_item, fill='green')
            len_p = 0
            new_inside_points = []

            def check_neighbours(in_p):
                inside_point_x, inside_point_y = in_p[0], in_p[1]
                ele_list = [(inside_point_x - 1, inside_point_y), (inside_point_x + 1, inside_point_y),
                            (inside_point_x, inside_point_y - 1), (inside_point_x, inside_point_y + 1)]
                for element in ele_list:
                    if element not in potential_inside_points and element not in traversed and element not in new_inside_points:
                        new_inside_points.append(element)
                        check_neighbours(element)

            for pp in set(potential_inside_points):
                if pp not in traversed:
                    len_p += 1
                    c_item = self.c_maps[str(pp[0]) + ',' + str(pp[1])]['cell']
                    self.canvas.itemconfigure(c_item, fill='blue')
                    self.canvas.update()
                    check_neighbours(pp)
            for in_points in set(new_inside_points):
                len_p += 1
                c_item = self.c_maps[str(in_points[0]) + ',' + str(in_points[1])]['cell']
                self.canvas.itemconfigure(c_item, fill='blue')
                self.canvas.update()
            print(len_p)
            self.canvas.update()

    def update_canvas(self, a, b, c):
        matrix_character = input_matrix[a][b]
        cell_to_update = self.c_maps[str(a) + ',' + str(b)]
        c_item = cell_to_update['cell']
        x0 = cell_to_update['x0']
        y0 = cell_to_update['y0']
        self.canvas.delete(c_item)

        if matrix_character == '-':
            r_img = self.image_map['d']
        elif matrix_character == 'J':
            r_img = self.image_map['J']
        elif matrix_character == '7':
            r_img = self.image_map['7']
        elif matrix_character == 'F':
            r_img = self.image_map['F']
        elif matrix_character == '|':
            r_img = self.image_map['I']
        else:
            r_img = self.image_map['L']

        self.canvas.create_image(x0, y0, anchor=tk.NW, image=r_img)

        update_text = f'{c}:{self.path_count[c]}'
        self.counter.itemconfigure(self.p_maps[c], text=update_text)
        self.canvas.update()
        self.canvas.update_idletasks()

    def create_the_canvas(self):
        self.canvas.delete("all")  # Clear the canvas

        cell_width = 10
        cell_height = 10
        for i in range(self.rows):
            for j in range(self.columns):
                char = self.matrix[i, j]
                x0 = j * cell_width
                y0 = i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height

                text_item = self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=char, fill='black',
                                                    font=('Consolas', 7, 'bold'))
                self.c_maps[str(i) + ',' + str(j)] = {
                    'cell': text_item,
                    'x0': x0,
                    'x1': x1,
                    'y0': y0,
                    'y1': y1
                }

        c_item = self.c_maps[str(self.starting_points[0]) + ',' + str(self.starting_points[1])]['cell']
        self.canvas.itemconfigure(c_item, fill='green')
        self.canvas.update()

        m = 100
        for c_index, co in enumerate(self.path_count):
            p_count = f'{co}:{self.path_count[co]}'
            self.p_maps[co] = self.counter.create_text(m, 12, text=p_count, fill='black',
                                                       font=('Consolas', 9, 'bold'))
            m = m * 4

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


large_matrix = numpy.array(input_matrix)
rt = tk.Tk()
sp_paths[0].append('left')
viewer = LargeMatrixViewer(rt, large_matrix, sp_paths[0])
rt.mainloop()
