# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        currentFood = currentGameState.getFood()
        currentFoodList = currentFood.asList()
        closestFoodList = []
        x, y = newPos

        for ghost in newGhostStates:
            if (x,y) == ghost.getPosition() and ghost.scaredTimer is 0:
                return -999999

        #print(ghostLocations)
        if action == "Stop":
            return -999999


        for food in currentFoodList:
            #Gives a Higher Score Avg. than Manhattan on autograder in my trials
            euclidDist = -1 * ((x-food[0])**2+(y-food[1])**2)**(1/2)

            #dist = -1*util.manhattanDistance((x,y),food)
            #closestFoodList.append(dist)

            closestFoodList.append(euclidDist)

        return max(closestFoodList)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        pacmanLegalActions = gameState.getLegalActions(pacmanIndex)
        maxPacmanValue = -float("inf")
        rootDepth = 0
        stateList= []
        firstGhost = 1


        for action in pacmanLegalActions:
            stateList.append(gameState.generateSuccessor(pacmanIndex,action))

        #print(stateList)

        #print(actionList)
        #arbitraryState
        nextState = stateList[0]
        for state in stateList:
            val = self.value(state,firstGhost,rootDepth)
            #Returning argmax
            if val > maxPacmanValue:
                maxPacmanValue = val
                nextState = state
                #print(state)
                #print(nextState)

        nextAction = ""
        for state in range(len(stateList)):
            if stateList[state] == nextState:
                nextAction = pacmanLegalActions[state]

        return nextAction

    def value(self,gameState,agent,depth):

        if depth == self.depth:
            return self.evaluationFunction(gameState)
        #print(gameState)

        #print(gameState.isWin())
        #util.pause()

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agent == 0:
            return self.maxAgent(gameState,agent,depth)
        else:
            #print("goes min")
            return self.minAgent(gameState,agent,depth)


    def maxAgent(self,gameState,agent,depth):
        legalActions = gameState.getLegalActions(agent)
        val = -float("inf")
        stateList = []
        for action in legalActions:
            stateList.append(gameState.generateSuccessor(agent, action))

        if not legalActions:
            return self.evaluationFunction(gameState)

        for state in stateList:
            val = max(val, self.value(state,1,depth))
            #print("Max agent:",val)


        #print("Max Agent Value: ",val)
        return val


    def minAgent(self,gameState,agent,depth):
        legalActions = gameState.getLegalActions(agent)
        ghostCount = gameState.getNumAgents()
        val = float("inf")
        stateList = []
        for action in legalActions:
            stateList.append(gameState.generateSuccessor(agent, action))

        if not legalActions:
            return self.evaluationFunction(gameState)
        #print("passes here")

        for state in stateList:
                if agent+1 == ghostCount:
                    val = min(val,self.value(state,0,depth+1))
                else:
            #Next ghost
                    #print("enters here")

                    val = min(val,self.value(state,agent+1,depth))

        #print("Min Agent Value: ",val)

        return val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        pacmanLegalActions = gameState.getLegalActions(pacmanIndex)
        maxPacmanValue = -float("inf")
        rootDepth = 0
        stateList = []
        firstGhost = 1
        alpha = -float("inf")
        beta = float("inf")

        for action in pacmanLegalActions:
            stateList.append(gameState.generateSuccessor(pacmanIndex, action))

        # print(stateList)

        # print(actionList)
        # arbitraryState
        nextState = stateList[0]
        for state in stateList:
            val = self.value(state, firstGhost, rootDepth,alpha,beta)
            # Returning argmax
            if val > maxPacmanValue:
                maxPacmanValue = val
                nextState = state
                alpha = val
                # print(state)
                # print(nextState)

        nextAction = ""
        for state in range(len(stateList)):
            if stateList[state] == nextState:
                nextAction = pacmanLegalActions[state]

        return nextAction

    def value(self,gameState,agent,depth,alpha,beta):

        if depth == self.depth:
            return self.evaluationFunction(gameState)
        #print(gameState)

        #print(gameState.isWin())
        #util.pause()

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agent == 0:
            return self.maxAgent(gameState,agent,depth,alpha,beta)
        else:
            #print("goes min")
            return self.minAgent(gameState,agent,depth,alpha,beta)



    def maxAgent(self,gameState,agent,depth,alpha,beta):
        legalActions = gameState.getLegalActions(agent)
        val = -float("inf")
        if not legalActions:
            return self.evaluationFunction(gameState)

        for action in legalActions:
           currentState = gameState.generateSuccessor(agent, action)
           val = max(val, self.value(currentState,1,depth,alpha,beta))
           if val > beta:
               return val
           alpha = max(alpha,val)

            #print("Max agent:",val)
        #print("Max Agent Value: ",val)
        return val


    def minAgent(self,gameState,agent,depth,alpha,beta):
        legalActions = gameState.getLegalActions(agent)
        ghostCount = gameState.getNumAgents()
        val = float("inf")
        if not legalActions:
            return self.evaluationFunction(gameState)

        for action in legalActions:
            currentState = gameState.generateSuccessor(agent, action)
            if agent+1 == ghostCount:
                val = min(val,self.value(currentState,0,depth+1,alpha,beta))
            else:
            #Next ghost
                #print("enters here")
                val = min(val, self.value(currentState, agent + 1, depth,alpha,beta))
            if val < alpha:
                return val
            beta = min(beta, val)
        #print("Min Agent Value: ",val)
        return val


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        pacmanLegalActions = gameState.getLegalActions(pacmanIndex)
        maxPacmanValue = -float("inf")
        rootDepth = 0
        stateList = []
        firstGhost = 1

        for action in pacmanLegalActions:
            stateList.append(gameState.generateSuccessor(pacmanIndex, action))

        # print(stateList)

        # print(actionList)
        # arbitraryState
        nextState = stateList[0]
        for state in stateList:
            val = self.value(state, firstGhost, rootDepth)
            # Returning argmax
            if val > maxPacmanValue:
                maxPacmanValue = val
                nextState = state
                # print(state)
                # print(nextState)

        nextAction = ""
        for state in range(len(stateList)):
            if stateList[state] == nextState:
                nextAction = pacmanLegalActions[state]

        return nextAction

    def value(self, gameState, agent, depth):

        if depth == self.depth:
            return self.evaluationFunction(gameState)
        # print(gameState)

        # print(gameState.isWin())
        # util.pause()

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agent == 0:
            return self.maxAgent(gameState, agent, depth)
        else:
            # print("goes min")
            return self.expValue(gameState, agent, depth)

    def expValue(self,gameState,agent,depth):
        val = 0
        legalActions = gameState.getLegalActions(agent)
        stateList = []

        if not legalActions:
            return self.evaluationFunction(gameState)

        for action in legalActions:
            stateList.append(gameState.generateSuccessor(agent, action))

        length = len(stateList)
        ghostCount = gameState.getNumAgents()

        for state in stateList:
            if agent + 1 == ghostCount:
                val += self.value(state, 0, depth + 1)
            else:
                # Next ghost
                # print("enters here")
                val += self.value(state, agent + 1, depth)

        probVal = val / length
        return probVal


    def maxAgent(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        val = -float("inf")
        stateList = []
        for action in legalActions:
            stateList.append(gameState.generateSuccessor(agent, action))

        if not legalActions:
            return self.evaluationFunction(gameState)

        for state in stateList:
            val = max(val, self.value(state, 1, depth))
            # print("Max agent:",val)

        # print("Max Agent Value: ",val)
        return val



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    Initially I get the locations of ghosts so that Pacman will stay away from them unless it has eaten any capsules
    Therefore I also consider the capsules in the world. Instead of Euclidiean Distance I have taken Manhattan Distance because
    taking Manhattan Distance to the Ghosts is More accurate as along the way there is no gain for the Pacman unlike the Foods.
    For the same logic as getting the foods I have gathered the capsules within a list and get the closest one in a list.
    I have summed up these individual scores to gather up a total evaluation score of the currentState and I have averaged
    1064.2 score.
    """
    "*** YOUR CODE HERE ***"
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsuleList = currentGameState.getCapsules()

    x ,y = currentGameState.getPacmanPosition()

    currentFood = currentGameState.getFood()
    currentFoodList = currentFood.asList()

    closestGhost = []
    eatableGhost = []
    scaredGhost = 0
    for ghost in newGhostStates:
        ghostPos = ghost.getPosition()

        if ghost.scaredTimer is not 0:
            ghostDist = -1 * util.manhattanDistance((x,y),ghostPos)
            closestGhost.append(ghostDist)
        else:
            ghostDist = -1 * util.manhattanDistance((x, y), ghostPos)
            eatableGhost.append(ghostDist)
            scaredGhost += 1

    closestFood = []
    for food in currentFoodList:
        foodDist = -1 * ((x - food[0]) ** 2 + (y - food[1]) ** 2) ** (1 / 2)
        closestFood.append(foodDist)

    closestCapsule = []
    for capsule in capsuleList:
        capsuleDist = -1 * ((x - capsule[0]) ** 2 + (y - capsule[1]) ** 2) ** (1 / 2)
        closestCapsule.append(capsuleDist)

    score = currentGameState.getScore()
    foodScore = 0
    eatableGhostScore = 0
    capsuleScore = 0
    scaryGhostScore = 0

    if not closestFood:
        foodScore = 0
    else:
        foodScore = max(closestFood)

    if scaredGhost != 0:
        eatableGhostScore = max(eatableGhost)

    if not closestGhost:
        scaryGhostScore = 0
    else:
        scaryGhostScore = min(closestGhost)

    if not capsuleList:
        capsuleScore = 0
    else:
        capsuleScore = max(closestCapsule)

    score += foodScore + eatableGhostScore + scaryGhostScore + capsuleScore

    return score
# Abbreviation
better = betterEvaluationFunction
