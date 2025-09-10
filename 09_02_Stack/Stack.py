'''
Class that represents a stack
'''
class Stack:
    def __init__(self): # Constructor
        self.list = [] 
        pass

    def push(self, x): # Add to the end
        self.list.append(x)
        pass

    def pop(self): # Return the last item              
        if len(self.list) == 0:
            return None
        else:
            return self.list.pop()

def correctnessTest(input, expected_output, correct):
    print(f"input:{input}")
    s = Stack()
    for e in input: s.push(e)
    result = []
    for _ in range(len(expected_output)): result.append(s.pop())
    print(f"output:{result}")
    if result == expected_output: print("Pass")
    else: 
        print(f"Fail: output is not equal to the expected output {expected_output}")
        correct = False
    print()

    return correct


if __name__ == "__main__": 
    '''
    Unit Test
    '''    
    print("Correctness test for class Stack")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True
    
    input, expected_output = [], [None, None]
    correct = correctnessTest(input, expected_output, correct)

    input, expected_output = [1, 2, 3, 4], [4, 3, 2, 1, None, None]
    correct = correctnessTest(input, expected_output, correct)
    
    input, expected_output = [-25, 4, 100, 72, -11, 16], [16, -11, 72, 100, 4, -25, None, None, None, None, None, None, None]
    correct = correctnessTest(input, expected_output, correct)
