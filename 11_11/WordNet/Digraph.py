from pathlib import Path
from collections import deque
import math # To use infinity in sap()
import timeit

'''
Class for storing directed graphs
'''
class Digraph:
    def __init__(self, V): # Constructor
        self.V = V # Number of vertices
        self.E = 0 # Number of edges
        self.adj = [[] for _ in range(V)]   # adj[v] is a list of vertices pointed from v

    def addEdge(self, v, w): # Add a directed edge v->w. Self-loops and parallel edges are allowed
        if v<0 or v>=self.V: raise Exception(f"Vertex id {v} is not within the range [{0}-{(self.V-1)}]")
        if w<0 or w>=self.V: raise Exception(f"Vertex id {w} is not within the range [{0}-{(self.V-1)}]")
        self.adj[v].append(w)        
        self.E += 1

    def outDegree(self, v):
        return len(self.adj[v])

    def __str__(self):
        rtList = [f"{self.V} vertices and {self.E} edges\n"]
        for v in range(self.V):
            for w in self.adj[v]:
                rtList.append(f"{v}->{w}\n")
        return "".join(rtList)

    def reverse(self): # return a digraph with all edges reversed
        g = Digraph(self.V)
        for v in range(self.V):
            for w in self.adj[v]: g.addEdge(w, v)
        return g

    '''
    Create a Digraph instance from a file
        fileName: Name of the file that contains graph information as follows:
            (1) the number of vertices, followed by
            (2) one edge in each line, where an edge v->w is represented by "v w"
            e.g., the following file represents a digraph with 2 vertices {0,1} and 2 edges {0->1, 1->0}
            2
            0 1
            1 0
        The file needs to be in the same directory as the current .py file
    '''
    @staticmethod
    def digraphFromFile(fileName):
        filePath = Path(__file__).with_name(fileName)   # Use the location of the current .py file   
        with filePath.open('r') as f:
            phase = 0
            line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
            while line:                                
                if len(line) > 0:
                    if phase == 0: # Read V, the number of vertices
                        g = Digraph(int(line))
                        phase = 1
                    elif phase == 1: # Read edges
                        vw = line.split()
                        if len(vw) != 2: raise Exception(f"Invalid edge format found in {line}")
                        g.addEdge(int(vw[0]), int(vw[1]))                        
                line = f.readline().strip()
        return g
        

'''
Class for storing the results of depth-first search
'''
class DFS:    
    # Constructor
    # Perform DFS on graph g starting from the source vertex s
    def __init__(self, g, s): 
        def recur(v):        
            self.visited[v] = True            
            for w in g.adj[v]:
                if not self.visited[w]: 
                    recur(w)
                    self.fromVertex[w] = v
        assert(isinstance(g, Digraph) and s>=0 and s<g.V)
        self.g, self.s = g, s
        self.visited = [False for _ in range(g.V)]
        self.fromVertex = [None for _ in range(g.V)]
        recur(s)     

    # Return a list of vertices on the path from s to v
    #     based on the results of DFS
    def pathTo(self, v):
        if not self.visited[v]: return None
        path = []
        while v != self.s:
            path.append(v)
            v = self.fromVertex[v]
        path.append(self.s)
        path.reverse()
        return path

    def hasPathTo(self, v):
        return self.visited[v]


'''
Class for storing the results of breadth-first search
'''
class BFS:
    # Constructor
    # PerformBDFS on graph g starting from the source vertex s
    def __init__(self, g, s):        
        assert(isinstance(g, Digraph) and s>=0 and s<g.V)
        self.g, self.s = g, s
        self.visited = [False for _ in range(g.V)]
        self.fromVertex = [None for _ in range(g.V)]
        self.distance = [None for _ in range(g.V)]
        queue = deque()
        queue.append(s)        
        self.visited[s] = True
        self.distance[s] = 0
        while len(queue) > 0:         
            v = queue.popleft()
            for w in g.adj[v]:
                if not self.visited[w]:
                    queue.append(w)
                    self.visited[w] = True
                    self.fromVertex[w] = v
                    self.distance[w] = self.distance[v] + 1

    # Return a list of vertices on the path from s to v
    #     based on the results of DFS
    def pathTo(self, v):
        if not self.visited[v]: return None
        path = []
        while v != self.s:
            path.append(v)
            v = self.fromVertex[v]
        path.append(self.s)
        path.reverse()
        return path

    def hasPathTo(self, v):
        return self.visited[v]

    def distTo(self, v):
        return self.distance[v]


