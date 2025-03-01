from typing import List
def n_knight(board:List[List[bool]],row:int,col:int,knight:int):
    if knight == 0:
        display(board)
        print()
        return 1

    if row == len(board)-1 and col == len(board):
        return 0

    if col == len(board):
        return n_knight(board,row+1, 0,knight)



    count = 0
    print(f"isSafe(board,row,col)",isSafe(board,row,col))
    if isSafe(board,row,col):
        board[row][col] = True
        count += n_knight(board,row,col+1,knight-1)
        board[row][col] = False

    count += n_knight(board,row,col+1,knight)
    return count

def isSafe(board,row,col):
    if isValid(board,row-2,col-1):
        if board[row-2][col-1]:
            return False

    if isValid(board,row-2,col+1):
        if board[row-2][col+1]:
            return False

    if isValid(board,row-1,col-2):
        if board[row-1][col-2]:
            return False

    if isValid(board,row-1,col+2):
        if board[row-1][col+2]:
            return False
    return True


def isValid(board,row,col):
    if row >= 0 and row < len(board) and col >= 0 and col < len(board):
        return True
    return False


def display(arr: List[List[bool]]):
    for row in arr:
        print(''.join('K' if r else 'O' for r in row))



n = 4
board = [[False] * n for _ in range(n)]
print(f"n_knight(board, 0,0,{n}):{n_knight(board, 0,0,n )}")
print("Solutions:")
