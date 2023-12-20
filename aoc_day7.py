with open('inputs/input7.txt') as f:
    inputs = f.read()
inputs = inputs.split('\n')

strength_map = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}
hands_bet_map = {hand.split(' ')[0]: int(hand.split(' ')[1]) for hand in inputs}
hands = [hand.split(' ')[0] for hand in inputs]
hand_type = {
    '5H': 7,
    '41H': 6,
    '32H': 5,
    '311H': 4,
    '221H': 3,
    '2111H': 2,
    '11111H': 1
}


# PART 1 LOGIC
def get_hand_type_part1(hand):
    hand_set = set(hand)
    t = []
    for card in hand_set:
        t.append(hand.count(card))
    t = sorted(t, reverse=True)
    h_type = ''.join(map(str, t)) + 'H'
    return hand_type[h_type]


# PART 2 LOGIC
def get_hand_type_part2(hand):
    hand_set = set(hand)
    t = []
    check_card = {}
    j_count = 0
    for card in hand_set:
        if hand.count('J') == 5:
            j_count = hand.count('J')
            t.append(0)
            break
        if card == 'J':
            j_count = hand.count('J')
            continue
        check_card[card] = hand.count(card)
        t.append(hand.count(card))
    t = sorted(t, reverse=True)
    t[0] += j_count
    h_type = ''.join(map(str, t)) + 'H'
    return hand_type[h_type]


def hand_type_arrays(part):
    all_hands = [[], [], [], [], [], [], []]
    for hand in hands:
        if part == 1:
            val = get_hand_type_part1(hand)
        else:
            val = get_hand_type_part2(hand)
        if val == 1:
            all_hands[0].append(hand)
        if val == 2:
            all_hands[1].append(hand)
        if val == 3:
            all_hands[2].append(hand)
        if val == 4:
            all_hands[3].append(hand)
        if val == 5:
            all_hands[4].append(hand)
        if val == 6:
            all_hands[5].append(hand)
        if val == 7:
            all_hands[6].append(hand)
    return all_hands


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        next_val = array[j]
        for index in range(5):
            f_val = strength_map[next_val[index]]
            l_val = strength_map[pivot[index]]
            if f_val > l_val:
                break
            if f_val == l_val:
                if index != 4:
                    continue
            if f_val < l_val:
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])
                break

    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def quicksort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quicksort(array, low, pi - 1)
        quicksort(array, pi + 1, high)


# THIS IS THE STARTING FUNCTION
def do_sort(part):
    all_hands = hand_type_arrays(part)
    new_hand = []
    for all_hand in all_hands:
        new_h5 = all_hand
        n = len(new_h5)
        quicksort(new_h5, 0, n - 1)
        new_hand.extend(new_h5)
    return new_hand


def mul_array(inp):
    index, x = inp
    return (index + 1) * hands_bet_map[x]


new_h = do_sort(1)
p = list(map(mul_array, enumerate(new_h)))
print(sum(p))

strength_map['J'] = 0
new_h = do_sort(2)
p = list(map(mul_array, enumerate(new_h)))
print(sum(p))
