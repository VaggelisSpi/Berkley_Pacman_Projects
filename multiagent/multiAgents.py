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

def euclideanDistance(x1, x2, y1, y2):
        "The Euclidean distance heuristic for a PositionSearchProblem"
        return ( (x1 - y1) ** 2 + (x2 - y2) ** 2 ) ** 0.5

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        "*** YOUR CODE HERE ***"
        # if successor state wins return a very high number
        if successorGameState.isWin():
          return 999999

        # Get the information from the current game state
        curFood = currentGameState.getFood()
        curFoodList = curFood.asList()

        # Get the information from the successor game state
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newFoodList = newFood.asList()
        newFoodCount = len(newFoodList)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPos = [ghostState.getPosition() for ghostState in newGhostStates]

        # Find the manhattan distance from pacman to all the foods in the
        # sucessor state
        newFoodDists = []
        for food in newFoodList:
            newFoodDists.append(manhattanDistance(newPos, food))

        score = 0

        # return a very high low if pacman will be eaten
        for i in range(len(newScaredTimes)):
            if newScaredTimes[i] <= 0 and newPos == newGhostPos[i]:
                return float("-Inf")
          # increase score if pacman eats a ghost
            elif newScaredTimes[i] > 0 and newPos == newGhostPos[i]:
                score += 500

        # if pacman eats food in the following state increase the score
        if newPos in curFoodList:
            score += 200

        # if pacman eats pellet in the following state increase the score
        if newPos in currentGameState.getCapsules():
            score += 500

        # penalty for stoping
        if action == Directions.STOP:
            score -= 30

        # reduce score by 10 for each food left
        score -= 10*newFoodCount
        # reduce score based on how far the closest food is, so the closer we
        # get to a food the greater the score
        score -= 2*min(newFoodDists)

        return score

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
    def maxValue(self, gameState, agentIndex, depth):
        # if max depth was reached or pacamn wins then we shouldn't look any further
        if gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)

        maxScore = float("-Inf")

        actions = gameState.getLegalActions(agentIndex)
        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            maxScore = max(maxScore, self.minValue(successor, 1, depth))

        return maxScore

    def minValue(self, gameState, agentIndex, depth):
        minScore = float("+Inf")

        actions = gameState.getLegalActions(agentIndex)
        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # if we are in the last ghost we'll invoke pacman next
            if (agentIndex == gameState.getNumAgents() - 1):
                minScore = min(minScore, self.maxValue(successor, 0, depth - 1))
            else:
            # if we have more ghosts to search for we'll invoke the next ghost
                minScore = min(minScore, self.minValue(successor, agentIndex + 1, depth))

        return minScore

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
        """
        "*** YOUR CODE HERE ***"

        actions = gameState.getLegalActions(0)
        maxScore = float("-Inf")
        maxAction = None
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            succScore = self.minValue(successor, 1, self.depth)
            # assign the action we will return to the highest scoring move
            if succScore > maxScore:
                maxScore = succScore
                maxAction = action

        return maxAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
        # if max depth was reached or pacamn wins then we shouldn't look any further
        if gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)

        maxScore = float("-Inf")

        actions = gameState.getLegalActions(agentIndex)
        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            maxScore = max(maxScore, self.minValue(successor, 1, depth, alpha, beta))
            if maxScore > beta:
                return maxScore
            alpha = max(alpha, maxScore)

        return maxScore

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        minScore = float("+Inf")

        actions = gameState.getLegalActions(agentIndex)
        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # if we are in the last ghost we'll invoke pacman next
            if (agentIndex == gameState.getNumAgents() - 1):
                minScore = min(minScore, self.maxValue(successor, 0, depth - 1, alpha, beta))
                if minScore < alpha:
                    return minScore
                beta = min(beta, minScore)
            else:
            # if we have more ghosts to search for we'll invoke the next ghost
                minScore = min(minScore, self.minValue(successor, agentIndex + 1, depth, alpha, beta))
                if minScore < alpha:
                    return minScore
                beta = min(beta, minScore)

        return minScore


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        maxScore = float("-Inf")
        maxAction = None
        alpha = float("-Inf")
        beta = float("+Inf")
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            succScore = self.minValue(successor, 1, self.depth, alpha, beta)
            # If the score is bigger than beta then prune the remainign
            # successors of the root
            if succScore > beta:
                return action
            # assign the action we will return to the highest scoring move
            if succScore > maxScore:
                maxScore = succScore
                maxAction = action
            alpha = max(alpha, succScore)

        return maxAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self, gameState, agentIndex, depth):
        # if max depth was reached or pacamn wins then we shouldn't look any further
        if gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)

        maxScore = float("-Inf")

        actions = gameState.getLegalActions(agentIndex)
        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            maxScore = max(maxScore, self.exp_value(successor, 1, depth))

        return maxScore

    def exp_value(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)

        # return the score of the current state if there are no successors
        if len(actions) == 0:
            return self.evaluationFunction(gameState)

        succScores = []
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # if we are in the last ghost we'll invoke pacman next
            if (agentIndex == gameState.getNumAgents() - 1):
                succScores.append(self.maxValue(successor, 0, depth - 1))
            else:
            # if we have more ghosts to search for we'll invoke the next ghost
                succScores.append(self.exp_value(successor, agentIndex + 1, depth))

        # expected value is the average of the successors' scores
        return sum(succScores)/len(succScores)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        maxScore = float("-Inf")
        maxAction = None
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            succScore = self.exp_value(successor, 1, self.depth)
            if succScore > maxScore:
                maxScore = succScore
                maxAction = action

        return maxAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # if successo state wins return a very high number
    if currentGameState.isWin():
      return 999999

     #  Get information for the current state
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    foodCount = len(foodList)
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPos = [ghostState.getPosition() for ghostState in ghostStates]
    capsuleList = currentGameState.getCapsules()

    score = 0

    # Get the manhattan distance to each food
    foodDists = []
    for food in foodList:
      foodDists.append(manhattanDistance(pos, food))

    # Get the manhattan distance to each capsule
    capsuleDists = []
    for capsule in capsuleList:
        capsuleDists.append(manhattanDistance(pos, capsule))

    # Get the manhattan distance to each ghost
    ghostDists = []
    for ghost in ghostPos:
      ghostDists.append(manhattanDistance(pos, ghost))

    score = 0

    for i in range(len(scaredTimes)):
        if scaredTimes[i] <= 0:
        # reduce score for being near to non scared ghosts because things might
        # get dangerous
            score -= 25*ghostDists[i]
        elif scaredTimes[i] > 0:
        # higher weight for being near to scared ghosts than being near to non
            score += 10*ghostDists[i]

    # reduce score for the number of food and power pellets left
    score -= 10*foodCount
    score -= 15*len(capsuleList)
    # value higher the closer foods
    for foodDist in foodDists:
        score += 10/foodDist

    # value higher the closer capsules
    for capsuleDist in capsuleDists:
        score += 5/capsuleDist

    # take into account the actual score too
    return score + 5*currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
