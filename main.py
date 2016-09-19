import time
import sys
import Queue
import random

# Read from file
if len(sys.argv) > 1:
    fileName = str(sys.argv[1])
else:
    fileName = 'test7GA.txt'
print 'Opening ', fileName

config = open(fileName, 'r', 0)
info = config.readlines()
config.close()

# Assign file contents to appropriate variables
searchMode = info[0]
startVal = int(info[1])
goalVal = int(info[2])
timeAlloc = info[3]
legalOps = info[4:]
# print 'Search Mode: ', searchMode
# print 'Starting Value: ', startVal
# print 'Goal Value: ', goalVal
# print 'Time Allocated: ', timeAlloc, 'seconds'
# print 'Legal Operations: ', legalOps

# Variables for output of results
isError = False
numStepsRequired = 0
nodesExpanded = 0
maxSearchDepth = 0
geneticGenerations = 0

#######################################################################################################################################

def geneticFitness(operations, member, start, goal):
    # print 'Evaluating fitness of ', member
    # calculate value obtained by doing operations indicated by member on the start value (operationVal)
    finalValue = start
    for x in range(0, len(member)):
        # print 'Val: ', finalValue
        # print 'X: ', x
        # print 'Member Len: ', len(member)
        # print 'Member: ', member
        finalValue = runOp(finalValue, operations[member[x]])
        if finalValue == goal:
            return 0
    # return true if abs(operationVal - goal) < fitAllowance
    return abs(finalValue - goal)

def crossover(memberOne, memberTwo):
    # print 'Crossover'
    if len(memberTwo) < len(memberOne):
        crossPos = len(memberTwo) / 2
        return memberTwo[0:crossPos] + memberOne[crossPos:len(memberOne)]
    else:
        crossPos = len(memberOne) / 2
        return memberOne[0:crossPos] + memberTwo[crossPos:len(memberTwo)]

def mutate(member, operations):
    # print 'Mutating'
    indexToMutate = random.randrange(0, len(member), 1)
    mutationType = random.randrange(0, 3)
    if mutationType == 0:
        member[indexToMutate] = random.randrange(0, len(operations))
    elif mutationType == 1 and len(member) > 1:
        del member[indexToMutate]
    elif mutationType == 2:
        member.append(random.randrange(0, len(operations)))
    return member

def geneticSearch(population, start, goal, maxTime, operations, popSize, fitAllowance, startTime, bestSoFar, bestDif):
    # print 'running genetic search'
    currentTime = time.time()
    if currentTime - startTime >= maxTime:
        return bestSoFar
    global geneticGenerations
    geneticGenerations += 1
    # generate list of random integers between 0 inclusive and the length of the list of operations non-inclusive
    memberForCrossover = None
    mfcIndex = 0
    for y in range(0, popSize):
        for x in range(1, len(operations) + 1):
            populationSection = random.sample(range(0, len(operations)), x)
            population.append(populationSection)
            # print population

    # run fitness function on each member of population
    offset = 0
    for z in range(0, len(population)):
        currentTime = time.time()
        if currentTime - startTime >= maxTime:
            return bestSoFar
        # if true, store population member for crossover with the next member to return true from the fitness function
        val = geneticFitness(operations, population[z - offset], start, goal)
        if bestDif == -1 or val < bestDif:
            bestSoFar = population[z - offset]
            bestDif = val
        if val == 0:
            for i in range(1, len(population[z - offset]) + 1):
                if geneticFitness(operations, population[z - offset][0:i], start, goal) == 0:
                    # print 'SOLUTION: ', population[z - offset][0:i]
                    return population[z - offset][0:i]
            # print 'SOLUTION: ', population[z - offset]
            return population[z - offset]
        elif val <= fitAllowance:
            # print 'Returned True'
            if memberForCrossover is None:
                mfcIndex = z - offset
                memberForCrossover = population[z - offset]
            else:
                # use crossover() to combine parts of each member and insert this new member into the list
                population.append(crossover(memberForCrossover, population[z - offset]))
                del population[z - offset]
                del population[mfcIndex]
                offset += 2
                memberForCrossover = None
                # print population
        # if false, delete population member and generate a new one
        else:
             del population[z - offset]
             offset += 1
             populationSection = []
             # TO CHANGE size of organisms added after culling, change value of range below
             newSize = 10
             if geneticGenerations > 10:
                 newSize = 10000
             elif geneticGenerations > 5:
                 newSize = 1000
             elif geneticGenerations > 2:
                 newSize = 100
             for i in range(random.randrange(1, newSize, 1)):
                 populationSection.append(random.randrange(0, len(operations) - 1, 1))
             # populationSection = random.sample(range(0, len(operations)), random.randrange(1, len(operations), 1))
             population.append(populationSection)
             # print population
        r = random.randrange(1, 11)
        if r == 3:
            newMember = mutate(population[z - offset], operations)
            population.append(newMember)
            offset += 1

    # Recursively call function with updated population until solution is found
    return geneticSearch(population, start, goal, maxTime, operations, popSize, fitAllowance, startTime, bestSoFar, bestDif)

