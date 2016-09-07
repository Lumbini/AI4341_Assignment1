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
import time

depth = 1
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

def IDDFS(start, goal, timeLimit):
    # Start Timer
    startTime = time.time()

    depth = 1
    graphList = ['+ 3', '/ 2' ,'- 1','* 5', '^ 2']

    # Boolean to check if goal has been reached
    success = 0

    # Store the Path array
    path = []

    currentTime = time.time()
    # Run while loop till goal found,
    while (currentTime-startTime) < timeLimit:
        
        graphSearch = combinations_with_replacement(range(5), depth)

        # Restart Path
        path = []
        # Start searching from start Node
        currNode = start;

        # check if the node is the goal
        if currNode == goal:
            success = 1
        
        for combinations in graphSearch:
            currentTime = time.time()
            for nodes in combinations:
                check = compute(currNode, graphList[nodes])
                eqn = [str(currNode) + str(graphList[nodes] + '=' + str(check))]
                path.extend(eqn)
                if check == goal:
                    success = 1
                    timeTaken = currentTime - startTime
                    print 'Iterative Deepening Search completed in ' + str(format(timeTaken, '.4f'))
                    print 'The equations required to reach goal are: '
                    return path
                    break
                else: currNode = check
        depth += 1
        currentTime = time.time()
    

    
def compute(currNode, nextNode):
    #create an array of chars
    opSet = nextNode.split(' ')
    # print opSet

    if isinstance(currNode, str):
        currSet = currNode.split(' ')
        number = currSet[1]
    else:
        number = currNode

    #if operator is power use the math.pow library
    # print str(number) + ' ' +  str(opSet[1])
    if opSet[0] == '^':
        return math.pow(int(number), int(opSet[1]))

    #For +, -, *, / use the eval() function
    else:
        magic = str(currNode) + nextNode
        return eval(magic)


if __name__ == "__main__":
    print IDDFS(4, 11, 2.5)
