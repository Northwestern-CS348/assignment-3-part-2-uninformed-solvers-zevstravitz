from solver import *

from solver import *

class Queue:
    def __init__(self, data=[]):
        self.visited = data[:]

    def len(self):
        return len(self.visited)

    def isempty(self):
        return len(self.visited) == 0

    def enqueue(self, x):
        return self.visited.append(x)

    def dequeue(self):
        return self.visited.pop(0)

    def peek(self):
        return self.visited[0]

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
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True
        elif len(self.currentState.children) == 0:
            frontier = self.gm.getMovables()
            for move in frontier:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                child.parent = self.currentState
                self.currentState.children.append(child)
                self.gm.reverseMove(move)
                if child in self.visited:
                    continue

        next_child_index = self.currentState.nextChildToVisit
        num_children = len(self.currentState.children)

        # child = self.currentState.children[next_child_index] //errors on 7th
        end = False
        for child_num in range(next_child_index, num_children):
            if self.currentState.children[next_child_index] not in self.visited:
                self.currentState.nextChildToVisit = child_num + 1
                child = self.currentState.children[child_num]
                self.currentState = child
                self.visited[child] = True
                self.gm.makeMove(child.requiredMovable)
                return self.currentState.state == self.victoryCondition
            elif child_num+1 == num_children:
                end=True
        if end:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.solveOneStep()


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.discovered = Queue()

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
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        if self.currentState.depth == 0:
            self.currentState.requiredMovable = []
        movables = self.gm.getMovables()
        if movables:
            for move in movables:
                self.gm.makeMove(move)
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, self.currentState.requiredMovable + [move])
                self.gm.reverseMove(move)
                if not newState in self.visited:
                    self.visited[newState] = True
                    self.discovered.enqueue(newState)
                    self.currentState.children.append(newState)
        if not self.discovered.isempty():
            return self.check_discovered()

    def check_discovered(self):
        next_movable = self.discovered.dequeue()
        req_movable = self.currentState.requiredMovable
        next = next_movable.requiredMovable
        req_pos = 0
        while (req_pos < len(req_movable)):
            if req_movable[req_pos] != next[req_pos]:
                break
            req_pos+=1
        pos = len(req_movable) - 1
        while (pos > req_pos-1):
            self.gm.reverseMove(req_movable[pos])
            pos-=1
        while req_pos < len(next):
            self.gm.makeMove(next[req_pos])
            req_pos+=1
        self.currentState = next_movable
        found = self.currentState.state == self.victoryCondition
        return found