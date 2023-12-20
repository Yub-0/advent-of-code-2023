with open('inputs/input8.txt') as f:
    inputs = f.read()
inputs = inputs.split("\n")
directions = inputs[0]
inputs_len = len(inputs)
nodes = {}
current_node = 'AAA'
direction_len = len(directions)
starting_nodes = []

for i in range(2, inputs_len):
    main_node = inputs[i][0:3]
    if main_node[2] == 'A':
        starting_nodes.append(main_node)
    left_one = main_node + 'L'
    right_one = main_node + 'R'
    nodes[left_one] = inputs[i][7:10]
    nodes[right_one] = inputs[i][12:15]

count_in = 0


def rec_find(c_node, c_i):
    global count_in
    if c_i > direction_len - 1:
        return c_node
    count_in += 1
    dir_one = c_node + directions[c_i]
    current_node1 = nodes[dir_one]
    if current_node1 == 'ZZZ':
        return current_node1
    return rec_find(current_node1, c_i + 1)


def aoc_d8_p1():
    global current_node
    global count_in
    new_node = current_node
    while new_node != 'ZZZ':
        new_node = rec_find(new_node, 0)
    print(count_in)
    count_in = 0


# BRUTE FORCE
def find_part2_brute(n_nodes, c_index):
    global count_in
    check_f = [0] * len(n_nodes)
    if c_index > direction_len - 1:
        return n_nodes
    count_in += 1
    new_nodes = ['a'] * len(n_nodes)

    for node_index, node in enumerate(n_nodes):
        dir_one = node + directions[c_index]
        new_val = nodes[dir_one]
        new_nodes[node_index] = new_val
        if new_val[2] == 'Z':
            check_f[node_index] = 1
        if not check_f.count(0):
            return False
    return find_part2_brute(new_nodes, c_index + 1)


def find_part2_lcm(n_nodes, c_index, f_index):
    global count_in
    check_f = [0] * len(n_nodes)
    if c_index > direction_len - 1:
        return n_nodes
    count_in += 1
    new_nodes = ['a'] * len(n_nodes)
    for node_index, node in enumerate(n_nodes):
        dir_one = node + directions[c_index]
        new_val = nodes[dir_one]
        new_nodes[node_index] = new_val
        if new_val[2] == 'Z':
            f_index[node_index] = count_in
            check_f[node_index] = 1
        if not check_f.count(0):
            return False
    return find_part2_lcm(new_nodes, c_index + 1, f_index)


def aoc_d8_p2():
    # BRUTE  FORCE
    # while True:
    #     loop_nodes = find_part2_brute(loop_nodes, 0)
    #     if not loop_nodes:
    #         break
    # print(count_in)

    # LCM
    global starting_nodes
    loop_nodes = starting_nodes
    first_z_index = [0] * len(starting_nodes)
    while True:
        loop_nodes = find_part2_lcm(loop_nodes, 0, first_z_index)
        if not first_z_index.count(0):
            break

    import math
    print(math.lcm(*first_z_index))


aoc_d8_p1()
aoc_d8_p2()
