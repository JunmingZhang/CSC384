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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        # base value of evaluation
        heur_val = scoreEvaluationFunction(successorGameState) + 1.0 * (max(newScaredTimes) + min(newScaredTimes))
        newGhostPosition = successorGameState.getGhostPositions()
        newFoodPosition = newFood.asList()

        # evaluation returns infinity if win, or negative infinity if lose
        if successorGameState.isWin():
          return float('inf')
        elif successorGameState.isLose():
          return -float('inf')

        # check ghost in the game, if the ghost is pretty close, decrease
        # the evaluation value by 1.0/manhattan distance between position of
        # pacman and the ghost in the next game state. If they are in the same
        # spot, then the ghost is in scare time, since the if the ghost is not
        # in scare time, then the pacman loses. In this case, the evaluation value
        # increases by 1.0.
        for ghostPos in newGhostPosition:
          ghostDistance = manhattanDistance(newPos,ghostPos)
          if ghostDistance <= 3:
            if ghostDistance == 0:
              heur_val += 1.0
            else:
              heur_val -= 1.0 / ghostDistance
        
        # check if there is any food nearby. If any food is around, but not eaten
        # by the pacman, the evaluation value increases by 1.0/manhattan distance between
        # the food and the pacman. If the pacman can eat the food, the evaluation value
        # increases by 1.0
        for foodPos in newFoodPosition:
          foodDistance = manhattanDistance(newPos, foodPos)
          if foodDistance == 0:
            heur_val += 1.0
          elif foodDistance > 0:
            heur_val += 1.0 / foodDistance
        
        return heur_val



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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


