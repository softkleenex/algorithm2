import copy
import random
from queue import PriorityQueue

class Board:
    def __init__(self, tiles): # Constructor
        self.n = len(tiles)
        self.tiles = copy.deepcopy(tiles)
        self.twinBoard = None
        
        # Compute Hamming distance
        self.hammingDistance = 0
        goal = 0
        for rowId, row in enumerate(tiles):
            for colId, t in enumerate(row):
                goal += 1
                if t == 0: continue
                if t != goal: self.hammingDistance += 1

        # Compute Manhattan distance
        self.manhattanDistance = 0
        for rowId, row in enumerate(tiles):
            for colId, t in enumerate(row):
                if t == 0: continue
                goalRow, goalCol = (t-1) // self.n, (t-1) % self.n
                self.manhattanDistance += abs(rowId - goalRow) + abs(colId - goalCol)

        # Find the empty tile and store its location in (self.rowZero, self.colZero)
        self.rowZero, self.colZero = None, None      
        for rowId, row in enumerate(self.tiles):
            for colId, t in enumerate(row):
                if t == 0: self.rowZero, self.colZero = rowId, colId 
        assert(self.rowZero != None and self.colZero != None) 

    # Create a human-readable string representation
    def __str__(self):
        strList = []        
        for row in self.tiles:
            for t in row:
                strList.append(f'{t:6d}')
            strList.append('\n')
        return ''.join(strList)

    def __repr__(self):  # This function is called when a Board object is printed as part of a list
        return self.__str__()

    # Defines behavior for the equality operator, ==
    def __eq__(self, other):
        if other == None: return False
        if not isinstance(other, Board): return False
        
        if self.n != other.n: return False
        for rowId, row in enumerate(self.tiles):
            for colId, t in enumerate(row):
                if t != other.tiles[rowId][colId]: return False
        return True

    # Defines behavior for the less-than operator, <
    # This function is required to compare two Boards in a PriorityQueue
    def __lt__(self, other):
        if self.n < other.n: return True
        else:
            for rowId, row in enumerate(self.tiles):
                for colId, t in enumerate(row):
                    if t < other.tiles[rowId][colId]: return True
            return False

    def hamming(self):
        return self.hammingDistance
    
    def manhattan(self):
        return self.manhattanDistance

    def dimension(self):
        return self.n

    def isGoal(self):
        return self.hammingDistance == 0
    
    def neighbors(self):
        # Create a neighbor board by switching (row, col) with (rowZero, colZero),
        #   where (rowZero, colZero) is the location of the empty tile
        def createNeighbor(tiles, row, col):            
            tiles[self.rowZero][self.colZero], tiles[row][col] = tiles[row][col], 0  # Switch two tiles
            neighbor = Board(self.tiles) # Create a neighbor with the switched tiles
            tiles[self.rowZero][self.colZero], tiles[row][col] = 0, tiles[self.rowZero][self.colZero] # Switch the tiles back to their original positions
            return neighbor

        neighborList = []
        if self.rowZero > 0: neighborList.append(createNeighbor(self.tiles, self.rowZero-1, self.colZero)) # Push up the empty tile
        if self.rowZero < self.dimension()-1: neighborList.append(createNeighbor(self.tiles, self.rowZero+1, self.colZero)) # Push down the empty tile
        if self.colZero > 0: neighborList.append(createNeighbor(self.tiles, self.rowZero, self.colZero-1)) # Push the empty tile to the left
        if self.colZero < self.dimension()-1: neighborList.append(createNeighbor(self.tiles, self.rowZero, self.colZero+1)) # Push the empty tile to the right

        return neighborList

    def twin(self):
        if self.twinBoard == None:
            # Randomly select two tile numbers to swap
            numbers4Twin = list(range(1, self.dimension()*self.dimension()))
            random.shuffle(numbers4Twin)

            # Identify (row, col) of the two tiles
            for rowId, row in enumerate(self.tiles):
                for colId, t in enumerate(row):
                    if t == numbers4Twin[0]: row1, col1 = rowId, colId
                    elif t == numbers4Twin[1]: row2, col2 = rowId, colId
            
            # Swap the two tiles to create a twin board
            self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1]
            self.twinBoard = Board(self.tiles)
            self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1] # Swap the two tiles back to their original positions

        return self.twinBoard


