with open('inputs/input9.txt') as f:
    inputs = f.read()
inputs = inputs.split('\n')

corrected_input = [[]] * len(inputs)

for index, string_numbers in enumerate(inputs):
    numbers = string_numbers.split()
    numbers = [int(num) for num in numbers]
    corrected_input[index] = numbers


def forward_interpolate(seq, b_value):
    b_value += seq[-1]
    new_seq = [0] * (len(seq) - 1)
    for i, num in enumerate(seq):
        if i != len(seq) - 1:
            new_seq[i] = seq[i + 1] - seq[i]
    test_new_seq = set(new_seq)
    if len(test_new_seq) == 1:
        b_value += list(test_new_seq)[0]
        return b_value
    return forward_interpolate(new_seq, b_value)


def aoc_d9_p1():
    new_numb = 0
    for c_input in corrected_input:
        buffer_value = 0
        new_numb += forward_interpolate(c_input, buffer_value)
    print(new_numb)


def backward_interpolate(seq, st):
    new_seq = [0] * (len(seq) - 1)
    for i, num in enumerate(seq):
        if i != len(seq) - 1:
            new_seq[i] = seq[i + 1] - seq[i]
    test_new_seq = set(new_seq)
    if len(test_new_seq) == 1:
        val = list(test_new_seq)[0]
        for n_i, n in enumerate(st[::-1]):
            val = n - val
        return val
    st.append(new_seq[0])
    return backward_interpolate(new_seq, st)


def aoc_d9_p2():
    new_numb = 0
    for c_input in corrected_input:
        buffer_list = [c_input[0]]
        new_numb += backward_interpolate(c_input, buffer_list)
    print(new_numb)


aoc_d9_p1()
aoc_d9_p2()
