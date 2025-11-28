import random
import timeit

#기본 정렬함수 못씀


def quickSelect(a, k, m): #리스트 a에서 크기순으로 K ~ m번쨰 원소를 찾아 순서대로 리스트에 담아 반환하는 함수 구현
    '''
    Find all elements (in order) in between k-th and m-th smallest elements, 
        including the k-th and the m-th, where 0 <= k <= m <= len(a)-1
    '''
    assert isinstance(a, list) 
    assert isinstance(k, int) and isinstance(m, int) and 0 <= k and k <= m and m <= len(a)-1
    #qucik selection사용하면 될듯, k랑m이 기준이여야 함
    
    '''
    Speed test for selecting 100000 out of 100000 elements with 3 unique keys
    QuickSort and QuickSelect(0, 99999) took 0.0697149590 and 0.0734102500 seconds
    thus tSpeedCompare / tQuickSelect = 0.9496624653, which must be > 2.0
    Fail떄문에 3way partition사용해야함'''
    
    # Partition a[lo~hi] into 3-sections and then continue to partition each half recursively
    def partition3Way(a, lo, hi):
        if (hi <= lo): return
        v = a[lo]
        lt, gt = lo, hi  # Indices to put next items <v and >v    
        i = lo
        while i <= gt:
            if a[i] < v:
                a[lt], a[i] = a[i], a[lt]  # Swap
                lt, i = lt+1, i+1
            elif a[i] > v:
                a[gt], a[i] = a[i], a[gt]  # Swap
                gt = gt-1
            else: i = i+1
        
        return (lt, gt)
    

    random.shuffle(a)  # 한 번만 셔플
    

    def selectRange(lo, hi):
        if lo >= hi: return

        lt, gt = partition3Way(a, lo, hi) #less than / greater than

        # k~m 범위에 따라 선택적 재귀
        if gt < k:  # k~m이 오른쪽에만
            selectRange(gt+1, hi)
        elif lt > m:  # k~m이 왼쪽에만
            selectRange(lo, lt-1)
        else:  # k~m이 pivot 영역과 겹침
            if lt > lo and k < lt:  # 왼쪽에 필요한 부분 있으면
                selectRange(lo, lt-1)
            if gt < hi and m > gt:  # 오른쪽에 필요한 부분 있으면
                selectRange(gt+1, hi)



    selectRange(0, len(a)-1)
    
    return a[k:m+1] 
        
    
    




def speedCompare(a):
    def recur(a, lo, hi):
        if hi <= lo: return

        i, j = lo+1, hi
        while True:
            while i <= hi and a[i] < a[lo]: i = i+1
            while j >= lo+1 and a[j] > a[lo]: j = j-1

            if (j <= i): break
            a[i], a[j] = a[j], a[i]
            i, j = i+1, j-1
        a[lo], a[j] = a[j], a[lo]        
           
        recur(a, lo, j-1)
        recur(a, j+1, hi)

    random.shuffle(a)
    recur(a, 0, len(a)-1)
    return a


def testCorrectness(a, k, m, expectedOutput, correct, output2console):    
    print(f"Correctness test for selecting {m-k+1} out of {len(a)} elements")
    output = quickSelect(a.copy(), k, m)
    if output2console: print(f"quickSelect({a}, {k}, {m}) = {output}")
    if output == expectedOutput: print("Pass")
    else:
        print("Fail")
        if output2console: print(f"expected output = {expectedOutput}")
        correct = False
    print()

    return correct


if __name__ == "__main__":    
    correct = True

    a = [2, 9, 3, 0, 6, 1, 4, 5, 7, 8]
    correct = testCorrectness(a, 0, 0, [0], correct, True)
    correct = testCorrectness(a, 3, 5, [3, 4, 5], correct, True) 
    correct = testCorrectness(a, 6, 9, [6, 7, 8, 9], correct, True)
    correct = testCorrectness(a, 0, 9, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], correct, True)

    size, k, m = 100, 57, 73
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False)

    size, k, m = 10000, 2000, 2100
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False) 

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in random order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        random.shuffle(a)
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 1.7")
        if tSpeedCompare / tQuickSelect > 1.7: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in ascending order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 2.0")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 0, 100000 - 1, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements with 3 unique keys")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [random.randint(0,2) for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n        
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}, which must be > 2.0")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()
    