import time
import sys
import Queue


# Read from file
if len(sys.argv) > 1:
    fileName = str(sys.argv[1])
else:
    fileName = 'test7.txt'
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

# # Iterative Deepening Search
# iterativeStart = time.time()
# # ALGORITHM GOES HERE
# iterativeEnd = time.time()
# iterativeTime = iterativeEnd - iterativeStart
# print "Iterative Deepening Search Took", iterativeTime, 'seconds'
#
# # Greedy Algorithm Search
# greedyStart = time.time()
# # ALGORITHM GOES HERE
# greedyEnd = time.time()
# greedyTime = greedyEnd - greedyStart
# print "Greedy Search Took", greedyTime, 'seconds'

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
        path = []
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


if __name__ == '__main__':
    # val = runOp(8,'/ 3')
    # print val
    if searchMode.rstrip('\n') == 'greedy':
        greedySearch(startVal, goalVal, float(timeAlloc), legalOps)

