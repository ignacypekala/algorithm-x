import os
import random
import subprocess
from functools import cmp_to_key

from solver import solve

MAX_ROW_COUNT = 200
MAX_ROW_LENGTH = 300
# seed = random.randint(0, 100)

seed = 1
random.seed(seed)

cursor = 0
cursor_cycles = 0

text = "ABCDEFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvxyz1234567890"

wygenerowane_rozwiazania = 0


def randint(a, b):
    return random.randint(a, b)


def stringify_matrix(matrix):
    text = ''
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text += matrix[i][j]
        text += '\n'
    return text


def gen_matrix(rows, columns, probability, text):
    size = len(text)
    input_lines = []

    def next_letter():
        global cursor_cycles, cursor
        nonlocal size
        letter = text[cursor]
        cursor += 1
        if cursor == size:
            cursor_cycles += 1
            cursor = 0

        return letter

    prev = ['_'] * columns
    for i in range(rows):
        generated_row = []
        filled = 0
        for j in range(columns):
            character = '_'
            if prev[j] == '_':
                if randint(probability[0], probability[1]) > 0:
                    character = '.'
                    filled += 1
            generated_row.append(character)
        if filled == 0:
            generated_row[randint(0, j)] = '.'
        input_lines.append(generated_row)
        prev = generated_row

    for i in range(rows):
        for j in range(columns):
            if input_lines[i][j] == '.':
                input_lines[i][j] = next_letter()

    return input_lines


def filter_words(words, filter):
    filtered_words = []
    for word in words:
        filtered_word = ''
        for char in range(len(filter)):
            if filter[char] == '+':
                filtered_word += word[char]
        filtered_words.append(filtered_word)
    filtered_words_text = ""
    for word in filtered_words:
        filtered_words_text += word + '\n'
    return filtered_words_text


def generate_test(rows, columns, path, probability, text):
    global wygenerowane_rozwiazania
    filter = ""
    for i in range(columns):
        filter += "+" if randint(0, 1) == 0 else "-"

    matrix = gen_matrix(rows, columns, probability, text)
    accum_row = ['_'] * columns
    words = solve(matrix, accum_row, 0)
    wygenerowane_rozwiazania += len(words)

    unsorted_output = filter_words(words, filter)
    with open(path + '.out.sorted', 'wb') as file:
        subprocess.run('sort', input=bytes(unsorted_output, 'utf-8'), stdout=file)

    with open(path + ".in", 'wb') as file:
        file.write(bytes(filter + '\n' + stringify_matrix(matrix), 'utf-8'))

batches = [
    [
        10,
        5, 5,
        (-5, 1),
        "abcdefghijklmnopqrstuvwxyz"
    ],
    [
        10,
        10, 10,
        (0, 1),
        "BCDEFGHJKLMNOPQRTUVWXYZ"
    ],
    [
        10,
        5, 10,
        (0, 1),
        "NOPQRSTWXYZABCDEFGH"
    ],
    [
        10,
        10, 5,
        (0, 1),
        "aBCDefghiJKLMNOpqrStUvwxyz"
    ],
    [
        10,
        30, 30,
        (0, 1),
        "CVJBWRFGQBOER"
    ],
    [
        10,
        48, 91,
        (0, 1),
        "Npmlcbyvglplmnovwnwayhxfhfbjrcebfglghgxv?Crjavr."
    ],
    [
        10,
        80, 10,
        (0, 1),
        "TqlfghqvbjnyrzjnxnqrzvvjBkrashepvr,uvfgbevnmnwzbjnynqehtvrzvrwfpranyvfpvrzbvpuhyhovbalpucemrqzvbgbj.-Pbolybancvrejfmlzzvrwfph?-Trbtensvn-emrxycbjnmavrcbrgn-Ngynffjnvgnolyjvrxfmlvyngjvrwolybmnavzhxelptnfvberxjbqxv."
    ],
    [
        10,
        100, 100,
        (0, 1),
        "JxbpvbyxnpuovtbftemnabjfybjnpujlqnpgehqabOvtbfhfznxcemrqmvjal,xbybevjbaphqan;Fybjglyxboemrxhfylfmlvelzbjcbemnqrx,Nyrgerfpvvpuzvrwfxvavrcbwzvrmbynqrx.Nolpravpyvgrjfxvrcvrfavvcbgenjl,Gemronzvrpmqebjvr,anjfvmlp,jenpnpmboynjl."
    ],
    [
        10,
        153, 274,
        (0, 1),
        "alskdjf ajshfeuwqhiug fjasgdfhgasdhfa dhsjfkla fhj aep ashf kjals eha ksjdh aipe hjqwp"
    ],
    [
        10,
        200, 300,
        (0, 1),
        "alkf;aksldjfaslkdfjaf jslkf jadslf jkasdf [oasd faklfjas df[ asdfj[]]]"
    ],
    [
        10,
        72, 65,
        (0, 1),
        "Ztyntrfgnwnx zyrxbBohqmvyfvr jgbovrcbrgn?Zuz,puprfmhfylfmrpsenfmxr?-Crjavr-Ynzoreg,Ynzoreg,glpuhwh.Avrmyr"
    ]
]
nazwy = []
batchnr = 0
dirname = 'tests'
try:
    os.mkdir(os.path.join(dirname))
except FileExistsError:
    pass

for batch in list(sorted(batches, key=cmp_to_key(lambda a, b: (a[2] ** 2) // a[1] - (b[2] ** 2) // b[2]))):
    nazwy.append(f'{batch[1]}x{batch[2]}')
    name = nazwy[batchnr]
    try:
        os.mkdir(os.path.join(dirname, name))
    except FileExistsError:
        pass
    probability = batch[3]
    print(f'Generating test pack {name} ({batch[1]}x{batch[2]}) with probability {probability[0] + 1} to {probability[1] + 1}.')
    print(f'The text has been written {cursor_cycles} times.')
    cursor_cycles = 0
    for nr in range(batch[0]):
        path = os.path.join(dirname, name) + '/' + name + '_' + str(nr)
        generate_test(batch[1], batch[2], path, probability, batch[4])
    ratio = int(wygenerowane_rozwiazania / (batch[0] * batch[1]) * 100)
    print(f"Achieved input/output ratio: {ratio}%\n")
    batchnr += 1
    cursor = 0

print(" ".join(nazwy[:batchnr]))