# This function is used to evaluate the speed of sap() function
def BFSforEvaluation(g):
    def bfs(s):
        queue = deque()
        queue.append(s)        
        visited[s] = True
        distance[s] = 0
        while len(queue) > 0:         
            v = queue.popleft()
            for w in g.adj[v]:
                if not visited[w]:
                    queue.append(w)
                    visited[w] = True
                    fromVertex[w] = v
                    distance[w] = distance[v] + 1

    visited = [False for _ in range(g.V)]
    fromVertex = [None for _ in range(g.V)]
    distance = [None for _ in range(g.V)]
    for v in range(g.V):
        if not visited[v]: bfs(v)


'''
Perform the topological sort on a DAG g, and return list of vertices in reverse DFS postorder
'''
def topologicalSort(g):
    def recur(v):        
        visited[v] = True        
        for w in g.adj[v]:            
            if not visited[w]: recur(w)
        reverseList.append(v) # Add v to the stack if all adjacent vertices were visited                

    assert(isinstance(g, Digraph))
    visited = [False for _ in range(g.V)]
    reverseList = []
    for v in range(g.V): 
        if not visited[v]: recur(v)

    reverseList.reverse()
    return reverseList


'''
Perform the topological sort on a DAG g, while detecing any cycle
    If a cycle is found, return None
    Otherwise, return list of vertices in reverse DFS postorder
'''
def topologicalSortWithCycleDetection(g):
    def recur(v):        
        visited[v] = True
        verticesInRecurStack.add(v)
        for w in g.adj[v]:
            if w in verticesInRecurStack: # Edge found to a vertex in the recursive stack
                print("cycle detected on vertex", w)                
                return True
            if not visited[w]: 
                if recur(w): return True
        reverseList.append(v) # Add v to the stack if all adjacent vertices were visited
        verticesInRecurStack.remove(v)
        return False

    assert(isinstance(g, Digraph))
    visited = [False for _ in range(g.V)]
    reverseList = []
    verticesInRecurStack = set() # Initialize set before the first call of recur()
    for v in range(g.V): 
        if not visited[v]:
            #verticesInRecurStack = set() # Initialize set before the first call of recur()
            if recur(v): # Return None if a cycle is detected                
                return None

    reverseList.reverse()
    return reverseList


def cycleDetection(g):
    def recur(v):
        visited[v] = True
        verticesInRecurStack.add(v)
        for w in g.adj[v]:
            if w in verticesInRecurStack: # Edge found to a vertex in the recursive stack
                #print("cycle detected on vertex", w)                
                return True
            if not visited[w]:
                if recur(w): return True
        verticesInRecurStack.remove(v)
        return False

    assert(isinstance(g, Digraph))
    visited = [False for _ in range(g.V)]
    verticesInRecurStack = set() # Initialize set before the first call of recur()
    for v in range(g.V): 
        if not visited[v]:            
            if recur(v): return True
    return False


