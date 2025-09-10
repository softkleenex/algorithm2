import statistics
import math
import random
import timeit

def simulate(n, t):#n * n 격자에 대해 t회 시뮬레이션
    assert isinstance(n, int) and n >= 2, f"n = {n} must be an integer >= 2"
    assert isinstance(t, int) and t >= 2, f"t = {t} must be an integer >= 2"
    
    N = n * n
    
    ids = []
    size = []   # size[i]: size of tree rooted at i
    
    
        

    def root(i):
        if i != ids[i]:
            i = root(ids[i])
        return i

    def connected(p, q):
        return root(p) == root(q)

    def union(p, q):    
        id1, id2 = root(p), root(q)
        if id1 == id2: return
        if size[id1] <= size[id2]: 
            ids[id1] = id2
            size[id2] += size[id1]
        else:
            ids[id2] = id1
            size[id1] += size[id2]

    
    
    v = [i for i in range(0, n * n) ]#정점 저장
    wallsToOpen_set = set()
    
    for v1 in v:
        for v2 in v:
            if v1 < v2:  # 중복 방지
                # 가로로 인접 (같은 행에서 차이가 1)
                if abs(v1 - v2) == 1 and v1 // n == v2 // n:
                    wallsToOpen_set.add((v1, v2))
                # 세로로 인접 (같은 열에서 차이가 n)
                elif abs(v1 - v2) == n:
                    wallsToOpen_set.add((v1, v2))

    #벽 목록, abs로 차이가 1 혹은 N인 경우 set생성
   
    walls_count = list()
    
    for i in range(t):

        ids = [_ for _ in range(N)]
        size = [1 for _ in range(N)]
        walls_count_temp = 0
        removed_walls = []
        wallsToOpen = list(wallsToOpen_set) 
        random.shuffle(wallsToOpen)
        while connected(0, n * n - 1) == False and wallsToOpen: #n = 3이라면, 0 이랑 8 이 연결되지 않는 한 계속!
            
            tempwall = wallsToOpen.pop()#랜덤하게 켜플된 벽에서 끝부분 pop < 끝부분이여도 상관 x
            
            root1, root2 = root(tempwall[0]), root(tempwall[1])
            if root1 != root2:  # 두개가 끊겨있던건가?
                union(tempwall[0], tempwall[1])#그렇다면 연결
                removed_walls.append(tempwall)
                walls_count_temp += 1
            else:#상태가 똑같다면
                pass
            
        
        walls_count.append(walls_count_temp/ len(wallsToOpen_set))
    
    
        
        
    
  
    
    

    return statistics.mean(walls_count), statistics.stdev(walls_count), removed_walls

'''
Simulate the performance of Quick Find
'''
def simulateQF(n, t):
    def connected(p, q):        
        return ids[p] == ids[q]

    def minMax(a, b):
        if a < b: return a, b
        else: return b, a

    def union(p, q):        
        id1, id2 = minMax(ids[p], ids[q])
        for idx, _ in enumerate(ids):
            if ids[idx] == id2: ids[idx] = id1
    
    for _ in range(t):
        numCells, numWalls = n * n, int(1.2 * n * (n - 1))
        ids = [i for i in range(numCells)]
        for _ in range(numWalls):
            union(random.randint(0, len(ids)-1), random.randint(0, len(ids)-1))
            connected(0, numCells - 1)

'''
Verify the maze maze 검증하기
'''
def verify(n, selectedWalls):
    def connected(p, q):        
        return ids[p] == ids[q]

    def minMax(a, b):
        if a < b: return a, b
        else: return b, a

    def union(p, q):        
        id1, id2 = minMax(ids[p], ids[q])
        for idx, _ in enumerate(ids):
            if ids[idx] == id2: ids[idx] = id1
    
    illegalConnections = []
    illegalVertices = []
    for id1, id2 in selectedWalls:
        minID, maxID = minMax(id1, id2)
        if maxID >= n * n or minID < 0: illegalVertices.append((id1, id2))
        if minID + 1 == maxID and minID % n < n - 1: continue
        elif minID + n == maxID and minID < n * (n - 1): continue
        else: illegalConnections.append((id1, id2))        

    if len(illegalVertices) > 0:
        print()
        print(f"cell numbers must be within 0 ~ {n * n - 1}, and thus the following cells are out of range: {illegalVertices}")
        return False

    if len(illegalConnections) > 0:    
        print()
        print(f"the following cells must not be connected: {illegalConnections}")
        return False
    
    ids = [i for i in range(n * n)]    
    for id1, id2 in selectedWalls: 
        if connected(id1, id2): illegalConnections.append((id1, id2))
        else: union(id1, id2)
    
    if len(illegalConnections) > 0:    
        print()
        print(f"the following connections must not be made as the cells are already connected: {illegalConnections}")
        print(f"the entire connections are: {selectedWalls}")
        return False

    if not connected(0, n * n - 1):
        print()
        print(f"no path exists from cell 0 to cell {n * n - 1} with the following connections: {selectedWalls}")
        return False
    
    return True














'''
Unit Test
'''
if __name__ == "__main__":
    print("Correctness test for simulate()")
    print("For each test case, if your answer does not appear within 10 seconds, then consider that you failed the case")
    correct = True
    
    input = 2, 10000
    rt_val = simulate(*input)           
    print(f"simulate{input}: ({rt_val[0]:.5f}, {rt_val[1]:.5f}) ", end="")
    if verify(input[0], rt_val[2]): 
        print("Pass ", end="")
        if math.floor(rt_val[0]*100) == 66: print("Pass ", end="")
        else:
            print(f"Fail (the average must be 0.66xxx) ", end="")
            correct = False
        if round(rt_val[1]*100) == 12: print("Pass ", end="")
        else:
            print(f"Fail (the stdev must round up to 0.12) ", end="")
            correct = False
        print()
    else: 
        print("Fail Fail Fail")
        correct = False

    input = 4, 10000
    rt_val = simulate(*input)     
    print(f"simulate{input}: ({rt_val[0]:.5f}, {rt_val[1]:.5f}) ", end="")
    if verify(input[0], rt_val[2]):
        print("Pass ", end="")
        if math.floor(rt_val[0]*100) == 57: print("Pass ", end="")
        else:
            print(f"Fail (the average must be 0.57xxx) ", end="")
            correct = False
        if round(rt_val[1]*100) == 6: print("Pass ", end="")
        else:
            print(f"Fail (the stdev must round up to 0.06) ", end="")
            correct = False
        print()        
    else: 
        print("Fail Fail Fail")
        correct = False

    input = 10, 2
    rt_val = simulate(*input)
    print(f"simulate{input}: ({rt_val[0]:.5f}, {rt_val[1]:.5f}) ", end="")    
    if verify(input[0], rt_val[2]): print("Pass")
    else: print("Fail")

    print()
    print("Speed test for simulate()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        input = 10, 100
        simulateCompare = simulateQF
        tSubmittedCode = timeit.timeit(lambda: simulate(*input), number=repeat) / repeat
        tCodeToCompare = timeit.timeit(lambda: simulateCompare(*input), number=repeat) / repeat
        print(f"Average running time of simulate{input} and {simulateCompare.__name__}{input} * 0.35 : {tSubmittedCode:.10f} and {tCodeToCompare * 0.31:.10f} ", end="")        
        if tSubmittedCode < tCodeToCompare * 0.35: print("Pass ", end="")
        else:
            print("Fail (the average running time of simulate() must be < 0.35 * the running time of QF-based method)", end="")
        print()                   
    