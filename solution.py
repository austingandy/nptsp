#! /usr/bin/env python
import sys, math, random
numVerts = 0
edges = []
colors = []
reds = []
blues = []

def main(argv):
	if int(argv) == 0:
		solve()
	else:
		fix()

def solve():
	global numVerts, edges, colors, reds, blues
	answerList = []
	for i in range(1, 496):
		print "working on file number " + str(i)
		fileName = "instances/" + str(i) + ".in"
		info = open(fileName, "r")
		settup(info)
		answers = open("initial_answers.out", "w")
		answer = ""
		chosenPath = runIterations()
		if not checkPath(chosenPath):
			print i
		chosenPath = [v+1 for v in chosenPath]
		for num in chosenPath:
			answer = answer + str(num) + " "
		answer += "\n"
		answerList.append(answer)
		info.close()
	answers.writelines(answerList)
	answers.close()

""" Reads input files and convers files into parsible formats. """
def settup(info):
	global reds, blues, colors, edges, numVerts
	first_line = info.readline().split()
	numVerts = int(first_line[0])
	edges = [[0 for j in range(numVerts)] for i in range(numVerts)]
	for i in range(numVerts):
		line = info.readline().split()
		for j in range(numVerts):
			edges[i][j] = int(line[j])
	colors = info.readline()
	reds = [vert for vert in range(numVerts) if colors[vert] == "R"]
	blues = [vert for vert in range(numVerts) if colors[vert] == "B"]

""" Runs all algorithms using various start points and inputs to find the
	best of the set of solutions generated. """
def runIterations():
	path = findBestPath()
	pathCost = cost(path)
	betterPathCost = pathCost + 1
	count = 0
	simCount = 10000;
	while betterPathCost > pathCost and count < 20:
		betterPath = simAnneal(path, simCount)
		betterPathCost = cost(betterPath)
		count += 1
	randomPath = findRandomPath()
	randPath = simAnneal(randomPath, simCount)
	randPath2 = findRandomPath()
	randPath3 = findRandomPath()
	randPath2 = simAnneal(randPath2, simCount)
	randPath3 = simAnneal(randPath3, simCount)
	randCost = cost(randPath)
	randCost2 = cost(randPath2)
	randCost3 = cost(randPath3)
	if randCost <= betterPathCost and randCost <= pathCost and randCost <= randCost2 and randCost <= randCost3:
		return randPath
	elif betterPathCost <= pathCost and betterPathCost <= randCost2 and betterPathCost <= randCost3:
		return betterPath
	elif pathCost <= randCost2 and pathCost <= randCost3:
		return path
	elif randCost2 <= randCost3:
		return randPath2
	else:
		return randPath3

""" Returns a randomly chosen path. """
def findRandomPath():
    vertsLeft = range(numVerts)
    redsLeft = reds[:]
    bluesLeft = blues[:]
    path = []
    prev_reds = 0
    prev_blues = 0
    while vertsLeft:
        vert = random.choice(vertsLeft)
        if colors[vert] == "R":
            if prev_reds == 3 or 3 * len(redsLeft) <= len(bluesLeft) + 1:
                continue
            else:
                prev_reds += 1
                path.append(vert)
                prev_blues = 0
                redsLeft.remove(vert)
        else:
            if prev_blues == 3 or 3 * len(bluesLeft) <= len(redsLeft) + 1:
                continue
            else:
                prev_blues += 1
                path.append(vert)
                prev_reds = 0
                bluesLeft.remove(vert)
        vertsLeft.remove(vert)
    return path

""" Iteratively finds the best vertex to start from using the
	greedy algorithm to find a solution. """
def findBestPath():
	bestPathCost = 101 * numVerts
	bestPath = []
	for i in range(numVerts):
		path = greedy_solution(i)
		currPathCost = cost(path)
		if currPathCost < bestPathCost:
			bestPath = path
			bestPathCost = currPathCost
	return bestPath

""" A neighbor of a path is defined as a path for which only 2 verticies
	are switched in order from the initial path. """
def findNeighbor(path):
	i = random.choice(path)
	j = random.choice(path)
	if i == j or colors[j] != colors[i]:
		return findNeighbor(path)
	neighbor = path[:]
	swap(neighbor, i, j)
	if not checkPath(neighbor):
		return findNeighbor(path)
	return neighbor

