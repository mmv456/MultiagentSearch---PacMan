# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

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

        # Don't need to do anything here as of now
        
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

        # create the minimum counter
        minimumFoodDistance = sys.maxint
        
        newFoodList = newFood.asList()
        
        for f in newFoodList:
            # figure I don't have to make the manhattanDistance function
            # because the util library has it
            if util.manhattanDistance(newPos, f) < minimumFoodDistance:
                minimumFoodDistance = util.manhattanDistance(newPos, f)
        
        # create the maximum counter
        maximumFoodDistance = 0
        
        for f in newFoodList:
            if util.manhattanDistance(newPos, f) > maximumFoodDistance:
                maximumFoodDistance = util.manhattanDistance(newPos, f)

        # create a variable to keep track of the closes distance to a ghost
        ghostDistance = sys.maxint
        
        for ghost in newGhostStates:
            if util.manhattanDistance(newPos, ghost.getPosition()) < ghostDistance:
                ghostDistance = util.manhattanDistance(newPos, ghost.getPosition())

        

        value = (1.0 / (minimumFoodDistance + 1.0)) + (successorGameState.getScore()) - (1.0 / (ghostDistance + 1.0))
        if ghostDistance == 0 or ghostDistance == 1:
            value = -sys.maxint - 1
        
        return value
        
        #return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"

        # keep track of the number of agents in the game
        numAgents = gameState.getNumAgents()

        # create a helper function to ease the process of minimax
        def helper(gameState, depth, agent):

            
            def overallValue(gameState, depth, agent):

                if gameState.isWin() or gameState.isLose() or depth == 0:

                    #print gameState
                    return self.evaluationFunction(gameState), None
                
                if agent == 0:
                    return maximum(gameState, depth, agent)
                
                #return maximum(gameState, depth, agent)
                return minimum(gameState, depth, agent)
            
            def maximum(gameState, depth, agent):

                #there's no action needed for this
                action = None
                # have a counter for the most negative value Python 2 can handle
                count = -sys.maxint - 1
                
                
                for agentAction in gameState.getLegalActions(agent):
                    
                    finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents)[0]
                    #print finalValue
                    
                    if finalValue > count:
                        count = finalValue
                        action = agentAction
                        
                # what to return here?
                return count, action

            def minimum(gameState, depth, agent):
                
                # again no action needed at first
                action = None
                # have a counter for the most positive number Python 2 can handle
                count = sys.maxint
                
                
                for agentAction in gameState.getLegalActions(agent):
                    if (agent + 1) % numAgents == 0:
                        # what to put here? --> TA hours

                        # change in depth is all that's needed, and same for the else
                        # depth - 1
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth - 1, (agent + 1) % numAgents)[0]
                    else:
                        # ??

                        # depth
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents)[0]

                    if finalValue < count:
                        count = finalValue
                        action = agentAction
                        
                #print count
                return count, action
            
            return overallValue(gameState, depth, 0)

        # for the whole of minimax, go through this helper function
        return helper(gameState, self.depth, 0)[1]
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        
        def helper(gameState, depth, agent, alpha, beta):
            
            def overallValue(gameState, depth, agent, alpha, beta):
                
                if gameState.isWin() or gameState.isLose() or depth == 0:
                    return self.evaluationFunction(gameState), None
                
                if agent == 0:
                    return maximum(gameState, depth, agent, alpha, beta)
                
                # maximum or minimum? --> TA
                return minimum(gameState, depth, agent, alpha, beta)

            def maximum(gameState, depth, agent, alpha, beta):
                
                action = None
                count = -sys.maxint - 1
                
                
                for agentAction in gameState.getLegalActions(agent):
                    
                    finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents, alpha, beta)[0]
                    
                    if finalValue > beta:
                        return finalValue, agentAction
                    
                    if finalValue > count:
                        count = finalValue
                        action = agentAction
                    alpha = max(alpha, count)
                    
                return count, action

            def minimum(gameState, depth, agent, alpha, beta):
                
                action = None
                count = sys.maxint
                
                
                for agentAction in gameState.getLegalActions(agent):
                    
                    if (agent + 1) % numAgents == 0:
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth - 1, (agent + 1) % numAgents, alpha, beta)[0]
                        
                    else:
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents, alpha, beta)[0]
                        
                    if finalValue < alpha:
                        return finalValue, agentAction
                    
                    if finalValue < count:
                        count = finalValue
                        action = agentAction
                    beta = min(beta, count)
                    
                return count, action
            
            return overallValue(gameState, depth, 0, alpha, beta)

        return helper(gameState, self.depth, 0, -sys.maxint - 1, sys.maxint)[1]
        #util.raiseNotDefined()

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
        
        numAgents = gameState.getNumAgents()
        
        def helper(gameState, depth, agent):

            
            def overallValue(gameState, depth, agent):
                
                if gameState.isWin() or gameState.isLose() or depth == 0:
                    return self.evaluationFunction(gameState), None
                
                if agent == 0:
                    return maximum(gameState, depth, agent)

                
                return average(gameState, depth, agent), None

            def maximum(gameState, depth, agent):

                action = None
                count = -sys.maxint - 1
                
                for agentAction in gameState.getLegalActions(agent):
                    finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents)[0]
                    
                    if finalValue > count:
                        count = finalValue
                        action = agentAction
                        
                return count, action

            # note that this is not minimum like in the other two functions, this is average
            def average(gameState, depth, agent):

                count = 0
                
                for agentAction in gameState.getLegalActions(agent):
                    
                    if (agent + 1) % numAgents == 0:
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth - 1, (agent + 1) % numAgents)[0]
                        
                    else:
                        finalValue = overallValue(gameState.generateSuccessor(agent, agentAction), depth, (agent + 1) % numAgents)[0]
                        
                    count += finalValue
                    
                return float(count) / len(gameState.getLegalActions(agent))
            
            return overallValue(gameState, depth, 0)


        return helper(gameState, self.depth, 0)[1]
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: There are five main values I am computing in this function.
                  First is the minimumFoodDistance which calculates the closest distance to food.
                  Second is the minimum capsule distance, which is the closest to the power dots.
                  Third is total time the ghosts get scared.
                  Fourth is the maximum distance to all of the food in total.
                  Fifth is the closest distance to one of the ghosts.
                  Once I do that I then use all five of these values to compute one single
                  value to evaluate which step Pacman has to take next.
    """
    "*** YOUR CODE HERE ***"

    # Create five separate variables, each of which will be involved in thhe
    # final evaluation equation
    # Look above for the descriptions of each
    agentPosition = currentGameState.getPacmanPosition()
    listOfFood = currentGameState.getFood()
    listOfCapsules = currentGameState.getCapsules()
    ghostLocations = currentGameState.getGhostStates()
    timesScared = [location.scaredTimer for location in ghostLocations]

    
    minimumFoodDistance = sys.maxint
    listOfFood = listOfFood.asList()
    
    for food in listOfFood:
        if util.manhattanDistance(agentPosition, food) < minimumFoodDistance:
            minimumFoodDistance = util.manhattanDistance(agentPosition, food)
    #print "minimumFoodDistance: " + str(minimumFoodDistance)


            
    minimumCapsuleDistance = sys.maxint
    
    for capsule in listOfCapsules:
        if util.manhattanDistance(agentPosition, capsule) < minimumCapsuleDistance:
            minimumCapsuleDistance = util.manhattanDistance(agentPosition, capsule)


            
    totalTimeScared = reduce(lambda x, y: x + y, timesScared, 0)
    

    
    maximumFoodDistance = 0
    
    for food in listOfFood:
        if util.manhattanDistance(agentPosition, food) > maximumFoodDistance:
            maximumFoodDistance = util.manhattanDistance(agentPosition, food)


            
    closestGhostDistance = sys.maxint
    
    for location in ghostLocations:
        if util.manhattanDistance(agentPosition, location.getPosition()) < closestGhostDistance:
            closestGhostDistance = util.manhattanDistance(agentPosition, location.getPosition())
    #print "closestGhostDistance: " + str(closestGhostDistance)
    
    value = (1.0 / (minimumFoodDistance + 1.0)) + (currentGameState.getScore()) - (1.0 / (closestGhostDistance + 1.0)) + (1.0 / (minimumCapsuleDistance + 1.0)) + totalTimeScared


                        
    if closestGhostDistance == 0 or closestGhostDistance == 1:
        value = -sys.maxint - 1

    #print "value: " + str(value)


    return value
    #util.raiseNotDefined()



# Abbreviation
better = betterEvaluationFunction

