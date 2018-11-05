#!/usr/bin/python

#
# Alan Neads (neadsa)
#

import sys
import os
import collections
import heapq

moveActions = [
        ( 1, 0 ), # One chicken
        ( 2, 0 ), # Two chickens
        ( 0, 1 ), # One wolf
        ( 1, 1 ), # One chicken, one wolf
        ( 0, 2 )  # Two wolves
]

nodesTotal = 0
nodesExpanded = 0

printSolutionPath = True

class Node:
        def __init__( self, inputState, action, depth, cost, parent ):
                global nodesTotal
                nodesTotal += 1
                self.state = inputState
                self.action = action
                self.depth = depth
                self.cost = cost
                self.parent = parent
        
        def getSuccessors( self ):
                global moveActions

                output = []
                for action in moveActions:
                        newState = performMove( action, self.state )

                        if ( newState != False ):
                                # Cost hueristic is previous cost plus the amount of chickens and wolves
                                newCost = self.cost

                                # Check which side the boat is on
                                if ( newState[2] == 1 ):
                                        newCost += newState[0] + newState[1]
                                elif ( newState[5] == 1 ):
                                        newCost += newState[3] + newState[4]

                                newCost -= 1
                                # New successor action
                                output.append(Node(newState, action, self.depth + 1, newCost, self))

                return output

class SolutionFound( Exception ):
        pass

def writeSolutionPath( outFile, node, startState ):
        if ( outFile == None or node == None or startState == None ):
                return False

        output = []
        currentNode = node
        while( currentNode.parent != None ):
                output.append(currentNode)
                currentNode = currentNode.parent
        
        try:
                fp = open(outFile, 'w')
        except IOError as e:
                if ( e.rrno == errno.EACCES ):
                        return False
                raise
        else:
                global printSolutionPath
                if ( printSolutionPath ):
                    sys.stdout.write('Solution path: \n')

                fp.write(stateToString(startState) + '\n')

                if ( printSolutionPath ):
                    sys.stdout.write(stateToString(startState) + '\n')

                for curNode in reversed(output):
                        fp.write(stateToString(curNode.state) + '\n')
                        
                        if ( printSolutionPath ):
                            sys.stdout.write(stateToString(curNode.state) + '\n')

def stateToString( inputState ):
    return "{0} {1} {2}, {3} {4} {5}".format(
        inputState[0],
        inputState[1],
        inputState[2],
        inputState[3],
        inputState[4],
        inputState[5]
    )

def readFileState( inFile = None ):
        if ( inFile == None ):
                return False
        try:
                fp = open(inFile, 'r')
        except IOError as e:
                if ( e.errno == errno.EACCES ):
                        return False
                raise
        else:
                lines = fp.readline()
                lines += fp.readline()
                fp.close()
                lines = lines.replace('\n', ',')
                lines = lines.split(',')
                lines = filter(None, lines)
                lines = [int(n) for n in lines]
                return lines

def swapValues( array, pos1, pos2 ):
        temp = array[pos1]
        array[pos1] = array[pos2]
        array[pos2] = temp
        return array

def performMove( action, inputState ):
        newState = inputState.copy()
        flip = 1

        # If the boat is on the left side we just
        # flip our math around with a -1 multiply
        if ( newState[2] == 1 and newState[5] == 0 ):
                flip = -1

        newState[0] += action[0] * flip
        newState[1] += action[1] * flip
        newState[3] -= action[0] * flip
        newState[4] -= action[1] * flip

        # Move the boat from one side to the other
        newState = swapValues(newState, 2, 5)

        # Check if enough chickens and wolves on both banks
        if ( newState[0] < 0 ):
                return False
        elif ( newState[1] < 0 ):
                return False
        elif ( newState[3] < 0 ):
                return False
        elif ( newState[4] < 0 ):
                return False

        # Check if we have 50%+ ratio of chickens to wolves
        if ( newState[0] < newState[1] and newState[0] != 0 ):
                return False
        elif ( newState[3] < newState[4] and newState[3] != 0 ):
                return False

        return newState

def bfs( inputState, goalState ):
        global nodesTotal
        global nodesExpanded
        print("Using BFS on", stateToString(inputState), "to reach goal state", stateToString(goalState))

        firstNode = Node(inputState, None, 0, 0, None )

        fringe = collections.deque()
        fringe.append(firstNode)
        solution = None
        explored = []

        while True:
                if len(fringe) == 0:
                        solution = None
                        break
                front = fringe.popleft()
                if ( front.state == goalState ):
                        solution = front
                        break
                if ( front.state not in explored ):
                        explored.append(front.state)
                        nodesExpanded += 1
                        for node in front.getSuccessors():
                                fringe.append(node)

        if ( solution == None ):
                print("nodes expanded:", nodesExpanded)
                print("No solution found")
                return

        print("nodes total:", nodesTotal)
        print("nodes expanded:", nodesExpanded)
        print("nodes in solution:", solution.depth)
        return solution