def swap(lst, i, j):
	temp = lst[i]
	lst[i] = lst[j]
	lst[j] = temp

""" Returns the probability with which we should choose a suboptimal
	path when running TSP. """
def acceptanceProb(e, ePrime, temp):
	if ePrime < e:
		return 1
	return math.exp(-1.0 * float(ePrime - e) / float(temp))

""" Runs the simmulated annealing algorithm kMax starting with
	the solution start. """
def simAnneal(start, kMax):
	curr = start[:]
	currCost = cost(start)
	for k in range(kMax):
		t = temp(float(k), float(kMax))
		new = findNeighbor(curr)
		newCost = cost(new)
		if acceptanceProb(currCost, newCost, t) >= random.random():
			curr = new
			currCost = newCost
	return curr

""" Ensures that path is a valid path. """
def checkPath(path):
	numColor = 0
	currColor = ""
	for vert in path:
		if numColor > 3:
			return False
		if currColor == colors[vert]:
			numColor += 1
		else:
			currColor = colors[vert]
			numColor = 1
	return True

""" Returns the temperature of iteration k when running kMax total
	iterations of simulated annealing. """
def temp(k, kMax):
	return math.log(kMax - k + 1)

""" Given a PATH, returns the cost of that PATH according to EDGES. """
def cost(path):
	pathCost = 0
	for i in range(1,numVerts):
		pathCost += edges[path[i-1]][path[i]]
	return pathCost

""" Returns path starting at STARTVERT chosing the closest
	unvisited node on every call to the helper. """
def greedy_solution(startVert):
    visited = [startVert]
    currColor = colors[startVert]
    numColor = 1
    totalCost = 0
    redsLeft = numVerts / 2 if currColor == "B" else (numVerts / 2) - 1
    bluesLeft = numVerts / 2 if currColor == "R" else (numVerts / 2) - 1
    currVert = startVert
    while len(visited) < numVerts:
        if 3*redsLeft <= bluesLeft+1 or (currColor == "R" and numColor >= 3):
            currVert, cost, nextColor = findBest(currVert, visited, blues)
        elif 3*bluesLeft <= redsLeft+1 or (currColor == "B" and numColor >= 3):
            currVert, cost, nextColor = findBest(currVert, visited, reds)
        elif numColor < 3:
            currVert, cost, nextColor = findBest(currVert, visited, range(numVerts))
        else:
            print "something is going wrong I think"
        totalCost += cost
        if nextColor == "R":
            redsLeft -= 1
        elif nextColor == "B":
            bluesLeft -= 1
        if nextColor == currColor:
            numColor += 1
        else:
            currColor = nextColor
            numColor = 1
    	visited.append(currVert)
    return visited

def findBest(currVert, visited, nextPossible):
	bestCost = 101
	next = -1
	toVisit = [v for v in nextPossible if v not in visited]
	for i in toVisit:
		cost = edges[currVert][i]
		if cost < bestCost:
			bestCost = cost
			next = i
	# might be better to keep currColor and colorCount global
	# I hate that I'm returning 3 things here this is just stupid
	if next == -1:
		print "currVert is " + str(currVert)
		print "visited is " + str(visited)
		print "nextPossible is " + str(nextPossible)
		print "toVisit is " + str(toVisit)
	return next, bestCost, colors[next]

def fix():
	""" Corrects any mistakes the algorithm made previously """
	scores = open("score.txt", 'r')
	paths = open("answer.out", 'r')
	newAnswers = open("new_answers.out", 'w')
	answerList = []
	for i in range(495):
		score = int(scores.readline())
		line = paths.readline()
		if score == -1:
			info = open("instances/" + str(i+1) + ".in", "r")
			print "working on file number " + str(i)
			settup(info)
			bestPath = [v+1 for v in runIterations()]
			answer = ""
			for num in bestPath:
				answer = answer + str(num) + " "
			answer += "\n"
			answerList.append(answer)
			info.close()
		else:
			answerList.append(line)
	scores.close()
	paths.close()
	newAnswers.writelines(answerList)
	newAnswers.close()

if __name__ == '__main__':
	main(sys.argv[1])