def solveManhattan(initialBoard):
    assert(isinstance(initialBoard, Board))

    # Create minPQ for the original board and its twin
    pq = PriorityQueue()
    pqTwin = PriorityQueue()

    # Initial state: (priority, board, moves, previous_node)
    # priority = moves + manhattan distance
    initialNode = (0 + initialBoard.manhattan(), initialBoard, 0, None)
    twinNode = (0 + initialBoard.twin().manhattan(), initialBoard.twin(), 0, None)

    pq.put(initialNode)
    pqTwin.put(twinNode)

    # Keep track of visited states to avoid cycles
    visited = set()
    visitedTwin = set()

    # Helper function to convert board to hashable tuple
    def boardToTuple(board):
        return tuple(tuple(row) for row in board.tiles)

    visited.add(boardToTuple(initialBoard))
    visitedTwin.add(boardToTuple(initialBoard.twin()))

    while pq.qsize() > 0 and pqTwin.qsize() > 0:
        # Process original board
        minNode = pq.get()
        priority, board, moves, prevNode = minNode

        # Check if goal is reached
        if board.isGoal():
            # Reconstruct the path
            path = []
            currentNode = minNode
            while currentNode is not None:
                path.append(currentNode[1])  # currentNode[1] is the board
                currentNode = currentNode[3]  # currentNode[3] is the previous node
            path.reverse()
            return path

        # Add neighbors to the priority queue
        for neighbor in board.neighbors():
            neighborTuple = boardToTuple(neighbor)
            # Skip if we've already visited this state
            if neighborTuple not in visited:
                visited.add(neighborTuple)
                newMoves = moves + 1
                newPriority = newMoves + neighbor.manhattan()
                newNode = (newPriority, neighbor, newMoves, minNode)
                pq.put(newNode)

        # Process twin board
        minNodeTwin = pqTwin.get()
        priorityTwin, boardTwin, movesTwin, prevNodeTwin = minNodeTwin

        # Check if twin reached the goal (means original is unsolvable)
        if boardTwin.isGoal():
            return None

        # Add twin's neighbors to the priority queue
        for neighbor in boardTwin.neighbors():
            neighborTuple = boardToTuple(neighbor)
            # Skip if we've already visited this state
            if neighborTuple not in visitedTwin:
                visitedTwin.add(neighborTuple)
                newMoves = movesTwin + 1
                newPriority = newMoves + neighbor.manhattan()
                newNode = (newPriority, neighbor, newMoves, minNodeTwin)
                pqTwin.put(newNode)

    return None
    

def solveNprint(initialBoard, solveFunction = solveManhattan):
    solution = solveFunction(initialBoard)
    if solution != None and isinstance(solution, list) and len(solution) >= 1:
        print(f"Solvable in {len(solution)-1} moves")
        for board in solution:
            print(board)
    else: print("Unsolvable")


def correctnessTest(func, input, expected_len, expected_output, correct):
    print(f"{func.__name__}(\n{input})")
    output = func(input)

    if expected_len == 0: # Unsolvable case
        if output is None: print("Pass")
        else:
            print(f"Fail - the output must be None (Unsolvable case)")
            correct = False                

    elif output is not None and isinstance(output, list):
        if  len(output) == expected_len:
            if expected_output == None: print("Pass")
            elif expected_output == output: print("Pass")
            else:    
                print(f"Fail - the output does not match the expected output")
                correct = False                
        else:
            print(f"Fail - length of output {len(output)} is not equal to {expected_len}")
            correct = False

    else:
        print(f"Fail - output is NOT a list")
        correct = False

    print()    

    return correct


