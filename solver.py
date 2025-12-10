def solve(matrix, accumulator, row_number):
    rows = len(matrix)

    if row_number > rows:
        return []
    words = []
    if all(map(lambda char: char != '_', accumulator)):
        words.append("".join(accumulator))

    columns = len(matrix[0])
    for i in range(row_number, rows):
        analyzed_row = matrix[i]
        plausible = True
        for j in range(columns):
            if accumulator[j] != '_':
                if analyzed_row[j] != '_':
                    plausible = False
                    break
        if plausible:
            for j in range(columns):
                if analyzed_row[j] != '_':
                    accumulator[j] = analyzed_row[j]

            words += solve(matrix, accumulator, i + 1)
            for j in range(columns):
                if analyzed_row[j] != '_':
                    accumulator[j] = '_'

    return words
