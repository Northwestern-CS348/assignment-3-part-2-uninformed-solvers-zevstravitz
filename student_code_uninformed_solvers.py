
from solver import *

class Queue:
    def __init__(self, data=[]):
        self.visited = data[:]

    def isempty(self):
        return len(self.visited) == 0

    def enqueue(self, x):
        return self.visited.append(x)

    def dequeue(self):
        return self.visited.pop(0)

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        # first, check to see if the current gamestate is solved
        if self.gm.getGameState() == self.victoryCondition:
            return True

        frontier = self.gm.getMovables()

        if len(frontier) == 0:
            self.currentState = self.currentState.parent
            self.solveOneStep()
        else:
            find_unvisited = False
            for move in frontier:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                self.gm.reverseMove(move)
                if child in self.visited:
                    continue
                find_unvisited = True
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.visited[child] = True
                self.gm.makeMove(move)
                self.currentState = child
                break
            if not find_unvisited:
                self.gm.reverseMove(move)
                self.currentState = self.currentState.parent
                self.solveOneStep()

class SolverBFS(UninformedSolver):


    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.explored = Queue()

    def findNextNode(self, nextGameState):
        while not self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        while nextGameState.depth != self.currentState.depth:
            traverse_node = nextGameState
            while traverse_node.depth != (self.currentState.depth + 1):
                traverse_node = traverse_node.parent
            for child in self.currentState.children:
                if child.requiredMovable == traverse_node.requiredMovable:
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    break
        return

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.gm.getGameState() == self.victoryCondition:
            return True

        if self.explored.isempty():
            frontier = self.gm.getMovables()
            for move in frontier:
                self.gm.makeMove(move)
                curr_gs = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

                if not self.visited.get(curr_gs, False):
                    if not curr_gs in self.currentState.children:
                        self.currentState.children.append(curr_gs)
                        curr_gs.parent = self.currentState
                        self.visited[curr_gs] = True
                        self.explored.enqueue(curr_gs)

                self.gm.reverseMove(move)

        next_gs = self.explored.dequeue()
        self.findNextNode(next_gs)
        if self.gm.getGameState() == self.victoryCondition:
            return True

        frontier = self.gm.getMovables()
        for move in frontier:
            self.gm.makeMove(move)
            curr_gs = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

            if not self.visited.get(curr_gs, False):
                if not curr_gs in self.currentState.children:
                    self.currentState.children.append(curr_gs)
                    curr_gs.parent = self.currentState

                    self.visited[curr_gs] = True
                    self.explored.enqueue(curr_gs)
            self.gm.reverseMove(move)