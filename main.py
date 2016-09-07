import time
import sys

# Read from file
if len(sys.argv) > 1:
    fileName = str(sys.argv[1])
else:
    fileName = "test.txt"
print "Opening ", fileName
config = open("test.txt", "r", 0)
info = config.readlines()
config.close()

# Assign file contents to appropriate variables
searchMode = info[0]
startVal = info[1]
goalVal = info[2]
timeAlloc = info[3]
legalOps = info[4:-1]
print "Search Mode: ", searchMode
print "Starting Value: ", startVal
print "Goal Value: ", goalVal
print "Time Allocated: ", timeAlloc, 'seconds'
print "Legal Operations: ", legalOps

# Variables for output of results
isError = False
numStepsRequired = 0
nodesExpanded = 0
maxSearchDepth = 0

# Iterative Deepening Search
iterativeStart = time.time()
# ALGORITHM GOES HERE
iterativeEnd = time.time()
iterativeTime = iterativeEnd - iterativeStart
print "Iterative Deepening Search Took", iterativeTime, 'seconds'

# Greedy Algorithm Search
greedyStart = time.time()
# ALGORITHM GOES HERE
greedyEnd = time.time()
greedyTime = greedyEnd - greedyStart
print "Greedy Search Took", greedyTime, 'seconds'


