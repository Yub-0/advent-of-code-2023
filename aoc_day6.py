from functools import reduce

time = [48, 87, 69, 81]
distance = [255, 1288, 1117, 1623]


# Part 1
def aoc_d6_part1():
    new_a = []
    for i in range(4):
        t = time[i]
        di = int(distance[i] / t)
        dif = t - di
        while True:
            if dif * di > distance[i]:
                new_a.append(dif - di + 1)
                break
            di += 1
            dif = dif - 1
    print(reduce(lambda x, y: x * y, new_a, 1))


# Part 2
def aoc_d6_part2(time0, distance0):
    time0 = int(''.join(map(str, time0)))
    distance0 = int(''.join(map(str, distance0)))
    di = int(distance0 / time0)
    dif = time0 - di
    while True:
        if dif * di > distance0:
            break
        di += 1
        dif = dif - 1
    print(dif - di + 1)


aoc_d6_part1()
aoc_d6_part2(time, distance)
