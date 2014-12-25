# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import sys

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
  
    closedSet = set()
    dataStructure = util.Stack()
    path = []
    
    pathTuple = () 
    if "startState" in dir(problem):
        nodeCoordStartState = problem.startState
        pathTuple = ((nodeCoordStartState, "", 0), )
    elif "getStartState" in dir(problem):
        nodeCoordStartState = problem.getStartState()
        pathTuple = ((nodeCoordStartState, "", 0), )
    else:
        raise Exception("No recognizable function for getting the Start State")
        
    dataStructure.push(pathTuple)

    result = findSolution(problem, pathTuple, dataStructure, closedSet)
    
    if result is None:
        raise Exception("No solution exists!")

    path = getListOfActions(result)
    #print "[Final Path] [%s] with length %d" % (str(result), len(result))
    #print "Path: %s with length %d" % (str(path), len(path)) 
    return path

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    closedSet = set()
    dataStructure = util.Queue()
    path = []
   
    pathTuple = () 
    if "startState" in dir(problem):
        nodeCoordStartState = problem.startState
        pathTuple = ((nodeCoordStartState, "", 0), )
    elif "getStartState" in dir(problem):
        nodeCoordStartState = problem.getStartState()
        pathTuple = ((nodeCoordStartState, "", 0), )
    else:
        raise Exception("No recognizable function for getting the Start State")
        
    dataStructure.push(pathTuple)

    result = findSolution(problem, pathTuple, dataStructure, closedSet)
    
    if result is None:
        raise Exception("No solution exists!")
    
    path = getListOfActions(result)

    #print "[Final Path] [%s] with length %d" % (str(result), len(result))
    #print "Path: %s with length %d" % (str(path), len(path)) 
    return path

def getListOfActions(path):
    pathList = []
    for arc in path:
        if arc[1] is not "":
            pathList.append(arc[1])

    return pathList
     
def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    
    closedSet = set()
    dataStructure = util.PriorityQueueWithFunction(lambda (path): problem.getCostOfActions(getListOfActions(path)))
    path = []
    
    pathTuple = () 
    if "startState" in dir(problem):
        nodeCoordStartState = problem.startState
        pathTuple = ((nodeCoordStartState, "", 0), )
    elif "getStartState" in dir(problem):
        nodeCoordStartState = problem.getStartState()
        pathTuple = ((nodeCoordStartState, "", 0), )
    else:
        raise Exception("No recognizable function for getting the Start State")

    dataStructure.push(pathTuple)

    result = findSolution(problem, pathTuple, dataStructure, closedSet)
    
    if result is None:
        raise Exception("No solution exists!")
  
    path = getListOfActions(result)

    #print "[Final Path] [%s] with length %d" % (str(result), len(result))
    #print "Path: %s with length %d" % (str(path), len(path)) 
    return path 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def getFn(gN, hN):
    #print "F(n): %d G(n) %d H(n) %d" % (gN + hN, gN, hN)
    return gN + hN

def getHeuristicFunction(problem, heuristic): 
    return lambda (path): getFn(problem.getCostOfActions(getListOfActions(path)), heuristic(path[-1][0], problem))

def aStarSearch(problem, heuristic=nullHeuristic):
    closedSet = set()
    dataStructure  = util.PriorityQueueWithFunction(getHeuristicFunction(problem, heuristic))
    path  = []
   
    pathTuple = () 
    if "startState" in dir(problem):
        nodeCoordStartState = problem.startState
        pathTuple = ((nodeCoordStartState, "", 0), )
    elif "getStartState" in dir(problem):
        nodeCoordStartState = problem.getStartState()
        pathTuple = ((nodeCoordStartState, "", 0), )
    else:
        raise Exception("No recognizable function for getting the Start State")

    dataStructure.push(pathTuple)

    result = findSolution(problem, pathTuple, dataStructure, closedSet)
    
    if result is None:
        raise Exception("No solution exists!")
  
    path = getListOfActions(result)

    #print "[Final Path] [%s] with length %d" % (str(result), len(result))
    #print "Path: %s with length %d" % (str(path), len(path)) 
    return path 


def findSolution(problem=None, startNode=(((0,0), "", 0)), dataStructure=util.Stack(), closedSet=None):
    """
    A function that takes a problem and identifies if there is a solution to the pacman maze.  Returns
    a list of arcs if the solution does exist.
    """
    
    nodeLocationIndex       = 0
    nodeArcDirectionIndex   = 1
    nodeArcCostIndex        = 2
    problemStateIndex        = 3 
     
    if problem is None:
        #print "No Problem"
        return None

    if dataStructure.isEmpty():
        #print "[Backtrack] Empty Queue"
        return None   

    while not dataStructure.isEmpty():
        destPath = dataStructure.pop()
        destNode = destPath[-1]
        destNodeCord = destNode[nodeLocationIndex]
        consideredNodeDir = destNode[nodeArcDirectionIndex]
        problemState = None

        if closedSet is not None and destNodeCord in closedSet:
            #print "[Visited] (%s)" % str(destNodeCord)
            continue
     
        #print "[Expanding] (%s)" % str(destPath) 
        
        if problemState is not None and problem.isGoalState(problemState): 
            #print "[Success] Reached Goal State at (%s)" % str(destNodeCord)
            return destPath
        elif problemState is None and problem.isGoalState(destNodeCord):
            return destPath

        successors = ()
        successors = problem.getSuccessors(destNodeCord)
        
        if not successors:
            #print "[Dead-end] %s" % str(destNodeCord)
            continue

        nodesThisLevel = len(successors)
        for node in successors:
            #print "[Child] (%s), [Parent] (%s)" % (str(node), str(destNode))
            dataStructure.push(tuple(list(destPath) + [node])) 

        if closedSet is not None:
            closedSet.add(destNodeCord)

    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


