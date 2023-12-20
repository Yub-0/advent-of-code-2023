import pandas as pd

df = pd.read_csv("inputs/input4.csv", header=None)


def convert_to_array(ser):
    ser = ser.split(' ')
    ser = [int(a) for a in ser if a]
    return ser


def aoc_d4_part1():
    sum1 = 0
    for i, row in df.iterrows():
        win, have = split_ant_convert(row[0])
        count = 0
        for w in win:
            if w in have:
                count += 1
        if count:
            sum1 += pow(2, count - 1)

    print(sum1)


def split_ant_convert(row):
    win_and_have = row.split(':')[1]
    win = win_and_have.split("|")[0]
    have = win_and_have.split("|")[1]
    win = convert_to_array(win)
    have = convert_to_array(have)
    return win, have


def aoc_d4_part2():
    total_cards = len(df)
    cards = {}

    for i in range(1, total_cards + 1, 1):
        cards['card' + str(i)] = 1

    for i, row in df.iterrows():
        i += 1
        current_card = 'card' + str(i)
        win, have = split_ant_convert(row[0])
        count = 0
        for w in win:
            if w in have:
                count += 1
        for n_card in range(cards[current_card]):
            for c in range(1, count + 1, 1):
                s = 'card' + str(i + c)
                cards[s] += 1

    new_a = [cards[key] for key in cards]
    print(sum(new_a))


aoc_d4_part1()
aoc_d4_part2()