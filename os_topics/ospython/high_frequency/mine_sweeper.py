# # import random
# #
# # def generate_minesweeper_grid(rows, cols, mines_count):
# #     # Initialize the grid with zeros
# #     grid = [[0 for _ in range(cols)] for _ in range(rows)]
# #
# #     # Place mines randomly
# #     mines_placed = 0
# #     while mines_placed < mines_count:
# #         row = random.randint(0, rows - 1)
# #         col = random.randint(0, cols - 1)
# #         if grid[row][col] != -1:
# #             grid[row][col] = -1
# #             mines_placed += 1
# #             # Update adjacent cells
# #             for i in range(max(0, row - 1), min(rows, row + 2)):
# #                 for j in range(max(0, col - 1), min(cols, col + 2)):
# #                     if grid[i][j] != -1:
# #                         grid[i][j] += 1
# #
# #     return grid
# #
# #
# # grid_size = input("enter the grid size in the format row,col,mine count:")
# # ans = grid_size.split(",")
# # # Generate a 2x3 grid with 3 mines
# # grid = generate_minesweeper_grid(int(ans[0]), int(ans[1]), 3)
# #
# # # Print the grid
# # for row in grid:
# #     print(row)
#
#
#
# import random
#
# class Matrix:
#     def __init__(self, rows, cols, default_value=0):
#         self.rows = rows
#         self.cols = cols
#         self.grid = [[default_value for _ in range(cols)] for _ in range(rows)]
#
#     def at(self, row, col):
#         return self.grid[row][col]
#
#     def set(self, row, col, value):
#         self.grid[row][col] = value
#
#     def in_bounds(self, row, col):
#         return 0 <= row < self.rows and 0 <= col < self.cols
#
#     def __str__(self):
#         return '\n'.join([' '.join(map(str, row)) for row in self.grid])
#
# class Minesweeper:
#     def __init__(self, rows, cols, mine_count):
#         self.rows = rows
#         self.cols = cols
#         self.mine_count = mine_count
#         self.grid = Matrix(rows, cols, default_value=0)
#         self.revealed = Matrix(rows, cols, default_value=False)
#         self.initialize_grid()
#
#     def initialize_grid(self):
#         # Place mines randomly
#         mines_placed = 0
#         while mines_placed < self.mine_count:
#             row = random.randint(0, self.rows - 1)
#             col = random.randint(0, self.cols - 1)
#             if self.grid.at(row, col) != 9:  # 9 represents a mine
#                 self.grid.set(row, col, 9)
#                 mines_placed += 1
#                 self.increment_adjacent_cells(row, col)
#
#     def increment_adjacent_cells(self, row, col):
#         # Increment mine counts in adjacent cells
#         for r in range(row - 1, row + 2):
#             for c in range(col - 1, col + 2):
#                 if self.grid.in_bounds(r, c) and self.grid.at(r, c) != 9:
#                     self.grid.set(r, c, self.grid.at(r, c) + 1)
#
#     def reveal(self, row, col):
#         if not self.grid.in_bounds(row, col) or self.revealed.at(row, col):
#             return
#
#         self.revealed.set(row, col, True)
#         if self.grid.at(row, col) == 0:
#             # Reveal all adjacent cells if current cell has no adjacent mines
#             for r in range(row - 1, row + 2):
#                 for c in range(col - 1, col + 2):
#                     if (r, c) != (row, col):
#                         self.reveal(r, c)
#
#     def is_mine(self, row, col):
#         return self.grid.at(row, col) == 9
#
#     def print_board(self):
#         # Print the board with revealed cells or hidden ('-') for unrevealed cells
#         display = ""
#         for row in range(self.rows):
#             for col in range(self.cols):
#                 if self.revealed.at(row, col):
#                     display += str(self.grid.at(row, col)) + " "
#                 else:
#                     display += "- "
#             display += "\n"
#         print(display)
#
# # Example usage:
# # rows, cols, mines = 5, 5, 5
# # game = Minesweeper(rows, cols, mines)
# #
# # # Reveal some cells and print the board
# # game.reveal(3, 4)  # Start by revealing the top-left corner
# # game.print_board()
# # ask these two from user
#
# grid_size = input("Enter the grid size in the format 'rows,cols,mine_count': ")
# rows, cols, mines = map(int, grid_size.split(','))
#
# # Create the Minesweeper game with user input
# game = Minesweeper(rows, cols, mines)
#
# # Ask the user for the initial reveal coordinates
# while True:
#     try:
#         reveal_coords = input("Enter the row and column to reveal (e.g., '0,0'): ")
#         row, col = map(int, reveal_coords.split(','))
#         break
#     except ValueError:
#         print("Invalid input. Please enter the coordinates as 'row,col'.")
#
# # Reveal the cell and print the board
# game.reveal(row, col)
# game.print_board()


