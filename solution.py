import collections

assignments = []
rows = 'ABCDEFGHI'
columns = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unit_list:
        possible_twins = [values[b] for b in unit if len(values[b]) == 2]

        counter = collections.Counter(possible_twins)
        # Exact Twins if the count matches 2
        twins = [key for key,value in counter.items() if value == 2]
        for twin in twins:
            for box in unit:
                if values[box] != twin and len(values[box]) > 1:
                    value = values[box]
                    for n in twin:
                        value = value.replace(n, '')
                        assign_value(values, box, value)
    return values

    # Eliminate the naked twins as possibilities for their peers


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [x+y for x in A for y in B]


boxes = cross(rows,columns)

row_units = [cross(r,columns) for r in rows]
column_units = [cross(rows, c) for c in columns]
square_units = [cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal units [A1,B2..I9] and [A9,B8..I1]
diagonal1 = [rs + cs for rs,cs in zip(rows,columns)]
diagonal2 = [rs + cs for rs,cs in zip(rows,columns[::-1])]
diagonal_units = [diagonal1, diagonal2]

unit_list = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - {s}) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for g in grid:
        if g in digits:
            chars.append(g)
        elif g == '.':
            chars.append(digits)
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width *3) *3])
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in columns))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before = solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return  False
    return values


def search(values):
    # Reduce the sudoku to narrow down the serach scope
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        # Already solved. No need to proceed with the method
        return  values

    # First try the box with lowest possibilities
    n, s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)

    # Recursive fn
    for value in values[s]:
        # Clone the Sudoku
        new_soduku = values.copy()
        new_soduku[s] = value
        attempt = search(new_soduku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