def dfs( inputState, goalState ):
        global nodesTotal
        global nodesExpanded
        print("Using DFS on", stateToString(inputState), "to reach goal state", stateToString(goalState))

        firstNode = Node(inputState, None, 0, 0, None )

        fringe = collections.deque()
        fringe.append(firstNode)
        solution = None
        explored = []

        while True:
                if len(fringe) == 0:
                        solution = None
                        break
                front = fringe.pop()
                if ( front.state == goalState ):
                        solution = front
                        break
                if ( front.state not in explored ):
                        explored.append(front.state)
                        nodesExpanded += 1
                        for node in front.getSuccessors():
                                fringe.append(node)

        if ( solution == None ):
                print("nodes expanded:", nodesExpanded)
                print("No solution found")
                return

        print("nodes total:", nodesTotal)
        print("nodes expanded:", nodesExpanded)
        print("nodes in solution:", solution.depth)
        return solution

def iddfs( inputState, goalState ):
        global nodesTotal
        global nodesExpanded
        print("Using IDDFS on", stateToString(inputState), "to reach goal state", stateToString(goalState))

        firstNode = Node(inputState, None, 0, 0, None )

        fringe = collections.deque()
        fringe.append(firstNode)
        solution = None
        explored = {}

        depthLimit = 0

        while True:
                if len(fringe) == 0:
                        if ( depthLimit > 2000 ):
                                solution = None
                                break
                        depthLimit += 1
                        fringe = collections.deque()
                        fringe.append(firstNode)
                        solution = None
                        explored = {}
                        nodesTotal = 1
                        continue
                front = fringe.popleft()
                if ( front.state == goalState ):
                        solution = front
                        break
                if ( tuple(front.state) not in explored ):
                        if ( front.depth + 1 <= depthLimit ):
                                explored[tuple(front.state)] = 1
                                nodesExpanded += 1
                                for node in front.getSuccessors():
                                        fringe.append(node)
        
        if ( solution == None ):
                print("nodes expanded:", nodesExpanded)
                print("No solution found")
                return

        print("nodes total:", nodesTotal)
        print("nodes expanded:", nodesExpanded)
        print("nodes in solution:", solution.depth)
        return solution

class PriorityQueue:
        def __init__( self ):
                self._queue = []
                self._index = 0

        def push( self, value, priority ):
                heapq.heappush( self._queue, (priority, self._index, value) )
                self._index = self._index + 1

        def pop( self ):
                return heapq.heappop( self._queue )[-1]

        def __len__( self ):
                return len( self._queue )

def astar( inputState, goalState ):
        global nodesTotal
        global nodesExpanded
        print("Using A* on", stateToString(inputState), "to reach goal state", stateToString(goalState))

        firstNode = Node(inputState, None, 0, 0, None )

        fringe = PriorityQueue()
        fringe.push(firstNode, firstNode.cost)
        solution = None
        explored = {}

        depthLimit = 1

        while True:
                if len(fringe) == 0:
                        solution = None
                        break
                front = fringe.pop()
                if ( front.state == goalState ):
                        solution = front
                        break
                if ( tuple(front.state) not in explored ):
                        explored[tuple(front.state)] = 1
                        nodesExpanded += 1
                        for node in front.getSuccessors():
                                fringe.push(node, node.cost)

        if ( solution == None ):
                print("nodes expanded:", nodesExpanded)
                print("No solution found")
                return

        print("nodes total:", nodesTotal)
        print("nodes expanded:", nodesExpanded)
        print("nodes in solution:", solution.depth)
        return solution

if ( __name__ == "__main__" ):
        if ( len(sys.argv) != 5 and len(sys.argv) != 6 ):
                sys.exit("Arguments: <initial state file> <goal state file> <mode> <output file>")

        if ( len(sys.argv) == 6 ):
                if ( sys.argv[5] == "--dont-print-solution-path" ):
                        printSolutionPath = False
                else:
                        sys.exit("Arguments: <initial state file> <goal state file> <mode> <output file>")

        inputFile = sys.argv[1]
        goalStateFile = sys.argv[2]
        mode = sys.argv[3].lower()
        outputFile = sys.argv[4]

        if ( os.path.exists(inputFile) == False or os.path.isfile(inputFile) == False ):
                sys.exit("Input file does not exist")

        if ( os.path.exists(goalStateFile) == False or os.path.isfile(goalStateFile) == False ):
                sys.exit("Goal state file does not exist")

        if ( mode != "bfs" and mode != "dfs" and mode != "iddfs" and mode != "astar" ):
                sys.exit("Invalid mode. Modes available are: bfs, dfs, iddfs, astar")

        inputState = readFileState( inputFile )
        goalState = readFileState( goalStateFile )

        if ( inputState == False ):
                sys.exit("Could not read from input file")

        if ( goalState == False ):
                sys.exit("Could not read from goal state file")

        output = None

        if ( mode == "bfs" ):
                output = bfs(inputState, goalState)
        elif ( mode == "dfs" ):
                output = dfs(inputState, goalState)
        elif ( mode == "iddfs" ):
                output = iddfs(inputState, goalState)
        elif ( mode == "astar" ):
                output = astar(inputState, goalState)

        writeSolutionPath( outputFile, output, inputState )
