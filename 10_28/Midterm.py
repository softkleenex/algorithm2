#10_28 알고리즘2 2021111470 이상재 중간고사

from queue import PriorityQueue


def findMinCostPath(cost, sx, sy, gx, gy):

#     <그외구현조건>
# -이문제는A*Search를잘이해하고있는지확인하는문제이므로반드시A*Search를사용하도록구현하세요. -(x,y)에서목적지까지의비용을예측하기위해d(x,y)=ManhattanDistance(x,y),(gx,gy))Xmin_cell_cost를
# 사용하세요.min_cell_cost는지도상의비용중가장작은값을의미합니다.
# -입력은올바른값이들어온다고가정하세요.따라서입력이올바름은체크하지않아도됩니다. -첨부파일에서findMinCostPath0함수내부의코드만변경할수있으며,그외코드는변경하지마세요.이들은
# findMinCostPath()함수가올바르게동작하는지검증하기위해사용됩니다.
# -이미import된모듈외추가로import할수없습니다.
# <채점기준>
# -A*Search를수업에서배운최적의방법대로올바르게구현하였음
# -첨부파일에주어진모든testcase를통
    
#     class PriorityQueue(Queue)
#  |  PriorityQueue(maxsize=0)
#  |
#  |  Variant of Queue that retrieves open entries in priority order (lowest first).
#  |
#  |  Entries are typically tuples of the form:  (priority number, data).
#  |
#  |  Method resolution order:
#  |      PriorityQueue
#  |      Queue
#  |      builtins.object
#  |
#  |  Methods inherited from Queue:
#  |

    
    
    # ['__class__', '__class_getitem__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get', '_init', '_put', '_qsize', 'empty', 'full', 'get', 'get_nowait', 'join', 'put', 'put_nowait', 'qsize', 'task_done']
    
    
    
    '''
    INPUT:
        cost: 2D array for cell costs
        sx, sy: x and y of the source
        gx, gy: x and y of the goal

    OUTPUT:
        (1) cost sum of the minimum-cost path, except the source
        (2) list of coordinates in the minimum-cost path
    '''
    min_cell_cost = min(min(row) for row in cost)
    
    def heuristic(x, y):#A* search
        return (abs(x - gx) + abs(y - gy)) * min_cell_cost #맨하탄
    
    pq = PriorityQueue()
    g_costs = {(sx, sy) : 0}
    parents = {(sx, sy) : None}
    visited = set()
    
    pq.put((heuristic(sx, sy), (sx, sy)))    
    
    directions = [(0, 1),(0, -1), (1, 0), (-1, 0)]
    rows, cols = len(cost), len(cost[0])
    
    while not pq.empty():#pq가 빈게 아니라면 반복
        f,(x,y) = pq.get()
        
        if (x, y) in visited:
            continue
        
        visited.add((x, y))
        
        if (x, y) == (gx, gy):
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                new_g = g_costs[(x, y)] + cost[ny][nx]

                if (nx, ny) not in g_costs or new_g < g_costs[(nx, ny)]:
                    g_costs[(nx, ny)] = new_g
                    parents[(nx, ny)] = (x, y)
                    # g(n): 실제비용 h(n):예측비용(맨하탄 거리)
                    f_cost = new_g + heuristic(nx, ny)
                    pq.put((f_cost, (nx, ny)))
    path = []
    current = (gx, gy)
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    
    total_cost = g_costs[(gx, gy)]
    
    return total_cost, path


def correctnessTest(func, input, expected_cost, expected_list, correct):
    print(f"{func.__name__}({input})")
    output = func(*input)
    print(f"output:{output}")
    cost, path = output
    if not (isinstance(cost, int) and 0 <= cost):
        print(f"Fail - the first token of the output must be an integer >= 0")
        correct = False
    elif not isinstance(path, list):
        print(f"Fail - the second token of the output must be a list")
        correct = False
    else:
        if expected_list is None:
            if expected_cost == cost: print("Pass")
            else:
                print(f"Fail - the output cost ({cost}) not match the expected cost ({expected_cost})")
                correct = False                            
        else:
            if expected_cost == cost and expected_list == path: print("Pass")
            else:    
                print(f"Fail - the output does not match the expected output ({expected_cost}, {expected_list})")
                correct = False                            
    print()    

    return correct


if __name__ == "__main__":
    '''
    Unit Test
    '''    
    print("Correctness test for midterm()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True

    correct = correctnessTest(findMinCostPath, ([[1, 1, 1],\
                                                 [1, 1, 1],\
                                                 [1, 1, 1]], 1, 1, 1, 1), 0, [(1, 1)], correct) 

    correct = correctnessTest(findMinCostPath, ([[1, 1, 1],\
                                                 [1, 1, 1],\
                                                 [1, 1, 1]], 0, 0, 2, 0), 2, [(0, 0), (1, 0), (2, 0)], correct)

    correct = correctnessTest(findMinCostPath, ([[1, 9, 1, 1],\
                                                 [1, 9, 1, 1],\
                                                 [1, 2, 1, 9],\
                                                 [9, 9, 1, 1]], 0, 0, 3, 3), 7, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)], correct)

    correct = correctnessTest(findMinCostPath, ([[1, 1, 9, 9, 9, 9],\
                                                 [1, 1, 1, 1, 9, 9],\
                                                 [9, 1, 9, 1, 1, 1],\
                                                 [9, 1, 1, 1, 9, 1],\
                                                 [9, 9, 9, 1, 1, 1]], 0, 0, 5, 4), 9, None, correct)
    # several minimum-cost paths exist (e.g., [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (4, 4), (5, 4)])

    correct = correctnessTest(findMinCostPath, ([[1, 2, 3, 4, 5, 6, 7, 8, 9],\
                                                 [9, 9, 9, 9, 9, 9, 9, 9, 9],\
                                                 [9, 8, 7, 6, 5, 4, 3, 2, 1],\
                                                 [9, 9, 9, 9, 9, 9, 9, 9, 9],\
                                                 [1, 2, 3, 4, 5, 6, 7, 8, 9]], 0, 0, 8, 4), 56, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (8, 3), (8, 4)], correct)
    
    