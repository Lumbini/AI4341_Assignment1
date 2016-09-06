#######################################################################################################################
#
#   CS 4341 - Intro to AI
#   Lumbini Parnas
#   Assignment 1
#
#   Implementation of Iterative Deepening search
#
#######################################################################################################################

#!/usr/bin/python

import math

#This function assumes that the graph is a list of list of permutations
#Test:

def combinations_with_replacement(iterable, r):
    # combinations('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def IDDFS(start, goal, graphSearch):
    
    # Start with depth = 1
    depth = 1

    # Boolean to check if goal has been reached
    success = 0

    # Store the Path array
    path = []

    #explored path

    # Run while loop till goal found,
    while success != 1:
        # Start searching from start Node
        currNode = start;

        # check if the node is the goal
        if currNode == goal:
            success = 1
        
        for level in range(0, depth):
            graphSearch = combinations_with_replacement(range, depth)
            for combinations in graphSearch:
                for node in combinations:
                    check = compute(start, node)
                    path.append(start + node + check)
                    if check == goal:
                        success = 1
                        break
        path = []  
    return path

    
def compute(currNode, nextNode):
    #create an array of chars
    opSet = nextNode.split()

    #if operator is power use the math.pow library
    if opSet[0] == '^':
        return math.pow(currNode,opSet[1])

    #For +, -, *, / use the eval() function
    else:
        magic = str(currNode) + nextNode
        return eval(magic)

if __name__ == "__main__":
    print IDDFS(4, 11, combinations_with_replacement(['+ 3', '/ 2', '* 5', '^ 2'], 3))
