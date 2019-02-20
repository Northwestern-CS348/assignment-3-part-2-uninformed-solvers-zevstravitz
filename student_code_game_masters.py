from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        find_disk = 0
        while (True):
            found = 0
            peg1_tuple, peg2_tuple, peg3_tuple = (),(),()
            for fact in GameMaster.kb.facts:
                if fact.statement.predicate == 'on':
                    disk_string = fact.statement.terms[0].term.element
                    peg_string = fact.statement.terms[1].term.element
                    diskNumber = int(disk_string[-1])

                    if diskNumber == find_disk:
                        found = 1
                        if peg_string == "peg1":
                            peg1_tuple += ([diskNumber])
                        elif peg_string == "peg2":
                            peg2_tuple += ([diskNumber])
                        elif peg_string == "peg3":
                            peg3_tuple += ([diskNumber])
                        find_disk += 1
                        break
            if found == 0:
                return (peg1_tuple, peg2_tuple,peg3_tuple)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        move_disk = movable_statement.terms[0].term.element
        peg1 = movable_statement.terms[1].term.element
        peg2 = movable_statement.terms[2].term.element



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1, row2, row3 = (),(),()
        for column in range(1,5):
            for row in range(1,5):
                found = 0
                for fact in self.kb.facts:
                    if fact.statement.predicate == "posn":
                        tile_string = fact.statement.terms[0].term.element
                        column_string = fact.statement.terms[1].term.element
                        row_string = fact.statement.terms[2].term.element

                        tile_num = int(tile_string[-1])
                        column_num = int(column_string[-1])
                        row_num = int(row_string[-1])

                        if row_num == row and column_num == column:
                            found = 1
                            if row_num == 1:
                                row1 += tuple([tile_num])
                            elif row_num == 2:
                                row2 += tuple([tile_num])
                            elif row_num == 3:
                                row3 += tuple([tile_num])
                            break

                if found == 0:
                    if row == 1:
                        row1 += tuple([-1])
                    elif row == 2:
                        row2 += tuple([-1])
                    elif row == 3:
                        row3 += tuple([-1])

        return (row1, row2, row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