def isLastAgent(gameState, agentIndex):
  return (gameState.getNumAgents() - 1 == agentIndex)


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
        """
        "*** YOUR CODE HERE ***"
        bestMove = (self.getActionHelper(0, 0, gameState))[1]
        return bestMove
    
    def getActionHelper(self, depth, agentIndex, gameState):
      """
        recursively find the score gained and the best action should be taken at
        the state input, used by minimax agent. The max player (pacman) tends to
        maximize the score while the min player (ghost) tends to minimize the score
      """
      action = None
      # if the player win or lose or reach the depth of the game search tree,
      # return the score at the current state and no action can be taken
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), action)
      
      if agentIndex == 0: # max player
        score = -float('inf')
      else: # min player
        score = float('inf')
  
      # get all actions can be taken at current agent
      actions = gameState.getLegalActions(agentIndex)
      
      # get the successor from all actions
      # and evaluate the score for the best action
      # for max and min player respecively
      for act in actions:
        nextState = gameState.generateSuccessor(agentIndex, act)
        if isLastAgent(gameState, agentIndex): # next turn is for max player
          nextScore, nextAction = self.getActionHelper(depth + 1, 0, nextState)
        else: # next turn is for min player
          nextScore, nextAction = self.getActionHelper(depth, agentIndex + 1, nextState)

        if agentIndex == 0 and nextScore > score: # max player and the score of child node > score currently
          score = nextScore
          action = act
        elif agentIndex != 0 and nextScore < score: # min player and the score of child node < score currently
          score = nextScore
          action = act
      
      return (score, action)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestMove = (self.getActionHelper(0, 0, gameState, -float('inf'), float('inf')))[1]
        return bestMove
    
    def getActionHelper(self, depth, agentIndex, gameState, alpha, beta):
      """
        recursively find the score gained and the best action should be taken at
        the state input, used by alpha-beta agent. The max player (pacman) tends to
        maximize the score while the min player (ghost) tends to minimize the score

        Cutting min node n (for max player):
        alpha - max of n's sibling
        beta - min of n's children
        
        Cutting max node n (for min player):
        alpha - max of n's children
        beta - min of n's sibling
      """
      action = None
      # if the player win or lose or reach the depth of the game search tree,
      # return the score at the current state and no action can be taken
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), action)
  
      if agentIndex == 0: # max player
        score = -float('inf')
      else: # min player
        score = float('inf')
      
      # get all actions can be made at the current agent
      actions = gameState.getLegalActions(agentIndex)
      
      # get the successor from all actions
      # and evaluate the score for the best action
      # for max and min player respecively
      # use pruning (break) to save time
      for act in actions:
        nextState = gameState.generateSuccessor(agentIndex, act)
        if isLastAgent(gameState, agentIndex): # next turn is for max player
          nextScore, nextAction = self.getActionHelper(depth + 1, 0, nextState, alpha, beta)
        else: # next turn is for min player
          nextScore, nextAction = self.getActionHelper(depth, agentIndex + 1, nextState, alpha, beta)

        if agentIndex == 0: # next turn is for max player
          alpha = max(alpha, nextScore) # alpha always takes max value between itself and the score of the child
          if nextScore > score: # for max player, always try to increase score
            score = nextScore
            action = act
        else: # next turn is for min turn
          beta = min(beta, nextScore) # beta always takes min value between itself and the score of the child
          if score < nextScore: # for min player, always try to decrease score
            score = nextScore
            action = act

        if beta <= alpha: # break if alpha exceeds beta
            break
      
      if agentIndex == 0: # max player, return alpha for maximization
        return (alpha, action)
      else: # min player, return beta for minimization
        return (beta, action)


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
        bestMove = (self.getActionHelper(0, 0, gameState))[1]
        return bestMove
    
    def getActionHelper(self, depth, agentIndex, gameState):
      """
        recursively find the score gained and the best action should be taken at
        the state input, used by minimax agent. The max player (pacman) tends to
        maximize the score while the chance player (ghost) tends to pick the score
        by probability
      """
      action = None
      # if the player win or lose or reach the depth of the game search tree,
      # return the score at the current state and no action can be taken
      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), action)
  
      if agentIndex == 0: # max player
        score = -float('inf')
      else: # min player
        score = float('inf')
      
      # get all actions can be made at the current agent
      actions = gameState.getLegalActions(agentIndex)
      
      # set the sum of scores and the number of scores for chance player
      # in order to find the average socre for chance player
      chanceScore = 0
      chanceScoreTimes = 0

      # get the successor from all actions
      # and evaluate the score for the best action
      # for max and mchance player respecively
      for act in actions:
        # find the next state caused by the act
        nextState = gameState.generateSuccessor(agentIndex, act)
        if isLastAgent(gameState, agentIndex): # next turn is for max player
          nextScore, nextAction = self.getActionHelper(depth + 1, 0, nextState)
        else: # next turn is for chance player
          nextScore, nextAction = self.getActionHelper(depth, agentIndex + 1, nextState)
        
        if agentIndex == 0: # get best action and score for max player
          if score < nextScore:
            score = nextScore
            action = act
        elif agentIndex != 0: # get score for chance player, action does not change
          chanceScore += nextScore
          chanceScoreTimes += 1
          # call probability method to get the score of the chance player
          score = self.__prob(chanceScore, chanceScoreTimes)

      return (score, action)
    
    def __prob(self, chanceScore, chanceScoreTimes):
      """
        compute the score for the chance score
        i.e., find the average of scores of chance player
      """
      return float(chanceScore) / float(chanceScoreTimes)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # get all useful information
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostPositions = currentGameState.getGhostPositions()
    foodPositions = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    ghostScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]


    # get the basic value for evaluation
    heur_val = scoreEvaluationFunction(currentGameState) + 2.75 * (max(ghostScaredTimes) + min(ghostScaredTimes))

    # evaluation returns infinity if win, or negative infinity if lose
    if currentGameState.isWin():
      return float('inf')
    elif currentGameState.isLose():
      return -float('inf')

    
    # check ghost in the game, if the ghost is pretty close, decrease
    # the evaluation value by 2.5/manhattan distance between position of
    # pacman and the ghost in the next game state. If they are in the same
    # spot, then the ghost is in scare time, since the if the ghost is not
    # in scare time, then the pacman loses. In this case, the evaluation value
    # increases by 2.0. (For better evaluation, there are weights for factors)
    for ghostPos in ghostPositions:
      ghostDistance = manhattanDistance(pacmanPosition,ghostPos)
      if ghostDistance <= 3:
        if ghostDistance == 0:
          heur_val += 2,0
        else:
          heur_val -= 2.5 / ghostDistance
    
    # check if there is any food nearby. If any food is around, but not eaten
    # by the pacman, the evaluation value increases by 2.0/manhattan distance between
    # the food and the pacman. If the pacman can eat the food, the evaluation value
    # increases by 2.0. (For better evaluation, there are weights for factors)
    for foodPos in foodPositions:
      foodDistance = manhattanDistance(pacmanPosition, foodPos)
      if foodDistance == 0:
        heur_val += 2.0
      elif foodDistance > 0:
        heur_val += 2.0 / foodDistance

    return heur_val




# Abbreviation
better = betterEvaluationFunction
