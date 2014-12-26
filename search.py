# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    closed = set()
    fringe = util.Stack()
    fringe.push(makeNode(problem.getStartState()))

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:
            closed.add(node.getState())
            insertAll(fringe, expand(node, problem))


def makeNode(state):
    return Node(state)

def expand(node, problem):
    parentNode = node
    childList = []
    #print node.getActions()
    successors = problem.getSuccessors(node.getState())
    #print successors
    for i in range(len(successors)):
        successor = successors[i]
        child = makeNode(successor[0])
        child.setActionList(parentNode.getActions())
        child.addAction(successor[1])
        child.setCumulativeCost(parentNode.getCumulativeCost() + successor[2])
        childList.append(child)

    return childList

def insertAll(stack, nodeList):
    for node in nodeList:
        stack.push(node)

def insertAllInPriorityQueue(queue, nodeList):
    for node in nodeList:
        queue.push(node, node.getDepth())

def insertAllWithCost(queue, nodeList):
    for node in nodeList:
        queue.push(node, node.getCumulativeCost())

def insertAllWithCostAndHeuristic(queue, nodeList, heuristic, problem):
    for node in nodeList:
        queue.push(node, node.getCumulativeCost() + heuristic(node.getState(), problem))

class Node:
    
    def __init__(self, state):
        self.actionList = []
        self.state = state
        self.cumulativeCost = 0

    def getState(self):
        return self.state

    def getActions(self):
        return self.actionList
  
    def setActionList(self, actions):
        self.actionList = actions[:]

    def addAction(self, action):
        self.actionList.append(action)

    def getDepth(self):
        return len(self.actionList)

    def getCumulativeCost(self):
        return self.cumulativeCost

    def setCumulativeCost(self, cost):
        self.cumulativeCost = cost

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    closed = set()
    fringe = util.PriorityQueue()
    node = makeNode(problem.getStartState())
    fringe.push(node, node.getDepth())

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:
            closed.add(node.getState())
            insertAllInPriorityQueue(fringe, expand(node, problem))

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    closed = set()
    fringe = util.PriorityQueue()
    node = makeNode(problem.getStartState())
    node.setCumulativeCost(0)
    fringe.push(node, node.getCumulativeCost())

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:
            closed.add(node.getState())
            insertAllWithCost(fringe, expand(node, problem))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    closed = set()
    fringe = util.PriorityQueue()
    node = makeNode(problem.getStartState())
    node.setCumulativeCost(0)
    fringe.push(node, node.getCumulativeCost() + heuristic(node.getState(), problem))

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()
        
        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:
            closed.add(node.getState())
            insertAllWithCostAndHeuristic(fringe, expand(node, problem), heuristic, problem)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
