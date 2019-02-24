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

        disks_on_peg1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1'))
        disks_on_peg2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2'))
        disks_on_peg3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3'))
        t1 = []
        t2 = []
        t3 = []

        if disks_on_peg1:
            for disks in disks_on_peg1:
                # get the name and take the last index for the number
                disk = int(str(disks.bindings[0].constant)[-1])
                t1.append(disk)
        if disks_on_peg2:
            for disks in disks_on_peg2:
                disk = int(str(disks.bindings[0].constant)[-1])
                t2.append(disk)
        if disks_on_peg3:
            for disks in disks_on_peg3:
                disk_string = str(disks.bindings[0].constant)[-1]
                disk_int = int(disk_string)
                t3.append(disk_int)

        t1.sort()
        t2.sort()
        t3.sort()

        gs_hanoi = (tuple(t1), tuple(t2), tuple(t3))

        return gs_hanoi

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
        peg_init = movable_statement.terms[1].term.element
        peg_final = movable_statement.terms[2].term.element

        # ______________RESET FACTS AT OLD POSITION_______________
        self.kb.kb_retract(parse_input("fact: (on " + move_disk + " " + peg_init + ")"))
        self.kb.kb_retract(parse_input("fact: (top " + move_disk + " " + peg_init + ")"))

        old_under_disk = self.kb.kb_ask(parse_input("fact: (onTopOf " + move_disk + "?x)"))

        if not old_under_disk:
            self.kb.kb_assert(parse_input('fact: (empty ' + peg_init + ')'))
        else:
            below_disk = old_under_disk[0].bindings_dict['?x']
            self.kb.kb_assert(parse_input('fact: (top ' + below_disk + ' ' + peg_init + ')'))
            self.kb.kb_retract(parse_input('fact: (onTopOf ' + move_disk + ' ' + below_disk + ')'))

        # ______________RESET FACTS AT NEW POSITION_______________
        new_empty_under = self.kb.kb_ask(parse_input('fact: (empty ' + peg_final + ')'))

        if not new_empty_under:
            curr_target_top = self.kb.kb_ask(parse_input('fact: (top ?x ' + peg_final + ')'))
            below_disk = curr_target_top[0].bindings_dict['?x']
            self.kb.kb_retract(parse_input('fact: (top ' + below_disk + ' ' + peg_final + ')'))

            self.kb.kb_assert(parse_input('fact: (top ' + move_disk + ' ' + peg_final))
            self.kb.kb_assert(parse_input('fact: (onTopOf ' + move_disk + ' ' + below_disk))
            self.kb.kb_assert(parse_input('fact: (on ' + move_disk + ' ' + peg_final + ')'))
        else:
            self.kb.kb_retract(parse_input('fact: (empty ' + peg_final + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + move_disk + ' ' + peg_final + ')'))
            self.kb.kb_assert(parse_input('fact: (on ' + move_disk + ' ' + peg_final + ')'))

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


        #all rows begin as being empty
        row1, row2, row3 = (),(),()
        # comb through all of the tiles
        for fact in self.kb.facts:
            if fact.statement.predicate == "coordinate":
                # Break up the fact
                tile_string = fact.statement.terms[0].term.element
                column_string = fact.statement.terms[1].term.element
                row_string = fact.statement.terms[2].term.element

                column_num = int(column_string[-1])
                row_num = int(row_string[-1])

                if tile_string[-1] == 'y':
                    if row_num == 1:
                        row1 += tuple([-1])
                    elif row_num == 2:
                        row2 += tuple([-1])
                    elif row_num == 3:
                        row3 += tuple([-1])
                    continue

                tile_num = int(tile_string[-1])

                if row_num == 1:
                    row1 += tuple([tile_num])
                elif row_num == 2:
                    row2 += tuple([tile_num])
                elif row_num == 3:
                    row3 += tuple([tile_num])
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
        tile = movable_statement.terms[0].term.element
        col1 = movable_statement.terms[1].term.element
        row1 = movable_statement.terms[2].term.element
        col2 = movable_statement.terms[3].term.element
        row2 = movable_statement.terms[4].term.element

        fact_old_posn = parse_input("fact: (coordinate " + tile + " " + col1 + " " + row1 + ")")
        self.kb.kb_retract(fact_old_posn)

        fact_new_posn = parse_input("fact: (coordinate " + tile + " " + col2 + " " + row2 + ")")
        self.kb.kb_assert(fact_new_posn)

        fact__old_empty_posn = parse_input("fact: (coordinate empty " + col2 + " " + row2 + ")")
        self.kb.kb_retract(fact__old_empty_posn)

        fact__new_empty_posn = parse_input("fact: (coordinate empty " + col1 + " " + row1 + ")")
        self.kb.kb_assert(fact__new_empty_posn)

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
