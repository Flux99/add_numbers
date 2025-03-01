
def nqueen(arr:List[List[int]],row:int):
    if row == len(arr):
        display(arr)
        return 1

    count = 0
    for col in range(len(arr)):

        if isSafe(arr, row,col):
            arr[row][col] = True
            count += nqueen(arr,row+1)
            arr[row][col] = False
    return count

def isSafe(arr:List[List[int]],row:int,col:int):
    for i in range(len(row)):
        if arr[i][col]:
            return False
    maxleft = min(row, col)
    for i in range(1,maxleft):
        if arr[row-1][col-1]:
            return False
    maxright = min(row, len(arr)-col-1)
    for i in range(1,maxright):
        if arr[row-1][col+1]:
            return False

def display(arr:List[List[int]]):
    for row in arr:
        for r in row:
            if r:
                print("Q")
            else:
                print("X")



n = 4
board = [[0] * n for _ in range(n)]
print("Solutions:")
print(nqueen(board, 0))
