with open('inputs/input8.txt') as f:
    inputs = f.read()
inputs = inputs.split("\n")
directions = inputs[0]
inputs_len = len(inputs)
nodes_map = {}
directions_length = len(directions)
start_nodes = []
end_nodes = []

for i in range(2, inputs_len):
    main_node = inputs[i][0:3]
    if main_node[2] == 'A':
        start_nodes.append(main_node)
    if main_node[2] == 'Z':
        end_nodes.append(main_node)
    left_one = main_node + 'L'
    right_one = main_node + 'R'
    nodes_map[left_one] = inputs[i][7:10]
    nodes_map[right_one] = inputs[i][12:15]

###################################################################################
count = 0
prev_count = count
memo_direction_end = {}
memo_found = {}
current_direction_index = 0
current_node = start_nodes[0]
current_rest_of_node = start_nodes[1:len(start_nodes)]
current_direction_index_all = 0


def get_next_node(node, inc_index, k):
    global count
    op_node = node
    i_index = inc_index
    check_memo = str(inc_index) + node
    if check_memo in memo_found:
        count += memo_found[check_memo]['count']
        return memo_found[check_memo]['last_node'], memo_found[check_memo]['index'] + 1
    found_at = 0
    while True:
        count += 1
        found_at += 1
        if i_index > directions_length - 1:
            if node not in memo_direction_end:
                memo_direction_end[node] = op_node
            i_index = 0
            node = op_node
        dir_one = op_node + directions[i_index]
        new_node = nodes_map[dir_one]
        if new_node in end_nodes:
            if k not in memo_found:
                memo_found[k] = {
                    'count': found_at,
                    'last_node': new_node,
                    'index': i_index
                }
            return new_node, i_index + 1
        op_node = new_node
        i_index += 1


def traverse_one():
    global current_node
    global current_direction_index
    global count
    global prev_count
    index_node_key = str(current_direction_index) + current_node
    next_node, end_index = get_next_node(current_node, current_direction_index, index_node_key)
    current_node = next_node
    current_direction_index = end_index
    if current_direction_index > 262:
        current_direction_index = 0
    counter_f = count - prev_count
    prev_count = count
    return counter_f


def get_next_single_node(node, d_index):
    dir_one = node + directions[d_index]
    new_node = nodes_map[dir_one]
    return new_node


def get_next_last_node(node, d_index, counter1, k):
    s_node = node
    found_at = 0
    i_index = 0
    check_memo = str(0) + node
    if check_memo in memo_found:
        return memo_found[check_memo]['last_node']
    while counter1:
        found_at += 1
        if i_index > directions_length - 1:
            i_index = 0
        dir_one = s_node + directions[i_index]
        new_node = nodes_map[dir_one]
        counter1 -= 1
        i_index += 1
        s_node = new_node
    if k not in memo_found:
        memo_found[k] = {
            'count': found_at,
            'last_node': s_node,
            'index': i_index
        }
    return s_node


def traverse_all(count_er):
    global current_direction_index_all
    global current_rest_of_node
    traverse_nodes = current_rest_of_node
    for node_index, node in enumerate(traverse_nodes):
        lp = str(0) + node
        traverse_nodes[node_index] = get_next_last_node(node, current_direction_index_all, count_er, lp)
    current_rest_of_node = traverse_nodes
    return traverse_nodes


def check_z(nz):
    if nz[2] == 'Z':
        return 1
    return 0


def check_z_all(c_node):
    check_for_z = list(map(check_z, c_node))
    if not check_for_z.count(0):
        return True
    return False


while True:
    print(count)
    counter = traverse_one()
    check_node = traverse_all(counter)
    val = check_z_all(check_node)
    if val:
        print(count)
        break
