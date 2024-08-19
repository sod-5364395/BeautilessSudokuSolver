import numpy as np


def make_sets(grid):
    columns, rows, blocks = [], [], []
    for column in grid.T:
        columns.append(set(column))
    for row in grid:
        rows.append(set(row))
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            blocks.append(set(grid[i:i+3, j:j+3].flatten()))
    return columns, rows, blocks


def solve_level_1(grid):
    print("starting grid:")
    print(grid)
    default_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    unclear_counter = 0
    unclear_counter_old = 0
    solved_flag = False
    while not solved_flag:
        solved_flag = True
        for row in range(0, 9):
            for column in range(0, 9):
                if grid[row][column] == 0:
                    c, r, m = make_sets(grid)
                    block_r = row // 3
                    block_c = column // 3
                    block = block_r * 3 + block_c
                    diff = default_set.difference(c[column]).difference(r[row]).difference(m[block])
                    if len(diff) == 1:
                        grid[row][column] = diff.pop()
                    elif len(diff) == 0:
                        raise ValueError
                    else:
                        unclear_counter += 1
                        solved_flag = False
        if unclear_counter_old == unclear_counter:
            break
        unclear_counter_old = unclear_counter
        unclear_counter = 0
    return grid, solved_flag


def solve_level_2(grid):
    default_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    unclear_counter = 0
    unclear_counter_old = 0
    solved_flag = False
    while not solved_flag:
        solved_flag = True
        for row in range(0, 9):
            for column in range(0, 9):
                if grid[row][column] == 0:
                    c, r, m = make_sets(grid)
                    block_r = row // 3
                    block_c = column // 3
                    block = block_r * 3 + block_c
                    unclear_diff = default_set.difference(c[column]).difference(r[row]).difference(m[block])
                    other_unclear_sets = []
                    for col in range(0, 9):
                        if grid[row][col] == 0 and col != column:
                            block_r = row // 3
                            block_c = col // 3
                            block_col = block_r * 3 + block_c
                            if block_col != block:
                                other_unclear_sets.append(default_set.difference(c[col]).difference(r[row]).difference(m[block]))
                    for ro in range(0, 9):
                        if grid[ro][column] == 0 and ro != row:
                            block_r = ro // 3
                            block_c = column // 3
                            block_ro = block_r * 3 + block_c
                            if block_ro != block:
                                other_unclear_sets.append(default_set.difference(c[column]).difference(r[ro]).difference(m[block]))
                    row_start_b, col_start_b = upper_left_corner(block)
                    for i in range(row_start_b, row_start_b + 3):
                        for j in range(col_start_b, col_start_b + 3):
                            if i != row or j != column:
                                other_unclear_sets.append(default_set.difference(c[j]).difference(r[i]).difference(m[block]))
                    for other_unclear_set in other_unclear_sets:
                        unclear_diff = unclear_diff.difference(other_unclear_set)
                    if len(unclear_diff) == 1:
                        grid[row][column] = unclear_diff.pop()
                        grid, solved_flag = solve_level_1(grid)
                    else:
                        unclear_counter += 1
                        solved_flag = False
        if unclear_counter_old == unclear_counter:
            break
        unclear_counter_old = unclear_counter
        unclear_counter = 0
    return grid, solved_flag


def upper_left_corner(block_index):
    block_row = block_index // 3
    block_col = block_index % 3
    row_start = block_row * 3
    col_start = block_col * 3
    return row_start, col_start


if __name__ == '__main__':

    grid_easy_0 = np.array([[0, 4, 0, 5, 0, 0, 0, 7, 0],
                            [0, 0, 5, 6, 0, 9, 8, 3, 1],
                            [6, 3, 0, 0, 2, 7, 5, 4, 0],
                            [7, 0, 4, 0, 0, 0, 0, 0, 6],
                            [0, 6, 0, 0, 5, 3, 2, 8, 4],
                            [0, 0, 0, 0, 0, 6, 0, 5, 0],
                            [3, 8, 7, 0, 0, 0, 4, 0, 0],
                            [0, 0, 0, 1, 0, 5, 0, 0, 3],
                            [5, 1, 6, 0, 0, 0, 9, 2, 0]])

    grid_easy_1 = np.array([[4, 9, 0, 1, 6, 0, 3, 7, 0],
                            [0, 0, 7, 0, 0, 0, 1, 8, 6],
                            [0, 8, 0, 2, 0, 0, 0, 5, 0],
                            [3, 0, 0, 7, 9, 0, 0, 0, 5],
                            [0, 0, 0, 3, 0, 0, 7, 2, 1],
                            [8, 7, 0, 4, 2, 5, 6, 0, 0],
                            [0, 0, 3, 0, 0, 2, 4, 0, 7],
                            [6, 0, 4, 0, 7, 3, 2, 0, 0],
                            [0, 2, 0, 0, 1, 0, 0, 9, 0]])

    grid_very_very_difficult_1 = np.array([[0, 0, 1, 0, 7, 0, 2, 0, 3],
                                           [8, 0, 0, 0, 0, 5, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 6],
                                           [5, 0, 0, 0, 0, 9, 6, 0, 1],
                                           [0, 0, 0, 0, 0, 4, 0, 0, 0],
                                           [7, 0, 9, 0, 0, 0, 0, 0, 8],
                                           [0, 0, 7, 8, 3, 0, 0, 0, 0],
                                           [0, 0, 5, 4, 2, 0, 0, 0, 0],
                                           [0, 6, 0, 0, 5, 0, 0, 3, 7]])

    grid_1, solved_flag_1 = solve_level_1(grid_very_very_difficult_1)

    if solved_flag_1:
        print('solved!')
        print(grid_1)
    else:
        print("not solved yet. go to next step.")
        # print("no progress. stopped solving.")
        print(grid_1)
        grid_2, solved_flag_2 = solve_level_2(grid_1)

        if solved_flag_2:
            print('solved!')
            print(grid_2)
        else:
            print("not solved yet. go to next step.")
            print(grid_2)