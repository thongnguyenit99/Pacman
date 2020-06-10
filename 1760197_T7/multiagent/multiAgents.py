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
import random
import util

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
      # Thu thập các động thái pháp lý và trạng thái của game hiện tại

        legalMoves = gameState.getLegalActions()

        # Chọn ra trạng thái tốt nhất trong danh sách trạng thái để trả về hướng đi tốt nhất
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Hàm evaluationFunction() nhận đầu vào là trạng thái hiện tại của game và một hành động mà Pacman
         có thể thực hiện từ trạng thái này. Kết quả trả về sẽ là điểm số ước lượng của hành động này,
          điểm số càng cao thì hành động càng được ưu tiên. 
          Đoạn code có sẵn trong hàm evaluationFunction() cung cấp sẵn cho chúng ta cách trích xuất một số 
          thông tin hữu ích từ trạng thái của game
        """
        #  Lấy trạng thái mới của game sau khi Pacman thực hiện action.
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # Lấy vị trí của Pacman sau khi Pacman thực hiện action.
        newPos = successorGameState.getPacmanPosition()
       # Cập nhật phần thức ăn còn lại sau khi Pacman thực hiện action.
        newFood = successorGameState.getFood()
        # Cập nhật trạng thái mới của ma sau khi Pacman thực hiện action.
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """tính khoảng cách đến thức ăn xa nhất"""
        newFoodList = newFood.asList()
        min_food_distance = -1
        for food in newFoodList:
            distance = util.manhattanDistance(newPos, food)
            if min_food_distance >= distance or min_food_distance == -1:
                min_food_distance = distance

        """Tính khoảng cách từ pacman đến hồn ma.
         Ngoài ra, kiểm tra sự gần gũi của những con ma (ở khoảng cách 1) xung quanh pacman."""
        distances_to_ghosts = 1
        proximity_to_ghosts = 0
        for ghost_state in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost_state)
            distances_to_ghosts += distance
            if distance <= 1:
                proximity_to_ghosts += 1

        """Tổng hợp số liệu vừa tìm dc sẻ trả về"""
        return successorGameState.getScore() + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """

        Khi viết hàm getAction() (cũng như là các hàm phụ trợ) trong class MinimaxAgent,
             bạn có thể gọi self.depth và self.evaluationFunction (self.depth và self.evaluationFunction
             được định nghĩa trong class MultiAgentSearchAgent, class MinimaxAgent kế thừa từ class này): 

             • self.depth cho biết biết độ sâu giới hạn của cây (số bước nhìn xa về tương lai). 
              Lưu ý: một đơn vị độ sâu ở đây gồm một lần đi của Pacman và tất cả các ma sau đó;
               như vậy, độ sâu bằng 2 nghĩa là: Pacman đi, tất cả các ma lần lượt đi,
                Pacman đi, tất cả các ma lần lượt đi

      • self.evaluationFunction nhận đầu vào là
        một trạng thái mà không phải là trạng thái kết thúc game và trả về giá trị ước lượng của trạng thái đó.
        self.evaluationFunction mặc định là scoreEvaluationFunction

        // trả về trạng thái successor của game sau khi agent thực hiện hành động.    
        • Lệnh gameState.generateSuccessor(agentIndex, action): 
        • Lệnh gameState.getNumAgents(): // trả về tổng số agent trong game. 
        • Lệnh gameState.getLegalActions(agentIndex): // Trả về các hành động mà agent có thể thực hiện.

        """
        "*** YOUR CODE HERE ***"
        # Đầu tiên, trong thuật toán này, hàm Minimax sẽ có 3 tham số đầu vào
        # Đó chính là: agent,độ sâu, và trạng thái của game
        def minimax(agent, depth, gameState):
            # Nếu mà trạng thái này thua/thắng hoặc độ sâu của agent bằng độ sau giới hạn trong khung chơi thì
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                # Trả về giá trị ước lượng của trạng thái mà pacman thực hiện hành động
                return self.evaluationFunction(gameState)
       # tại đây có 2 trường hợp:
       # 1 là khi agent=0 hoặc trường hợp còn lại

            if agent == 0:  # maximize for pacman
                # trả về trạng thái successor của game sau khi agent thực hiện hành động
                # và trả về các hành động mà agnet có thể thực hiện
                return max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  # minize for ghosts
                 # Tính toán các Agent và tăng độ sâu(bước đi của pacman đi)
                nextAgent = agent + 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == 0:
                    depth += 1
                    # trả về  chi phi ước lượng ít nhất bằng cách gọi lại hàm
                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))

        """Thực hiện hành động tối đa hoá hành động của pacman"""
        maximum = float("-inf")
        # hướng đi của pacman sẽ là hướng tây
        action = Directions.WEST
        # Trả về các hành động mà agent có thể thực hiện.
        for agentState in gameState.getLegalActions(0):
              # trả về trạng thái successor của game sau khi agent thực hiện hành động
            utility = minimax(1, 0, gameState.generateSuccessor(0, agentState))
            if utility > maximum or maximum == float("-inf"):
                maximum = utility
                action = agentState

        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(agent, depth, game_state, a, b):  # maximizer function
            v = float("-inf")
            for newState in game_state.getLegalActions(agent):
                v = max(v, alphabetaprune(
                    1, depth, game_state.generateSuccessor(agent, newState), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        def minimizer(agent, depth, game_state, a, b):  # minimizer function
            v = float("inf")

            # calculate the next agent and increase depth accordingly.
            next_agent = agent + 1
            if game_state.getNumAgents() == next_agent:
                next_agent = 0
            if next_agent == 0:
                depth += 1

            for newState in game_state.getLegalActions(agent):
                v = min(v, alphabetaprune(next_agent, depth,
                                          game_state.generateSuccessor(agent, newState), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def alphabetaprune(agent, depth, game_state, a, b):
            # return the utility in case the defined depth is reached or the game is won/lost.
            if game_state.isLose() or game_state.isWin() or depth == self.depth:
                return self.evaluationFunction(game_state)

            if agent == 0:  # maximize for pacman
                return maximizer(agent, depth, game_state, a, b)
            else:  # minimize for ghosts
                return minimizer(agent, depth, game_state, a, b)

        """Performing maximizer function to the root node i.e. pacman using alpha-beta pruning."""
        utility = float("-inf")
        action = Directions.WEST
        alpha = float("-inf")
        beta = float("inf")
        for agentState in gameState.getLegalActions(0):
            ghostValue = alphabetaprune(
                1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)
            if ghostValue > utility:
                utility = ghostValue
                action = agentState
            if utility > beta:
                return utility
            alpha = max(alpha, utility)

        return action


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
        def expectimax(agent, depth, gameState):
            # return the utility in case the defined depth is reached or the game is won/lost.
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agent == 0:  # maximizing for pacman
                return max(expectimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  # performing expectimax action for ghosts/chance nodes.
                # calculate the next agent and increase depth accordingly.
                nextAgent = agent + 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == 0:
                    depth += 1
                return sum(expectimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))

        """Performing maximizing task for the root node i.e. pacman"""
        maximum = float("-inf")
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            utility = expectimax(
                1, 0, gameState.generateSuccessor(0, agentState))
            if utility > maximum or maximum == float("-inf"):
                maximum = utility
                action = agentState

        return action


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """Calculating distance to the closest food pellet"""
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newFoodList = newFood.asList()
    min_food_distance = -1
    for food in newFoodList:
        distance = util.manhattanDistance(newPos, food)
        if min_food_distance >= distance or min_food_distance == -1:
            min_food_distance = distance

    """Calculating the distances from pacman to the ghosts. Also, checking for the proximity of the ghosts (at distance of 1) around pacman."""
    distances_to_ghosts = 1
    proximity_to_ghosts = 0
    for ghost_state in currentGameState.getGhostPositions():
        distance = util.manhattanDistance(newPos, ghost_state)
        distances_to_ghosts += distance
        if distance <= 1:
            proximity_to_ghosts += 1

    """Obtaining the number of capsules available"""
    newCapsule = currentGameState.getCapsules()
    numberOfCapsules = len(newCapsule)

    """Combination of the above calculated metrics."""
    return currentGameState.getScore() + (1 / float(min_food_distance)) - (1 / float(distances_to_ghosts)) - proximity_to_ghosts - numberOfCapsules


# Abbreviation
better = betterEvaluationFunction
