import pandas as pd

df = pd.read_csv("inputs/input2.csv", header=None)

games = {}


def rearrange_balls():
    for index, row in df.iterrows():
        g_s = 'game' + str(index + 1)
        game_sets = row.iloc[0].split(':')[1]
        game_sets = game_sets.split(';')
        new_d = {}
        for i, s in enumerate(game_sets):
            new_d['set' + str(i + 1)] = s
        if new_d:
            games[g_s] = new_d


# Part 1
def aoc_d2_part1():
    rearrange_balls()
    rule = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    sum1 = 0
    for key in games:
        add_this = True
        for key2 in games[key]:
            detail = games[key][key2]
            detail = detail.split(',')
            n_d = {}
            for d in detail:
                d_split = d.split(' ')
                n_d[d_split[2]] = int(d_split[1])
                if rule[d_split[2]] < n_d[d_split[2]]:
                    games[key] = None
            if not games[key]:
                add_this = False
                break
            games[key][key2] = n_d
        if add_this:
            sum1 = sum1 + int(key.split('game')[1])
    print(sum1)


# Part 2
def aoc_d2_part2():
    rearrange_balls()
    sum1 = 0
    for key in games:
        n_d = {}
        for key2 in games[key]:
            detail = games[key][key2]
            detail = detail.split(',')
            for d in detail:
                d_split = d.split(' ')
                if d_split[2] not in n_d:
                    n_d[d_split[2]] = int(d_split[1])
                    continue
                if int(d_split[1]) > n_d[d_split[2]]:
                    n_d[d_split[2]] = int(d_split[1])
        games[key] = n_d
    for key in games:
        mul_c = 0
        for key2 in games[key]:
            if not mul_c:
                mul_c = games[key][key2]
                continue
            mul_c = mul_c * games[key][key2]
        sum1 = sum1 + mul_c
    print(sum1)


aoc_d2_part1()
aoc_d2_part2()