'''
Find the sap(shortest ancestral path) on digraph g between any vertex in aList and any vertex in bList
Return the common ancestor and the length of sap
'''
def sap(g, aList, bList):
    aSet = set(aList)
    bSet = set(bList)
    common = aSet & bSet
    if common:
        return (list(common)[0], 0)

    visitedA = [None] * g.V
    visitedB = [None] * g.V
    q = deque()

    for v in aList:
        visitedA[v] = 0
        q.append(('A', v, 0))

    for v in bList:
        visitedB[v] = 0
        q.append(('B', v, 0))

    minDist = math.inf
    ancestor = None

    while q:
        src, v, dist = q.popleft()

        if dist >= minDist:
            break

        for w in g.adj[v]:
            if src == 'A':
                if visitedA[w] is None:
                    visitedA[w] = dist + 1
                    q.append(('A', w, dist + 1))

                    if visitedB[w] is not None:
                        total = visitedA[w] + visitedB[w]
                        if total < minDist:
                            minDist = total
                            ancestor = w
            else:
                if visitedB[w] is None:
                    visitedB[w] = dist + 1
                    q.append(('B', w, dist + 1))

                    if visitedA[w] is not None:
                        total = visitedA[w] + visitedB[w]
                        if total < minDist:
                            minDist = total
                            ancestor = w

    return (ancestor, minDist)          

class WordNet:
    def __init__(self, synsetFileName, hypernymFileName): # Constructor
        self.synsets = []
        self.nounToIndex = {}  # (noun, list of indices in self.synsets)

        # Create vertices        
        synsetFilePath = Path(__file__).with_name(synsetFileName)   # Use the location of the current .py file        
        with synsetFilePath.open('r') as f:            
            line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
            while line:
                if len(line) > 0:
                    tokens = line.split(',')
                    self.synsets.append(tokens[1])                    
                    for word in tokens[1].split():
                        if word not in self.nounToIndex: self.nounToIndex[word] = []
                        self.nounToIndex[word].append(int(tokens[0]))
                line = f.readline().strip()
        self.g = Digraph(len(self.synsets))        

        # Create edges        
        hypernymFilePath = Path(__file__).with_name(hypernymFileName)   # Use the location of the current .py file 
        with hypernymFilePath.open('r') as f:
            line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
            while line:
                if len(line) > 0:
                    tokens = line.split(',')
                    v = int(tokens[0])
                    for idx in range(1, len(tokens)):
                        self.g.addEdge(v, int(tokens[idx]))                    
                line = f.readline().strip()
        

        # Check to see if the graph is a rooted DAG
        numVerticesWithZeroOutdegree = 0
        for v in range(self.g.V):
            if self.g.outDegree(v) == 0: 
                numVerticesWithZeroOutdegree += 1
                #print("vertex with 0 outdegree", self.synsets[v])
        if numVerticesWithZeroOutdegree != 1: raise Exception(f"The graph has {numVerticesWithZeroOutdegree} vertices with outdegree=0")

        if cycleDetection(self.g): raise Exception("The graph contains a cycle")

    def nouns(self): # Return all WordNet nouns (for debugging)
        return self.nounToIndex.keys()

    def isNoun(self, word): # Is word a WordNet noun?
        return word in self.nounToIndex

    # Return the shortest common ancestor of nounA and nounB and the distance
    #   in a shortest ancestral path
    def sap(self, nounA, nounB):
        if nounA not in self.nounToIndex: raise Exception(f"{nounA} not in WordNet")
        if nounB not in self.nounToIndex: raise Exception(f"{nounB} not in WordNet")
        sca, distance = sap(self.g, self.nounToIndex[nounA], self.nounToIndex[nounB])
        return self.synsets[sca], distance


def outcast(wordNet, wordFileName):
    words = set()
    filePath = Path(__file__).with_name(wordFileName)   # Use the location of the current .py file   
    with filePath.open('r') as f:        
        line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
        while line:                                
            if len(line) > 0:
                words.update(line.split())                              
            line = f.readline().strip()
    
    maxDistance = -1
    maxDistanceWord = None
    for nounA in words:
        distanceSum = 0
        for nounB in words:
            if nounA != nounB:
                _, distance = wordNet.sap(nounA, nounB)
                distanceSum += distance
        if distanceSum > maxDistance:
            maxDistance = distanceSum
            maxDistanceWord = nounA
    
    return maxDistanceWord, maxDistance, words


def sapTest(g, aList, bList, expectedOutputs, correct):
    result = sap(g, aList, bList)
    print(f"sap(g, {aList}, {bList}): {result}")        
    if result in expectedOutputs: print("pass")
    else:
        print(f"fail - expected outputs are {expectedOutputs}")
        correct = False
    return correct


