import numpy

MULTIPLIER = 1_000_000  # for part 2
# MULTIPLIER = 10
# MULTIPLIER = 2 # for part 1

with open('inputs/input11.txt') as f:
    inputs = f.read()

input_matrix = []
row = []
row_index = 0
row_with_no_galaxies = {}
for i_index, input1 in enumerate(inputs):
    if input1 == '\n':
        if '#' not in row:
            row_with_no_galaxies[row_index] = row
        input_matrix.append(row)
        row_index += 1
        row = []
        continue
    row.append(input1)
else:
    if '#' not in row:
        row_with_no_galaxies[row_index] = row
    input_matrix.append(row)

input_matrix = numpy.array(input_matrix)
transposed_input_matrix = input_matrix.transpose(-1, 0)

row_index = 0
col_with_no_galaxies = {}
for input1 in transposed_input_matrix:
    if '#' not in input1:
        col_with_no_galaxies[row_index] = input1
    row_index += 1

input_matrix = transposed_input_matrix.transpose(-1, 0)

sum_distance = 0


def find_distance(current_row, current_galaxy_index, universe):
    global sum_distance, row_with_no_galaxies, col_with_no_galaxies, MULTIPLIER
    part_universe = universe
    for row_from_cr, g_row in enumerate(part_universe):
        row_from_cr += 1
        if '#' not in g_row:
            continue
        compare_row = current_row + row_from_cr
        no_empty_row = 0
        for empty_row in row_with_no_galaxies:
            if current_row < empty_row < compare_row:
                no_empty_row += 1
        for galaxy_index, gal in enumerate(g_row):
            no_empty_col = 0
            if '#' not in g_row[galaxy_index:len(g_row)]:
                continue
            if gal == '#':
                if galaxy_index == current_galaxy_index:
                    pass
                elif galaxy_index > current_galaxy_index:
                    for c_key in col_with_no_galaxies:
                        if current_galaxy_index < c_key < galaxy_index:
                            no_empty_col += 1
                else:
                    for c_key in col_with_no_galaxies:
                        if current_galaxy_index > c_key > galaxy_index:
                            no_empty_col += 1
                val = (abs(galaxy_index - current_galaxy_index) + row_from_cr - no_empty_col - no_empty_row +
                       (no_empty_col * MULTIPLIER) + (no_empty_row * MULTIPLIER))
                # print(f'g{galaxy_index}-g{current_galaxy_index}:{val}, {galaxy_index}, {current_galaxy_index},'
                #       f'{no_empty_col}, {no_empty_row}')
                sum_distance += val


for index, r in enumerate(input_matrix):
    if '#' not in r:
        continue
    galaxy_a = []
    for b_index, body in enumerate(r):
        if '#' not in r[b_index:len(r)]:
            continue
        if body == '#':
            galaxy_a.append(b_index)
            find_distance(index, b_index, input_matrix[index + 1:len(input_matrix)])
    if len(galaxy_a) > 1:
        sum_distance = sum_distance
        for i, g in enumerate(galaxy_a):
            if i == len(galaxy_a) - 1:
                break
            for sub_g in galaxy_a[i + 1:len(galaxy_a)]:
                no_of_empty_col_in_between = 0
                for c in col_with_no_galaxies:
                    if g < c < sub_g:
                        no_of_empty_col_in_between += 1
                sum_distance += abs(g - sub_g) + (no_of_empty_col_in_between * MULTIPLIER) - no_of_empty_col_in_between

print(sum_distance)
