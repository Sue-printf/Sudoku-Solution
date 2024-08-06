import sys
import glob

# Function to convert the Sudoku string to a 2D list
def sudoku_string_to_board(sudoku_string):
    sudoku_list = [sudoku_string[i:i+9] for i in range(0, 81, 9)]
    sudoku_board = [[int(cell) for cell in row] for row in sudoku_list]
    return sudoku_board

# Function to parse the Sudoku puzzle from a file
def parse_sudoku_from_file(file_path):
    sudoku_boards = []
    with open(file_path, 'r') as file:
        for line in file:
            input_string = line.strip() # Remove newline characters
            sudoku_board = sudoku_string_to_board(input_string)
            sudoku_boards.append(sudoku_board)
    return sudoku_boards

# The rest of the functions remain unchanged from the previous code
def is_valid(sudoku_dict, row, col, num):
    for x in range(9):
        if sudoku_dict[f'{row}{x}'] == num:
            return False
        if sudoku_dict[f'{x}{col}'] == num:
            return False
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if sudoku_dict[f'{start_row + i}{start_col + j}'] == num:
                return False
    return True

def find_empty(sudoku_dict):
    empty_cells = [(key, count_possible_values(sudoku_dict, key)) for key in sudoku_dict if sudoku_dict[key] == 0]
    return min(empty_cells, key=lambda x: x[1])[0] if empty_cells else None

def count_possible_values(sudoku_dict, cell):
    row, col = int(cell[0]), int(cell[1])
    possible_values = set(range(1, 10))
    for num in range(1, 10):
        if not is_valid(sudoku_dict, row, col, num):
            possible_values.remove(num)
    return len(possible_values)

def solve_sudoku(sudoku_dict):
    empty = find_empty(sudoku_dict)
    if not empty:
        return True

    row, col = int(empty[0]), int(empty[1])

    for num in range(1, 10):
        if is_valid(sudoku_dict, row, col, num):
            sudoku_dict[empty] = num
            if solve_sudoku(sudoku_dict):
                return True
            sudoku_dict[empty] = 0

    return False

def print_sudoku(sudoku_dict):
    return ''.join(str(sudoku_dict[f'{row}{col}']) for row in range(9) for col in range(9))

def process_file(file_path):
    sudoku_board = parse_sudoku_from_file(file_path)
    sudoku_dict = {f'{row}{col}': sudoku_board[row][col] for row in range(9) for col in range(9)}
    if solve_sudoku(sudoku_dict):
        solved_board_string = print_sudoku(sudoku_dict)
        print(f"Solved: {solved_board_string}")
        with open(f'output_{file_path}.txt', 'w') as output_file:
            output_file.write(solved_board_string)
    else:
        print("No solution exists.")

def main():
    sudoku_files = glob.glob('sudoku_boards.txt')
    for file_path in sudoku_files:
        print(f"Processing {file_path}...")
        sudoku_boards = parse_sudoku_from_file(file_path)
        for sudoku_board in sudoku_boards:
            sudoku_dict = {f'{row}{col}': sudoku_board[row][col] for row in range(9) for col in range(9)}
            if solve_sudoku(sudoku_dict):
                solved_board_string = print_sudoku(sudoku_dict)
                print(f"Solved: {solved_board_string}")
                with open(f'output_{file_path}.txt', 'a') as output_file:
                    output_file.write(solved_board_string + "\n")
            else:
                print("No solution exists.")
if __name__ == "__main__":
    main()
