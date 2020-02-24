# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search stat    e

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    newStack = util.Stack()
    visitedStates = []
    initialState = problem.getStartState()
    currentState = [initialState,"Start",0] #Making it as same as successor states to get successors
    newStack.push(currentState)
    movementStack = util.Stack()
    moveList = []
    movementStack.push(moveList)

    while not newStack.isEmpty():
        currentState = newStack.pop()
        #print("Visited States",visitedStates)
        moveList = movementStack.pop()

        if currentState[0] not in visitedStates:
            if problem.isGoalState(currentState[0]):
                print(moveList)
                return moveList
            visitedStates.append(currentState[0])
            for nextState in problem.getSuccessors(currentState[0]):
                newMoves = moveList + [nextState[1]]
                movementStack.push(newMoves)
                newStack.push(nextState)



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    newQueue = util.Queue()
    visitedStates = []
    initialState = problem.getStartState()
    currentState = [initialState, "Start", 0]  # Making it as same as successor states to get successors
    newQueue.push(currentState)
    movementQueue = util.Queue()
    moveList = []
    movementQueue.push(moveList)

    while not newQueue.isEmpty():
        currentState = newQueue.pop()
        # print("Visited States",visitedStates)
        moveList = movementQueue.pop()

        if currentState[0] not in visitedStates:
            if problem.isGoalState(currentState[0]):
                print(moveList)
                return moveList
            visitedStates.append(currentState[0])
            for nextState in problem.getSuccessors(currentState[0]):
                newMoves = moveList + [nextState[1]]
                movementQueue.push(newMoves)
                newQueue.push(nextState)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    newPriority = util.PriorityQueue()
    visitedStates = []
    initialState = problem.getStartState()
    currentState = [initialState, "Start", "0"]  # Making it as same as successor states to get successors
    newPriority.push(currentState,0)
    movementPriority = util.PriorityQueue()
    moveList = []
    movementPriority.push(moveList,0)
    moveCost = 0
    moveCostPriority = util.PriorityQueue()
    moveCostPriority.push(moveCost,moveCost)

    while not newPriority.isEmpty():
        currentState = newPriority.pop()
        # print("Visited States",visitedStates)
        moveList = movementPriority.pop()
        moveCost = moveCostPriority.pop()

        if currentState[0] not in visitedStates:
            if problem.isGoalState(currentState[0]):
                return moveList
            visitedStates.append(currentState[0])
            for nextState in problem.getSuccessors(currentState[0]):
                newMoves = moveList + [nextState[1]]
                moveCosts = moveCost + nextState[2]
                movementPriority.push(newMoves,moveCosts)
                newPriority.push(nextState,moveCosts)
                moveCostPriority.push(moveCosts,moveCosts)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    newPriority = util.PriorityQueue()
    visitedStates = []
    initialState = problem.getStartState()
    currentState = [initialState, "Start", 0]  # Making it as same as successor states to get successors
    newPriority.push(currentState, 0)
    movementPriority = util.PriorityQueue()
    moveList = []
    movementPriority.push(moveList, 0)
    moveCost = 0
    moveCostPriority = util.PriorityQueue()
    moveCostPriority.push(moveCost, moveCost)

    while not newPriority.isEmpty():
        currentState = newPriority.pop()
        # print("Visited States",visitedStates)
        moveList = movementPriority.pop()
        moveCost = moveCostPriority.pop()

        if currentState[0] not in visitedStates:
            if problem.isGoalState(currentState[0]):
                return moveList
            visitedStates.append(currentState[0])
            for nextState in problem.getSuccessors(currentState[0]):
                newMoves = moveList + [nextState[1]]
                moveCosts = moveCost + nextState[2]
                heuristicCost = moveCosts + heuristic(nextState[0],problem)
                movementPriority.push(newMoves, heuristicCost)
                newPriority.push(nextState, heuristicCost)
                moveCostPriority.push(moveCosts, heuristicCost)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
