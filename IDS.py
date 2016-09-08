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
import time
import sys
import math

# Read from file
if len(sys.argv) > 1:
    fileName = str(sys.argv[1])
else:
    print 'Please enter Filename'
    
print 'Opening ', fileName
config = open(fileName, 'r', 0)
info = config.readlines()
config.close()


# Assign file contents to appropriate variables
searchMode = info[0]
startVal = int(info[1])
goalVal = int(info[2])
timeAlloc = float(info[3])
legalOps = info[4:]
depth = 0
print 'Search Mode:', searchMode
print 'Starting Value: ', startVal
print 'Goal Value: ', goalVal
print 'Time Allocated: ', timeAlloc, 'seconds'
print 'Legal Operations: ', legalOps

# Variables for output of results
isError = False
numStepsRequired = 0
nodesExpanded = 0
maxSearchDepth = 0

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

def IDDFS(start, goal, timeLimit, opList):
    # Start Timer
    graphList = []

    for operations in opList:
        graphList.append(operations.rstrip('\n'))
        
    startTime = time.time()

    depth = 1
    #number of nodes 
    nodesExpanded = 0

    # Boolean to check if goal has been reached
    success = 0

    # Store the Path array
    path = []

    currentTime = time.time()
    # Run while loop till goal found,
    while (currentTime-startTime) < timeLimit:
        
        graphSearch = combinations_with_replacement(range(len(legalOps)), depth)
        # for x in graphSearch:
        #     print x

        # Restart Path
        path = []
        # Start searching from start Node
        currNode = start;

        # check if the node is the goal
        if currNode == goal:
            success = 1
            print 'Start = Goal. Haha That was easy.'
        

        #Iterate  through the list of list of combinations
        for combinations in graphSearch:
            
            currentTime = time.time()
            #Go through the list of Combination
            for nodes in combinations:
                
                check = compute(currNode, graphList[nodes], depth, nodesExpanded)
                if check is None:
                    break
                nodesExpanded += 1
                
                eqn = [str(currNode) + ' '+ str(graphList[nodes] + ' = ' + str(check))]
                path.extend(eqn)
                if check == goal:
                    success = 1
                    timeTaken = currentTime - startTime
                
                    print 'Iterative Deepening Search completed in ' + str(timeTaken)
                    print 'Depth: ' + str(depth)
                    print 'Nodes Expanded: ' + str(nodesExpanded)
                    print 'Number of equations to reach goal: ' + str(len(path))
                    print 'The equations required to reach goal are: ' 
                    return path
                    break
                currNode = check
        
            
        depth += 1
        currentTime = time.time()
        if depth >= 500 or (currentTime - startTime) > timeAlloc:
            print 'Could not reach goal in given time or depth limit reached'
            print 'Depth: ' + str(depth)
            break
        
def compute(currNode, nextNode, depth, nodesExpanded):
    #create an array of chars
    opSet = nextNode.split(' ')
    # print opSet

    if isinstance(currNode, str):
        currSet = currNode.split(' ')
        number = long(currSet[1])
    else:
        number = long(currNode)
        

    #if operator is power use the math.pow library
    # print str(number) + ' ' +  str(opSet[1])
    # print number
    
    if opSet[0] == '^':
        try:
            result = long(math.pow(long(number), int(opSet[1])))
            return result
            
        except OverflowError:
            print 'Memory limit reached,  Trying next possible operation'
            print 'Nodes Expanded: ' + str(nodesExpanded)
            print 'Depth: ' + str(depth)
            pass

    #For +, -, *, / use the eval() function
    else:
        number = str(currNode) + nextNode
        try:
            return eval(number)
        except TypeError:
            print 'Iterative Deepening Search terminated due to Memory Limitations'
            sys.exit(0)

if __name__ == "__main__":
    #print IDDFS(startVal, goalVal, timeAlloc, legalOps)

    #if searchMode == 'iterative':
    print IDDFS(startVal, goalVal, timeAlloc, legalOps)
    # elif searchMode is 'greedy':
    #     print 'Greedy'
    # else: 
    #     print 'Search Type not available'
