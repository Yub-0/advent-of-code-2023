with open('inputs/input8.txt') as f:
    inputs = f.read()
inputs = inputs.split("\n")
directions = inputs[0]
inputs_len = len(inputs)
nodes = {}
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
loop_nodes = starting_nodes


# numb = [18673, 15517, 20777, 11309, 13939, 17621]
# import math
# print(math.lcm(*numb))

def rec_find(n_nodes, c_index):
    global count_in
    global il
    check_f = [0] * len(n_nodes)
    if c_index > direction_len - 1:
        return n_nodes
    count_in += 1
    new_nodes = ['a'] * len(n_nodes)

    for node_index, node in enumerate(n_nodes):
        dir_one = node + directions[c_index]
        new_val = nodes[dir_one]
        new_nodes[node_index] = new_val
        # if node_index == 4:
        #     if new_val[2] == 'Z':
        #         print(count_in)
        #         print(new_val)
        if new_val[2] == 'Z':
            check_f[node_index] = 1
        if not check_f.count(0):
            return False
    return rec_find(new_nodes, c_index + 1)


print(loop_nodes)