def wnTest(wn, aWord, bWord, expectedOutput, correct):
    result = wn.sap(aWord, bWord)
    print(f"wn.sap({aWord}, {bWord}): {result}")
    if result != None and len(result) == 2 and result[1] == expectedOutput: print("pass")
    else:
        print(f"fail - expected output is {expectedOutput}")
        correct = False
    return correct


def outcastTest(wn, fileName, expectedOutput, correct):
    result = outcast(wn, fileName)
    print(f"outcast(wn, {fileName}): {result}")
    if result != None and len(result) == 3 and result[0] == expectedOutput: print("pass")
    else:
        print(f"fail - expected output is {expectedOutput}")
        correct = False
    return correct


if __name__ == "__main__":   
    correct = True
    print('if your answer does not appear within 5 seconds, consider that you fail the case')
    
    # Unit test for sap()
    print('test sap()')    
    print('digraph6.txt')
    d6 = Digraph.digraphFromFile('digraph6.txt')
    correct = sapTest(d6, [1], [5], [(0, 2)], correct)
    correct = sapTest(d6, [1], [1], [(1, 0)], correct)
    correct = sapTest(d6, [1], [4], [(0, 3), (4, 3)], correct)
    correct = sapTest(d6, [1], [3], [(3, 2)], correct)

    print('digraph12.txt')
    d12 = Digraph.digraphFromFile('digraph12.txt')
    correct = sapTest(d12, [3], [10], [(1, 4)], correct)
    correct = sapTest(d12, [3], [10, 2], [(0, 3)], correct)
    
    print('digraph25.txt')
    d25 = Digraph.digraphFromFile('digraph25.txt')
    correct = sapTest(d25, [13, 23, 24], [6, 16, 17], [(3, 4)], correct)
    correct = sapTest(d25, [13, 23, 24], [6, 16, 17, 4], [(3, 4), (1, 4)], correct)
    correct = sapTest(d25, [13, 23, 24], [6, 16, 17, 1], [(1, 3)], correct)
    correct = sapTest(d25, [13, 23, 24, 17], [6, 16, 17, 1], [(17, 0)], correct)


    # Unit test with WordNet
    print()
    print('test WordNet')
    wn = WordNet("synsets.txt", "hypernyms.txt")
    print(wn.isNoun("blue"))
    print(wn.isNoun("fox"))
    print(wn.isNoun("lalala"))
    correct = wnTest(wn, "blue", "red", 2, correct)
    correct = wnTest(wn, "blue", "fox", 8, correct)
    correct = wnTest(wn, "apple", "banana", 2, correct)
    correct = wnTest(wn, "George_W._Bush", "JFK", 2, correct)
    correct = wnTest(wn, "George_W._Bush", "Eric_Arthur_Blair", 7, correct)
    correct = wnTest(wn, "George_W._Bush", "chimpanzee", 17, correct)

    print('test outcast()')
    correct = outcastTest(wn, "outcast5.txt", "table", correct)
    correct = outcastTest(wn, "outcast8.txt", "bed", correct)
    correct = outcastTest(wn, "outcast11.txt", "potato", correct)
    correct = outcastTest(wn, "outcast9.txt", "fox", correct)
    
    
    # Unit test for speed
    print()
    print('test speed')
    if not correct: print("fail since the algorithm is not correct")
    else:
        n, mult = 20, 80
        dwn = Digraph.digraphFromFile('digraph_wordnet.txt')
        tBFS = timeit.timeit(lambda: BFSforEvaluation(dwn), number=n)/n    
        tSAP = timeit.timeit(lambda: sap(dwn, [62294, 62295], [21240, 21241]), number=n)/n    # potato and apple    
        print(f"{n} calls of sap() on dwn took {tSAP * 10**3:.10f} msec on average, and the same number of calls of BFS() / {mult} took {tBFS * 10**3 / mult:.10f} msec on average")
        if tSAP < tBFS / mult: print("pass")
        else: print("fail") 