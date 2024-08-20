import numpy as np


def solve_level_1(grid):
    default_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    unclear_counter = 0
    unclear_counter_old = 0
    solved_flag = False
    while not solved_flag:
        solved_flag = True
        for row in range(0, 9):
            for column in range(0, 9):
                if grid[row][column] == 0:
                    r, c, b = make_sets(grid)
                    block = calc_block_index(row, column)
                    diff = default_set.difference(r[row]).difference(c[column]).difference(b[block])
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
                    r, c, b = make_sets(grid)
                    block = calc_block_index(row, column)
                    unclear_diff = default_set.difference(c[column]).difference(r[row]).difference(b[block])
                    other_unclear_sets_row = []
                    other_unclear_sets_column = []
                    other_unclear_sets_block = []
                    for col in range(0, 9):
                        if grid[row][col] == 0 and col != column:
                            block_col = calc_block_index(row, col)
                            other_unclear_sets_row.append(default_set.difference(r[row]).difference(c[col]).difference(b[block_col]))
                    unclear_diff_copy = unclear_diff
                    for other_unclear_set_row in other_unclear_sets_row:
                        unclear_diff_copy = unclear_diff_copy.difference(other_unclear_set_row)
                    if len(unclear_diff_copy) == 1:
                        grid[row][column] = unclear_diff_copy.pop()
                        grid, solved_flag = solve_level_1(grid)
                        if solved_flag:
                            break
                    else:
                        for ro in range(0, 9):
                            if grid[ro][column] == 0 and ro != row:
                                block_ro = calc_block_index(ro, column)
                                other_unclear_sets_column.append(default_set.difference(r[ro]).difference(c[column]).difference(b[block_ro]))
                        unclear_diff_copy = unclear_diff
                        for other_unclear_set_column in other_unclear_sets_column:
                            unclear_diff_copy = unclear_diff_copy.difference(other_unclear_set_column)
                        if len(unclear_diff_copy) == 1:
                            grid[row][column] = unclear_diff_copy.pop()
                            grid, solved_flag = solve_level_1(grid)
                            if solved_flag:
                                break
                        else:
                            row_start_b, col_start_b = upper_left_corner(block)
                            for i in range(row_start_b, row_start_b + 3):
                                for j in range(col_start_b, col_start_b + 3):
                                    if grid[i][j] == 0 and (i != row or j != column):
                                        other_unclear_sets_block.append(
                                            default_set.difference(r[i]).difference(c[j]).difference(b[block]))
                            unclear_diff_copy = unclear_diff
                            for other_unclear_set_column in other_unclear_sets_column:
                                unclear_diff_copy = unclear_diff_copy.difference(other_unclear_set_column)
                            if len(unclear_diff_copy) == 1:
                                grid[row][column] = unclear_diff_copy.pop()
                                grid, solved_flag = solve_level_1(grid)
                                if solved_flag:
                                    break
                            else:
                                unclear_counter += 1
                                solved_flag = False
            if solved_flag:
                break
        if unclear_counter_old == unclear_counter:
            break
        unclear_counter_old = unclear_counter
        unclear_counter = 0
    return grid, solved_flag


def solve_level_3(grid):
    if _rec_solve_level_3(grid):
        return grid, True
    return grid, False


def _rec_solve_level_3(grid):
    default_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for row in range(0, 9):
        for column in range(0, 9):
            if grid[row][column] == 0:
                r, c, b = make_sets(grid)
                block = calc_block_index(row, column)
                unclear_diff = default_set.difference(c[column]).difference(r[row]).difference(b[block])
                if len(unclear_diff) > 0:
                    for number in unclear_diff:
                        grid[row][column] = number
                        if _rec_solve_level_3(grid):
                            return True
                        grid[row][column] = 0
                    return False
                else:
                    return False
    return True


def calc_block_index(row, column):
    block_r = row // 3
    block_c = column // 3
    block_index = block_r * 3 + block_c
    return block_index


def upper_left_corner(block_index):
    block_row = block_index // 3
    block_col = block_index % 3
    row_start = block_row * 3
    col_start = block_col * 3
    return row_start, col_start