import random

class Matrix:
    def __init__(self, rows, cols, default_value=0):
        self.rows = rows
        self.cols = cols
        self.grid = [[default_value for _ in range(cols)] for _ in range(rows)]

    def at(self, row, col):
        return self.grid[row][col]

    def set(self, row, col, value):
        self.grid[row][col] = value

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.grid])

class Minesweeper:
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.grid = Matrix(rows, cols, default_value=0)
        self.revealed = Matrix(rows, cols, default_value=False)
        self.initialize_grid()

    def initialize_grid(self):
        # Place mines randomly
        mines_placed = 0
        while mines_placed < self.mine_count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid.at(row, col) != 9:  # 9 represents a mine
                self.grid.set(row, col, 9)
                mines_placed += 1
                self.increment_adjacent_cells(row, col)

    def increment_adjacent_cells(self, row, col):
        # Increment mine counts in adjacent cells
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if self.grid.in_bounds(r, c) and self.grid.at(r, c) != 9:
                    self.grid.set(r, c, self.grid.at(r, c) + 1)

    def reveal(self, row, col):
        if not self.grid.in_bounds(row, col) or self.revealed.at(row, col):
            return

        self.revealed.set(row, col, True)
        if self.grid.at(row, col) == 9:
            print("Game Over! You hit a mine.")
            return False
        elif self.grid.at(row, col) == 0:
            # Reveal all adjacent cells if current cell has no adjacent mines
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if (r, c) != (row, col):
                        self.reveal(r, c)
        return True

    def print_board(self):
        # Print the board with revealed cells or hidden ('-') for unrevealed cells
        display = ""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.revealed.at(row, col):
                    display += str(self.grid.at(row, col)) + " "
                else:
                    display += "- "
            display += "\n"
        print(display)

# Get user input for grid size and mine count
# grid_size = input("Enter the grid size in the format 'rows,cols,mine_count': ")
# rows, cols, mines = map(int, grid_size.split(','))

# Create the Minesweeper game with user input
# game = Minesweeper(rows, cols, mines)

# Loop to reveal cells until the user quits or hits a mine
# while True:
#     game.print_board()
#     try:
#         reveal_coords = input("Enter the row and column to reveal (e.g., '0,0') or type 'exit' to quit: ")
#         if reveal_coords.lower() == 'exit':
#             print("Game exited.")
#             break
#
#         row, col = map(int, reveal_coords.split(','))
#         if not game.reveal(row, col):
#             game.print_board()
#             print("Ending the game you hit on the mine")
#             break  # End game on hitting a mine
#     except ValueError:
#         print("Invalid input. Please enter the coordinates as 'row,col' or type 'exit' to quit.")



# import random
#
# def generate_minesweeper_grid(rows, cols, mines_count):
#     # Initialize the grid with zeros
#     grid = [[0 for _ in range(cols)] for _ in range(rows)]
#
#     # Place mines randomly
#     mines_placed = 0
#     while mines_placed < mines_count:
#         row = random.randint(0, rows - 1)
#         col = random.randint(0, cols - 1)
#         if grid[row][col] != 9:  # 9 represents a mine
#             grid[row][col] = 9
#             mines_placed += 1
#             # Update adjacent cells
#             for i in range(max(0, row - 1), min(rows, row + 2)):
#                 for j in range(max(0, col - 1), min(cols, col + 2)):
#                     if grid[i][j] != 9:
#                         grid[i][j] += 1
#
#     return grid
#
# # Generate a 2x3 grid with 3 mines
# grid = generate_minesweeper_grid(5, 7, 4)
#
# # Print the grid
# for row in grid:
#     print(" ".join(str(cell) for cell in row))
# this is the correct code and below is the wrong code which is printing like below
#1 9 0 0 0 0 0
#0 9 0 0 0 0 0
#0 0 0 0 0 0 0
#0 0 0 1 1 0 0
#0 0 0 0 9 9 0



import random

def generate_mine_sweeper_grid(rows,cols,mine_count):
    if mine_count > rows * cols:
        return []


    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_placed = 0
    while mine_placed < mine_count :
        r= random.randint(0,rows-1)
        c = random.randint(0,cols-1)

        if grid[r][c] != 9:
            grid[r][c] = 9
            mine_placed += 1

            for i in range(max(0,r-1), min(rows,r+2)):
                for j in range(max(0,c-1), min(cols,c+2)):
                    if grid[i][j] != 9:
                        grid[i][j] +=1
    return grid


grid = generate_mine_sweeper_grid(5,7,4)

for r in grid:
	print(" ".join(str(c) for c in r))
