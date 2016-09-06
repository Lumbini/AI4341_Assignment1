from Queue import PriorityQueue
import time

class NodeOp:
	def __init__(self,node,completedOperation,parentNodeOp):
		self.node = node
		self.op = completedOperation
		self.parent = parentNodeOp


#Greedy Search Algorithm
#start is starting number
#goal is the goal number
#maxtime is the maximum time allowed for the search
#operations are the operations given to the search to use
#	operations contains strings of each operation
def greedySearch(start,goal,maxTime,operations):
	done = 0

	#begin timer for search
	startTime = time.time()

	#add initial node to frontier
	frontier = PriorityQueue()
	if start == goal:
		return

	else:
		#add children to frontier
		for next in operations:
			newValue = runOp(start,next)
			priority = abs(newValue - goal)
			print 'Priority = ' + str(priority)
			newNodeOp = NodeOp(newValue,next,start) #first parent is integer
			frontier.put(newNodeOp,priority)

		currentTime = time.time()

		current = start
		nodesExplored = 1
		while (currentTime - startTime) < maxTime:
			current = frontier.get()
			print 'Node = ' + str(current.node) + ' Past operator was ' + str(current.op)
			nodesExplored += 1

			#check if current is goal
			if current.node == goal:
				currentTime = time.time()
				break

			#add children to frontier
			for next in operations:
				newValue = runOp(current.node,next)
				priority = abs(newValue - goal)
				print 'Priority = ' + str(priority)
				newNodeOp = NodeOp(newValue,next,current) #all other parents are NodeOps
				frontier.put(newNodeOp,priority)

			currentTime = time.time()

		#add parent nodes to path 
		path = []
		while True:
			path.append(current)
			if current.parent is NodeOp: #type check. Not sure if this works
				current = current.parent
			else:
				break

		path.reverse()

		#final printing
		print currentTime - startTime
		print 'Explored ' + str(nodesExplored) + ' nodes'



def runOp(value,operation):
	altValue = int(operation[2:])
	op = operation[:1]

	if op == '+':
		newValue = float(value) + float(altValue)
		return newValue
	elif op == '-':
		newValue = float(value) - float(altValue)
		return newValue
	elif op == '/':
		newValue = float(value) / float(altValue)
		return newValue
	elif op == '*':
		newValue = float(value) * float(altValue)
		return newValue
	elif op == '^':
		newValue = float(value) ** float(altValue)
		return newValue
	else: #will cause error if invalid operation
		return


if __name__ == '__main__':
	# val = runOp(10,'/ 15')
	# print val
	greedySearch(1,3,5,['+ 1','* 2'])
