seeds = [2149186375, 163827995, 1217693442, 67424215, 365381741, 74637275, 1627905362, 77016740, 22956580, 60539394, 586585112,
         391263016, 2740196667, 355728559, 2326609724, 132259842, 2479354214, 184627854, 3683286274, 337630529]

with open("inputs/input5.txt") as f:
    para = f.read()

para = para.split(':')

all_maps = {}

mapping_keys = ['seed_soil_map', 'soil_fertilizer_map', 'fertilizer_water_map', 'water_light_map', 'light_temperature-map',
                'temperature_humidity_map', 'humidity_location_map']
map_item_1 = ['seed_value', 'soil_value', 'fertilizer_value', 'water_value', 'light_value',
              'temperature_value', 'humidity_value']
map_item_2 = ['soil_value', 'fertilizer_value', 'water_value', 'light_value', 'temperature_value',
              'humidity_value', 'location_value']

for index, p in enumerate(para):
    all_maps[mapping_keys[index]] = []
    filtered_list = [item for item in p.split('\n') if item != '']
    for row in filtered_list:
        items = row.split(' ')
        d = {map_item_1[index]: int(items[1]), map_item_2[index]: int(items[0]), 'range': int(items[2])}
        all_maps[mapping_keys[index]].append(d)

    all_maps[mapping_keys[index]] = sorted(all_maps[mapping_keys[index]], key=lambda x: x[map_item_1[index]])


# Part 1
def map_this(key_array, ind):
    new_l = []
    for key in key_array:
        for ssm in all_maps[mapping_keys[ind]]:
            if ssm[map_item_1[ind]] <= key <= (ssm[map_item_1[ind]] + ssm['range']):
                dif = key - ssm[map_item_1[ind]]
                new_l.append(ssm[map_item_2[ind]] + dif)
    if ind == 6:
        return new_l
    return map_this(new_l, ind + 1)


def aoc_d5_part1():
    result = map_this(seeds, 0)
    print(min(result))


# Test single seed
# def map_single_seed(s_seed, check_i):
#     new_l = None
#     key = s_seed
#     for ssm in all_maps[keys[check_i]]:
#         if ssm[b[check_i]] <= key <= (ssm[b[check_i]] + ssm['range']):
#             dif = key - ssm[b[check_i]]
#             new_l = ssm[c[check_i]] + dif
#     if check_i == 6:
#         return new_l
#     return map_single_seed(new_l, check_i + 1)
#
#
# print(map_single_seed(2149186376, 0))

# Part 2

def map_values(val, pa):
    val_inside = val
    if pa < 0:
        return val_inside
    for ss in all_maps[mapping_keys[pa]]:
        if ss[map_item_2[pa]] <= val_inside <= (ss[map_item_2[pa]] + ss['range']):
            di = val_inside - ss[map_item_2[pa]]
            val_inside = ss[map_item_1[pa]] + di
            break
    return map_values(val_inside, pa - 1)


def aoc_d5_part2():
    # 2857216
    i = 20358599
    # i = 20000000  # ans -> 20358599
    while True:
        print(i)
        break_flag = False
        v = map_values(i, 6)
        print(v)
        if not v:
            continue
        for i_s, seed in enumerate(seeds):
            if i_s % 2 != 0:
                if seeds[i_s - 1] <= v <= ((seeds[i_s - 1]) + seed):
                    break_flag = True
                    break
        if break_flag:
            break
        i += 1


aoc_d5_part1()
aoc_d5_part2()
