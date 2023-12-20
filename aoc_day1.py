import pandas as pd
import inflect

pd.set_option('display.max_rows', None)
df = pd.read_csv('inputs/input1.csv', header=None)


# Part 1
def is_digit(el):
    if el.isdigit():
        return el


def aoc_d1_part1():
    sum1 = 0
    for i, row in df.iterrows():
        digits = map(is_digit, row[0])
        digits = [a for a in list(digits) if a]
        sum1 = sum1 + int(digits[0] + digits[len(digits) - 1])
    print(sum1)


# Part 2
def no_to_words():
    n_to_w_dic = {}
    p = inflect.engine()
    for n in range(9, -1, - 1):
        word = p.number_to_words(n)
        n_to_w_dic[word] = str(n)
    return n_to_w_dic


def aoc_d1_part2():
    dic = no_to_words()
    sum1 = 0
    for i, row in df.iterrows():
        new_s = ''
        for s in row.iloc[0]:
            new_s += s
            for key in dic:
                if key in new_s:
                    new_s += new_s[len(new_s) - 1]
                    new_s = new_s.replace(key, dic[key])
        row.iloc[0] = new_s
        digits = map(is_digit, row.iloc[0])
        digits = [a for a in list(digits) if a]
        sum1 = sum1 + int(digits[0] + digits[len(digits) - 1])
    print(sum1)


aoc_d1_part1()
aoc_d1_part2()
