with open('inputs/input3.txt', 'r') as f:
    text = f.read()

t_array = []


def make_2d_array():
    i_array = []
    for lt in text:
        if lt == '\n':
            t_array.append(i_array)
            i_array = []
            continue
        i_array.append(lt)
    t_array.append(i_array)


make_2d_array()


def aoc_d3_part1():
    symbols = []
    text_set = set(text)

    for letter in text_set:
        if not letter.isdigit() and letter != '.' and letter != ' ' and letter != "\n":
            symbols.append(letter)

    def try_this(x, y):
        try:
            if x < 0 or y < 0:
                return '.'
            return t_array[x][y]
        except:
            return '.'

    def check_proximity(x, y):
        prox_array = [try_this(x - 1, y - 1), try_this(x - 1, y), try_this(x - 1, y + 1), try_this(x + 1, y + 1),
                      try_this(x + 1, y),
                      try_this(x + 1, y - 1), try_this(x, y - 1), try_this(x, y + 1)]
        for sy in symbols:
            if sy in prox_array:
                return True
        return False

    sum1 = 0
    sym_flag = False
    s = ''
    for r_index, row in enumerate(t_array):
        for i_index, item in enumerate(row):
            if not item.isdigit():
                if sym_flag:
                    sum1 += int(s)
                    sym_flag = False
                s = ''
                continue
            s += item
            if not sym_flag:
                sym_flag = check_proximity(r_index, i_index)
    print(sum1)


def aoc_d3_part2():
    def try_this(x, y):
        try:
            if x < 0 or y < 0 or not t_array[x][y].isdigit():
                return '.'
            left_flag = y - 1
            right_flag = y + 1
            s = t_array[x][y]
            if left_flag >= 0:
                t_l = t_array[x][left_flag]
                while t_l.isdigit():
                    s = t_l + s
                    left_flag -= 1
                    if left_flag < 0:
                        break
                    t_l = t_array[x][left_flag]
            if right_flag <= len(t_array) - 1:
                r_l = t_array[x][right_flag]
                while r_l.isdigit():
                    s = s + t_array[x][right_flag]
                    right_flag += 1
                    if right_flag > len(t_array) - 1:
                        break
                    r_l = t_array[x][right_flag]
            return s
        except:
            return '.'

    def check_proximity(x, y):
        prox_array = [try_this(x - 1, y - 1), try_this(x - 1, y),
                      try_this(x - 1, y + 1), try_this(x + 1, y + 1),
                      try_this(x + 1, y), try_this(x + 1, y - 1),
                      try_this(x, y - 1), try_this(x, y + 1)]
        prox_array = set(prox_array)
        prox_array.discard('.')
        return prox_array

    sum1 = 0
    i = 0
    for r_index, row in enumerate(t_array):
        for i_index, item in enumerate(row):
            if item == '*':
                proximity_set = check_proximity(r_index, i_index)
                proximity_set = list(proximity_set)
                if len(proximity_set) == 2:
                    i += 1
                    sum1 = sum1 + (int(proximity_set[0]) * int(proximity_set[1]))
    # 80071063 too low
    # 80541603 too high
    print(sum1)


aoc_d3_part1()
aoc_d3_part2()
