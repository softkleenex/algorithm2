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
    
    for idx in range(N):    
        ids.append(idx)
        size.append(1)

    def root(i):
        while i != ids[i]: i = ids[i]
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

    
    v = [i for i in range(0, n) ]#정점 저장
    wallsToOpen_set = set(sorted(v, v1) for v1 in v if (abs(v - v1) == 1 or abs(v - v1) == n) and v1 >= 0)
    print(wallsToOpen)
    #벽 목록, abs로 차이가 1 혹은 N인 경우 set생성
    removed_walls = []
    
    for i in range(t):
        wallsToOpen = list(wallsToOpen) 
        random.shuffle(wallsToOpen)
        while connected(0, n * n - 1) == False: #n = 3이라면, 0 이랑 8 이 연결되지 않는 한 계속!
            
            tempwall = wallsToOpen.pop
            tempids = [x for x in ids]
            union(tempwall[0], tempwall[1])
            if ids == tempids:
                pass
            else:
                
    
    
        
        
    
  
    
    
     

    return statistics.mean(), statistics.stdev(), removed_walls



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
    