#######################################################################################################################################
class NodeOp:
    def __init__(self, node, completedOperation, parentNodeOp, depth):
        self.node = node
        self.op = completedOperation
        self.parent = parentNodeOp
        self.depth = depth


# Greedy Search Algorithm
# start is starting number
# goal is the goal number
# maxtime is the maximum time allowed for the search
# operations are the operations given to the search to use
#	operations contains strings of each operation
def greedySearch(start, goal, maxTime, operations):
    done = 0
    path = []
    depth = 1
    maxDepth = 1

    # begin timer for search
    startTime = time.time()

    # add initial node to frontier
    frontier = Queue.PriorityQueue()
    nodesExplored = 1
    if start == goal:
        currentTime = time.time()
        print 'The starting number is the goal'

    else:
        # add children to frontier
        for next in operations:
            newValue = runOp(start, next.rstrip('\n'))
            priority = abs(newValue - goal)
            newNodeOp = NodeOp(newValue, next.rstrip('\n'), start, depth + 1)  # first parent is integer
            frontier.put((priority,newNodeOp))

        currentTime = time.time()

        current = start

        while (currentTime - startTime) < maxTime:
            current = frontier.get()[1]
            if maxDepth < current.depth:
                maxDepth = current.depth

            # print 'Node = ' + str(current.node) + ' Past operator was ' + str(current.op)
            nodesExplored += 1

            # check if current is goal
            if current.node == goal:
                currentTime = time.time()
                break

            # add children to frontier
            for next in operations:
                newValue = runOp(current.node, next.rstrip('\n'))
                priority = abs(newValue - goal)
                newNodeOp = NodeOp(newValue, next.rstrip('\n'), current, current.depth + 1)  # all other parents are NodeOps
                frontier.put((priority,newNodeOp))

            currentTime = time.time()

        # add parent nodes to path
        while True:
            path.append(current)
            if isinstance(current.parent, NodeOp):  # type check. Not sure if this works
                current = current.parent
            else:
                break

        path.reverse()
        printPath(start,path)
        if path[len(path)-1].node != goal:
            print 'Goal not obtained'
        else:
            print 'Goal obtained!'

    # final printing
    print 'Steps Taken: ' + str(len(path))
    print 'Max Depth: ' + str(maxDepth)
    print 'Explored ' + str(nodesExplored) + ' nodes'
    print 'Search took ' + str(currentTime - startTime) + ' seconds'


def printPath(start, path):
    print str(start) + ' ' + path[1].op + ' = ' + str(path[1].node)

    for x in range(1,len(path)):
        print str(path[x-1].node) + ' ' + path[x].op + ' = ' + str(path[x].node)



def runOp(value, operation):
    altValue = float(operation[1:])
    op = operation[0]

    if op == '+':
        newValue = value + altValue
        return newValue
    elif op == '-':
        newValue = value - altValue
        return newValue
    elif op == '/':
        newValue = value / altValue
        return newValue
    elif op == '*':
        newValue = value * altValue
        return newValue
    elif op == '^':
        if value >= 0:
            try:
                newValue = value ** altValue
                return newValue
            except:
                pass
                return 0
        else:
            return 0
    else:  # will cause error if invalid operation
        return

######################################################################################################################################################

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

    depth = 0
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
            if (currentTime - startTime) > timeAlloc:
                break
            currentTime = time.time()
            #Go through the list of Combination
            for nodes in combinations:
                
                check = compute(currNode, graphList[nodes], depth, nodesExpanded)
                if check is None or (currentTime - startTime) > timeAlloc:
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
        if depth >= 50 or (currentTime - startTime) > timeAlloc:
            print 'Could not reach goal in given time or depth limit reached'
            print 'Depth: ' + str(depth)
            print 'Nodes Expanded: ' + str(nodesExpanded)
            print 'Time Taken: ' + str(currentTime-startTime)
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
            result = long(number * 2)
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

def printSolution(sol, start, operations):
    currentVal = start
    for x in range(0, len(sol)):
        print currentVal, operations[sol[x]].rstrip('\n'), '=', runOp(currentVal, operations[sol[x]])
        currentVal = runOp(currentVal, operations[sol[x]])
    return currentVal
#MAIN
######################################################################################################################################################
if __name__ == '__main__':
    # val = runOp(8,'/ 3')
    # print val
    if searchMode.rstrip('\n') == 'greedy':
        greedySearch(startVal, goalVal, float(timeAlloc), legalOps)
    elif searchMode.rstrip('\n') == 'iterative':
        print IDDFS(startVal, goalVal, float(timeAlloc), legalOps)
    elif searchMode.rstrip('\n') == 'genetic':
        populationSize = 100
        fitAllowance = 10
        startTime = time.time()
        solution = geneticSearch([], startVal, goalVal, float(timeAlloc), legalOps, populationSize, fitAllowance, startTime, [], -1)
        searchTime = time.time() - startTime
        finalVal = printSolution(solution, startVal, legalOps)
        print 'Error: ', abs(finalVal - goalVal)
        print 'Size of Organism: ', len(solution)
        print 'Search Required: ', searchTime, 'seconds'
        print 'Population Size: ', populationSize * len(legalOps) * geneticGenerations
        print 'Number of Generations: ', geneticGenerations