if __name__ == "__main__":
    '''
    For visual inspection
    '''
    # Solvable in 0 move (already solved)
    b0 = Board([[1,2,3],[4,5,6],[7,8,0]])    
    solveNprint(b0)
    
    # Solvable in 4 moves
    b4 = Board([[0,1,3],[4,2,5],[7,8,6]])
    solveNprint(b4)  

    
    '''
    Unit Test
    '''    
    print("Correctness test for solveManhattan()")
    print("For each test case, if your answer does not appear within 10 seconds, then consider that you failed the case")
    print()
    correct = True

    b0 = Board([[1,2,3],[4,5,6],[7,8,0]])
    correct = correctnessTest(solveManhattan, b0, 1, [b0], correct)

    b4 = Board([[0,1,3],[4,2,5],[7,8,6]])
    b41 = Board([[1,0,3],[4,2,5],[7,8,6]])
    b42 = Board([[1,2,3],[4,0,5],[7,8,6]])
    b43 = Board([[1,2,3],[4,5,0],[7,8,6]])
    b44 = Board([[1,2,3],[4,5,6],[7,8,0]])
    correct = correctnessTest(solveManhattan, b4, 5, [b4, b41, b42, b43, b44], correct)

    b4_5 = Board([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 0, 14, 15], [16, 17, 13, 19, 20], [21, 22, 18, 23, 24]])
    b4_5_1 = Board([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 0, 19, 20], [21, 22, 18, 23, 24]])
    b4_5_2 = Board([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 0, 23, 24]])
    b4_5_3 = Board([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 0, 24]])
    b4_5_4 = Board([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]])
    correct = correctnessTest(solveManhattan, b4_5, 5, [b4_5, b4_5_1, b4_5_2, b4_5_3, b4_5_4], correct)
    
    b3_2 = Board([[3, 1], [0, 2]])
    b3_2_1 = Board([[0, 1], [3, 2]])
    b3_2_2 = Board([[1, 0], [3, 2]])
    b3_2_3 = Board([[1, 2], [3, 0]])
    correct = correctnessTest(solveManhattan, b3_2, 4, [b3_2, b3_2_1, b3_2_2, b3_2_3], correct)    

    b4_10 = Board([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                      [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                      [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                      [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                      [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                      [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                      [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
                      [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
                      [81, 82, 83, 84, 85, 86, 0, 87, 89, 90],
                      [91, 92, 93, 94, 95, 96, 97, 88, 98, 99]])
    b4_10_1 = Board([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                        [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                        [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                        [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
                        [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
                        [81, 82, 83, 84, 85, 86, 87, 0, 89, 90],
                        [91, 92, 93, 94, 95, 96, 97, 88, 98, 99]])
    b4_10_2 = Board([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                        [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                        [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                        [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
                        [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
                        [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
                        [91, 92, 93, 94, 95, 96, 97, 0, 98, 99]])
    b4_10_3 = Board([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                        [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                        [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                        [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
                        [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
                        [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
                        [91, 92, 93, 94, 95, 96, 97, 98, 0, 99]])
    b4_10_4 = Board([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                        [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                        [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
                        [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
                        [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
                        [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
                        [91, 92, 93, 94, 95, 96, 97, 98, 99, 0]])
    correct = correctnessTest(solveManhattan, b4_10, 5, [b4_10, b4_10_1, b4_10_2, b4_10_3, b4_10_4], correct)

    b6_4 = Board([[0, 1, 2, 3], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]])
    correct = correctnessTest(solveManhattan, b6_4, 7, None, correct)

    b12_3 = Board([[0, 1, 2], [4, 5, 3], [6, 7, 8]])
    correct = correctnessTest(solveManhattan, b12_3, 13, None, correct)

    b14 = Board([[8,1,3],[4,0,2],[7,6,5]])
    correct = correctnessTest(solveManhattan, b14, 15, None, correct)

    b24 = Board([[3,2,1],[6,5,4],[0,7,8]])
    correct = correctnessTest(solveManhattan, b24, 25, None, correct)
    
    print("This case may take several seconds, longer than the other cases")
    b34_4 = Board([[0, 1, 2, 3], [5, 6, 7, 4], [8, 9, 10, 11], [12, 13, 14, 15]])
    correct = correctnessTest(solveManhattan, b34_4, 35, None, correct)
    
    # Unsolvable board
    b0_twin = Board([[1,2,3],[4,5,6],[8,7,0]])   # twin of b0
    correct = correctnessTest(solveManhattan, b0_twin, 0, None, correct)    

    # Unsolvable board
    b41_twin = Board([[3,0,1],[4,2,5],[7,8,6]])   # twin of b41
    correct = correctnessTest(solveManhattan, b41_twin, 0, None, correct)   


