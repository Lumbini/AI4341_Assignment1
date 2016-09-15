import time
import sys
import Queue
import random

# Read from file
if len(sys.argv) > 1:
    fileName = str(sys.argv[1])
else:
    fileName = 'test.txt'
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
print 'Search Mode: ', searchMode
print 'Starting Value: ', startVal
print 'Goal Value: ', goalVal
print 'Time Allocated: ', timeAlloc, 'seconds'
print 'Legal Operations: ', legalOps

# Variables for output of results
isError = False
numStepsRequired = 0
nodesExpanded = 0
maxSearchDepth = 0

########################################################################################################################


def calculate_fitness(operations, member, start, goal):
    tmp_val = start
    for x in range(0, len(member)):
        tmp_val = runOp(tmp_val, operations[member[x]])
    return abs(tmp_val - goal)


def genetic_search(start_value, target_value, time_limit, operations):
    population = Queue.PriorityQueue()

    for i in range(0, 10):
        organism = []
        num_of_operations = random.randrange(5, 25)
        val = start_value
        for j in range(0, num_of_operations):
            if random.randint(0, 4):
                #  use greedy
                present_best = sys.maxint
                operator_to_add = -1
                for k in range(0, len(legalOps)):
                    tmp_val = runOp(val, operations[k])
                    if operator_to_add < 0 or abs(tmp_val - target_value) < abs(present_best - target_value):
                        present_best = tmp_val
                        operator_to_add = operations[k]
            else:
                operator_to_add = operations[random.randint(0, len(operations)-1)]
            organism.append(operator_to_add)
            val = runOp(val, operator_to_add)
        population.put((abs(val - target_value), organism))
        organism = []
    flag = True

    org1 = population.get()
    org2 = population.get()
    cross_position = len(org2[1]) / 2
    org3 = org1[0:cross_position] + org2[cross_position:len(org2[1])]
    print org1
    print org2
    print org3


#######################################################################################################################


class NodeOp:
    def __init__(self, node, completedOperation, parentNodeOp):
        self.node = node
        self.op = completedOperation
        self.parent = parentNodeOp


# Greedy Search Algorithm
# start is starting number
# goal is the goal number
# maxtime is the maximum time allowed for the search
# operations are the operations given to the search to use
#	operations contains strings of each operation
def greedySearch(start, goal, maxTime, operations):
    done = 0
    path = []

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
            newNodeOp = NodeOp(newValue, next.rstrip('\n'), start)  # first parent is integer
            frontier.put((priority,newNodeOp))

        currentTime = time.time()

        current = start

        while (currentTime - startTime) < maxTime:
            current = frontier.get()[1]
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
                newNodeOp = NodeOp(newValue, next.rstrip('\n'), current)  # all other parents are NodeOps
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
    print 'Search took ' + str(currentTime - startTime) + ' seconds'
    print 'Explored ' + str(nodesExplored) + ' nodes'


def printPath(start, path):
    print str(start) + ' ' + path[1].op + ' = ' + str(path[1].node)

    for x in range(1,len(path)):
        print str(path[x-1].node) + ' ' + path[x].op + ' = ' + str(path[x].node)



def runOp(value, operation):
    altValue = int(operation[1:])
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
        newValue = value ** altValue
        return newValue
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
        #geneticSearch(startVal, goalVal, float(timeAlloc), legalOps, 0, 2, 0, 0)
        genetic_search(startVal, goalVal, float(timeAlloc), legalOps)
    else:
        geneticSearch(5, 6, 2.5, ['+ 1', '- 2', '* 3', '/ 4', '^ 5'], 10, 1, 1, 1)
