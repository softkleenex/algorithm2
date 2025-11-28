from queue import PriorityQueue
from RedBlackBST import LLRB


class Segment:
    def __init__(self, x1, y1, x2, y2):
        assert(x1==x2 or y1==y2) # Accept either a horizontal or vertical segment  
        assert(not (x1==x2 and y1==y2)) # Two end points cannot be equal              

        # Put smaller values in (x1,y1) and larger values in (x2,y2)
        if x1==x2:            
            if y1 < y2: self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            else: self.x1, self.y1, self.x2, self.y2 = x1, y2, x2, y1
        elif y1==y2:
            if x1 < x2: self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
            else: self.x1, self.y1, self.x2, self.y2 = x2, y1, x1, y2
    
    def isHorizontal(self):
        return self.y1 == self.y2

    def isVertical(self):
        return self.x1 == self.x2

    # Create a human-readable string representation
    def __str__(self):
        return f"({self.x1},{self.y1})--({self.x2},{self.y2})"

    def __repr__(self): # Called when a Segment is printed as an element of a list
        return self.__str__()

    # Defines behavior for the equality operator, ==
    # This operator is required for grading
    def __eq__(self, other):
        if other == None: return False
        if not isinstance(other, Segment): return False        
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2


'''
segments: list of Segment objects
return value: list of Segment pairs that intersect
'''
def sweepLine(segments):
    pq = PriorityQueue()
    bst = LLRB()
    result = []

    for seg in segments:
        if seg.isHorizontal():
            pq.put((seg.x1, 0, seg))
            pq.put((seg.x2, 2, seg))
        else:
            pq.put((seg.x1, 1, seg))

    while pq.qsize() > 0:
        event = pq.get()
        x, event_type, seg = event

        if event_type == 0:
            bst.put(seg.y1, seg)
        elif event_type == 2:
            bst.delete(seg.y1)
        else:
            y_list = bst.rangeSearch(seg.y1, seg.y2)
            for y in y_list:
                h_seg = bst.get(y)
                result.append((h_seg, seg))

    return result


def correctnessTest(func, input, expected_output, correct):
    print(f"{func.__name__}({input})")
    output = func(input)
    print(f"output:{output}")
    if output is not None and isinstance(output, list):
        if expected_output == output: print("Pass")
        else:    
            print(f"Fail - the output does not match the expected output {expected_output}")
            correct = False                        
    else:
        print(f"Fail - output is NOT a list")
        correct = False
    print()    

    return correct


if __name__ == "__main__":
    '''
    Unit Test
    '''    
    print("Correctness test for sweepLine()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True

    input = [Segment(0,1,15,1), Segment(1,4,8,4), Segment(3,8,11,8), Segment(9,6,16,6)]
    expected_output = []
    correct = correctnessTest(sweepLine, input, expected_output, correct)

    input = [Segment(-8,0,8,0), Segment(-7,-1,-7,8), Segment(-6,-2,-6,5), Segment(0,1,0,-10), Segment(5,-3,5,10)]
    expected_output = [(Segment(-8,0,8,0), Segment(-7,-1,-7,8)), (Segment(-8,0,8,0), Segment(-6,-2,-6,5)),\
                       (Segment(-8,0,8,0), Segment(0,-10,0,1)), (Segment(-8,0,8,0), Segment(5,-3,5,10))]
    correct = correctnessTest(sweepLine, input, expected_output, correct)

    input = [Segment(3,3,8,3), Segment(4,1,4,8), Segment(7,2,7,10), Segment(1,7,12,7)]
    expected_output = [(Segment(3,3,8,3), Segment(4,1,4,8)), (Segment(1,7,12,7), Segment(4,1,4,8)),\
                       (Segment(3,3,8,3), Segment(7,2,7,10)), (Segment(1,7,12,7), Segment(7,2,7,10))]
    correct = correctnessTest(sweepLine, input, expected_output, correct)

    input = [Segment(0,1,15,1), Segment(14,0,14,2), Segment(1,4,8,4), Segment(6,3,6,7),\
        Segment(2,5,4,5), Segment(3,8,11,8), Segment(9,6,16,6), Segment(13,5.5,13,9.5)]
    expected_output = [(Segment(1,4,8,4), Segment(6,3,6,7)), (Segment(9,6,16,6), Segment(13,5.5,13,9.5)),\
        (Segment(0,1,15,1), Segment(14,0,14,2))]
    correct = correctnessTest(sweepLine, input, expected_output, correct)
   
    input = [Segment(1,3,6,3), Segment(5,0,5,9), Segment(4,7,9,7), Segment(8,6,8,10),\
        Segment(10,4,13,4), Segment(11,2,17,2), Segment(12,1,12,5), Segment(15,5.5,15,7.5), Segment(14,6.5,16,6.5)]
    expected_output = [(Segment(1,3,6,3), Segment(5,0,5,9)), (Segment(4,7,9,7), Segment(5,0,5,9)),\
                       (Segment(4,7,9,7), Segment(8,6,8,10)), (Segment(11,2,17,2), Segment(12,1,12,5)),\
                        (Segment(10,4,13,4), Segment(12,1,12,5)), (Segment(14,6.5,16,6.5), Segment(15,5.5,15,7.5))]
    correct = correctnessTest(sweepLine, input, expected_output, correct)

    
    
    
    
    