def make_sets(grid):
    rows, columns, blocks = [], [], []
    for row in grid:
        rows.append(set(row))
    for column in grid.T:
        columns.append(set(column))
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            blocks.append(set(grid[i:i+3, j:j+3].flatten()))
    return rows, columns, blocks


if __name__ == '__main__':

    grid_easy_0 = np.array([
        [0, 4, 0, 5, 0, 0, 0, 7, 0],
        [0, 0, 5, 6, 0, 9, 8, 3, 1],
        [6, 3, 0, 0, 2, 7, 5, 4, 0],
        [7, 0, 4, 0, 0, 0, 0, 0, 6],
        [0, 6, 0, 0, 5, 3, 2, 8, 4],
        [0, 0, 0, 0, 0, 6, 0, 5, 0],
        [3, 8, 7, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 1, 0, 5, 0, 0, 3],
        [5, 1, 6, 0, 0, 0, 9, 2, 0]])

    grid_easy_1 = np.array([
        [4, 9, 0, 1, 6, 0, 3, 7, 0],
        [0, 0, 7, 0, 0, 0, 1, 8, 6],
        [0, 8, 0, 2, 0, 0, 0, 5, 0],
        [3, 0, 0, 7, 9, 0, 0, 0, 5],
        [0, 0, 0, 3, 0, 0, 7, 2, 1],
        [8, 7, 0, 4, 2, 5, 6, 0, 0],
        [0, 0, 3, 0, 0, 2, 4, 0, 7],
        [6, 0, 4, 0, 7, 3, 2, 0, 0],
        [0, 2, 0, 0, 1, 0, 0, 9, 0]])

    grid_very_very_difficult_0 = np.array([
        [0, 0, 1, 0, 7, 0, 2, 0, 3],
        [8, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6],
        [5, 0, 0, 0, 0, 9, 6, 0, 1],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [7, 0, 9, 0, 0, 0, 0, 0, 8],
        [0, 0, 7, 8, 3, 0, 0, 0, 0],
        [0, 0, 5, 4, 2, 0, 0, 0, 0],
        [0, 6, 0, 0, 5, 0, 0, 3, 7]])

    grid_medium_0 = np.array([
        [0, 0, 7, 0, 0, 9, 0, 3, 0],
        [0, 6, 8, 0, 0, 0, 9, 2, 0],
        [0, 0, 3, 0, 0, 2, 1, 0, 8],
        [0, 7, 0, 9, 0, 0, 2, 4, 0],
        [3, 0, 0, 0, 0, 5, 0, 0, 0],
        [5, 9, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 9, 0],
        [8, 0, 0, 0, 5, 0, 4, 0, 0],
        [0, 0, 1, 0, 0, 4, 6, 0, 0]])

    grid_difficult_0 = np.array([
        [1, 0, 8, 0, 0, 2, 0, 0, 5],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 4, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 1, 5, 0, 0],
        [5, 0, 0, 0, 2, 0, 7, 3, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 6],
        [6, 3, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 9, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 1, 0, 4, 0, 0]])

    grid_unclear_difficulty_0 = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    grid_error_0 = np.array([
        [0, 0, 4, 0, 6, 0, 2, 0, 3],
        [8, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 6],
        [5, 0, 0, 0, 0, 9, 6, 0, 1],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [7, 0, 9, 0, 0, 0, 0, 0, 8],
        [0, 0, 7, 8, 3, 0, 0, 0, 0],
        [0, 0, 5, 4, 2, 0, 0, 0, 0],
        [0, 6, 0, 0, 5, 0, 0, 3, 7]])

    grid_1, solved_flag_1 = solve_level_1(grid_easy_1)

    if solved_flag_1:
        print('solved on level 1!')
        print(grid_1)
    else:
        print("not solved on level 1. go to level 2.")
        grid_2, solved_flag_2 = solve_level_2(grid_1)
        if solved_flag_2:
            print('solved on level 2!')
            print(grid_2)
        else:
            print("not solved on level 2. go to level 3.")
            grid_3, solved_flag_3 = solve_level_3(grid_2)
            if solved_flag_3:
                print('solved on level 3!')
                print(grid_3)
            else:
                print("not solved on level 3. ERROR???")
