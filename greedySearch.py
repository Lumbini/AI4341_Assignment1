import Queue
import time

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
    if start == goal:
        return

    else:
        # add children to frontier
        for next in operations:
            newValue = runOp(start, next)
            priority = abs(newValue - goal)
            newNodeOp = NodeOp(newValue, next, start)  # first parent is integer
            frontier.put((priority,newNodeOp))

        currentTime = time.time()

        current = start
        nodesExplored = 1

        while (currentTime - startTime) < maxTime:
            current = frontier.get(

            )[1]
            # print 'Node = ' + str(current.node) + ' Past operator was ' + str(current.op)
            nodesExplored += 1

            # check if current is goal
            if current.node == goal:
                currentTime = time.time()
                break

            # add children to frontier
            for next in operations:
                newValue = runOp(current.node, next)
                priority = abs(newValue - goal)
                newNodeOp = NodeOp(newValue, next, current)  # all other parents are NodeOps
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

        # final printing
        print 'Search took ' + str(currentTime - startTime) + ' seconds'
        print 'Explored ' + str(nodesExplored) + ' nodes'


def printPath(start, path):
    print str(start) + ' ' + path[1].op + ' = ' + str(path[1].node)

    for x in range(2,len(path)):
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
    greedySearch(5, -8, 1, ['^ 2','/ 5','+ 2','- 10','* 9'])
