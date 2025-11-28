import math
import timeit
import random


# Given a list of points (x, y)
#   find the convex hull using Graham's Scan
# Return a list of points in the convex hull in ccw order
# 이 함수를 구현해야 한다
#i > j, i > k에 대해서 외적인 


#Hsort
def shellSort(a):
    N = len(a)
    h = 1
    while h < N / 3:
        h = 3 * h + 1   # Knuth's Sequence 1, 4, 13, 40, 121, 364, ...

    numSwapsTotal = 0
    while h >= 1:        
        _, numSwaps = hInsertionSort(a, h)
        numSwapsTotal += numSwaps
        h = h // 3
    
    return a, numSwapsTotal

def hInsertionSort(a, h):
    numSwaps = 0  
    for i in range(h, len(a)):  # Begin from a[h]
        key = a[i]     # Element to move at current iteration
        j = i - h
        while j >= 0 and a[j][0] > key[0]:
            a[j + h] = a[j]  # Move element a[j] to a[j+h] if a[j] > key
            numSwaps += 1
            j -= h         # Decrement j by h
        a[j + h] = key   # Place the key to the farthest it can go to the left      
    return a, numSwaps
#Hsort

def grahamScan(points):
    
    
    px, py  = min(points, key = lambda x : (x[1], -x[0])) #y는 작고, x는 커야한다!!!
    
    points = points.copy()
    points.remove((px, py))
    
    angle_points = list()

    for i in range(len(points)):
        tx, ty = points[i][0], points[i][1]
        temp_angle = math.atan2(points[i][1] - py , points[i][0] - px)
        angle_points.append((temp_angle,(points[i][0], points[i][1])))
       
    #시작점은 가장 우측 하단이고, atan2는 우측 0, 좌측-180이기에, 각도가 작은것부터 포함해야한다

    sorted_angle_points, temp = shellSort(angle_points)
    
        
    
    now_points = [(px, py)]
    for i in range(len(sorted_angle_points)):
        now_points.append(tuple(sorted_angle_points[i][1]))
        
        # 점을 추가한 직후 볼록성 검사
        while len(now_points) >= 3 and not isconvex(now_points[-3], now_points[-2], now_points[-1]):
            now_points.pop(-2)
    
    #마지막 점 체크!
    while len(now_points) >= 3 and not isconvex(now_points[-2], now_points[-1], now_points[-0]):
        now_points.pop(-1)

    
    return now_points

def isconvex(i, j, k):#점세개 a > b / b > c에 대해서, 점 b로 인해서 생기는 벡터가 볼록하다면 True > pass
   
    #교안에서는,, i > j > k 라면

    
    cross_product = (j[0] - i[0]) * (k[1] - i[1]) - (j[1] - i[1])*(k[0] -i[0])
    
    if cross_product > 0:#
        return True
    else:
        return False # ==0, 직선이거나,  < 0 이면 false, b를 제거해야한다




def correctnessTest(input, expected_output, correct):
    output = grahamScan(input)
    print(f"grahamScan({input})\n{output}")
    if output == expected_output: print("Pass")
    else:        
        print(f"Fail - expected output: {expected_output}")
        correct = False
    print()    

    return correct


def simulateNSquare(points):    
    points = sorted(points, key = lambda p: (p[1], -p[0]))     
    for i in range(len(points)):
        points_with_angle = []
        for j in range(i + 1, len(points)):
            x, y = points[j]
            points_with_angle.append((x, y, math.atan2(y - points[i][1], x - points[i][0])))
        points_with_angle = sorted(points_with_angle, key = lambda p: p[2])


'''
Unit Test
'''
if __name__ == "__main__":
    '''# ccw turns
    print(ccw((0,0), (-1,1), (-2, -1)))
    print(ccw((-1,1), (-2, -1), (0,0)))
    print(ccw((-2, -1), (0,0), (-1,1)))

    # non-ccw turns
    print(ccw((0,0), (-2, -1), (-1,1)))
    print(ccw((-2, -1), (-1,1), (0,0)))
    print(ccw((-1,1), (0,0), (-2, -1)))
    print(ccw((0,0), (-1, 1), (-2, 2))) # Straight line'''

    print("Correctness test for grahamScan()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True
    
    input = [(3, -1), (2, -2), (4, -1)]
    expected_output = [(2, -2), (4, -1), (3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(0, 0), (-2, -1), (-1, 1), (1, -1), (3, -1), (-3, -1)]
    expected_output = [(3, -1), (-1, 1), (-3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(4, 2), (3, -1), (2, -2), (1, 0), (0, 2), (0, -2), (-1, 1), (-2, -1), (-2, -3), (-3, 3), (-4, 0), (-4, -1), (-4, -2), (-4, -3), (-4, -4)]
    expected_output = [(-4, -4), (2, -2), (3, -1), (4, 2), (-3, 3), (-4, 0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2)]
    expected_output = [(-2, -2), (1, -1), (2, 0), (2, 2), (0, 2), (-1, 1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2), (-2, 2), (4, -4)]
    expected_output = [(4, -4), (2, 2), (-2, 2), (-2, -2)]
    correct = correctnessTest(input, expected_output, correct)

    # "342235" is a 6-digit number and is greater than the other 5-digit numbers
    input = [(342235, -23412), (-74545, 72345), (25812, -45689), (-45676, 24578), (45689, 0), (-74545, 0), (0, 45689), (0, -45689)]
    expected_output = [(25812, -45689), (342235, -23412), (-74545, 72345), (-74545, 0), (0, -45689)]
    correct = correctnessTest(input, expected_output, correct)
    
    print()
    print("Speed test for grahamScan()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        inputLength = 100
        minC, maxC = -1000000, 1000000
        points = [(random.randint(minC, maxC), random.randint(minC, maxC)) for _ in range(inputLength)]
        tCodeToCompare = timeit.timeit(lambda: simulateNSquare(points), number=repeat) / repeat
        tSubmittedCode = timeit.timeit(lambda: grahamScan(points), number=repeat) / repeat        
        print(f"Average running time of grahamScan() and simulateNSquare() * 0.2 with {inputLength} points: {tSubmittedCode:.10f} and {tCodeToCompare * 0.2:.10f}")                
        if tSubmittedCode < tCodeToCompare * 0.2: print("Pass")
        else:
            print("Fail")
        print() 