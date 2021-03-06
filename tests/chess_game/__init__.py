import testify as T

from chess_game import board
from chess_game import common
from chess_game import notation
from chess_game import pieces
from chess_game import rules
from chess_game.move import Move
from chess_game.position import Position


class BasePlayableChessGameTestCase(T.TestCase):

    __test__ = False

    @T.let
    def chess_board(self):
        return board.BasicChessBoard()

    @T.let
    def notation_processor(self):
        return notation.ChessNotationProcessor(self.chess_rules)

    @T.let
    def chess_rules(self):
        return rules.ChessRules(self.chess_board)

    def build_move(self, src, dst, *args, **kwargs):
        return Move(src, dst, self.chess_rules, *args, **kwargs)

    def make_legal_promotion(self, src, dst, **kwargs):
        return self.make_legal_move(self.build_move(src, dst, self.chess_rules, **kwargs))

    def make_legal_move(self, *args):
        if len(args) == 2:
            return self._make_legal_move(args)
        move, = args
        return self._make_legal_move(move)

    def _make_legal_move(self, move):
        if not isinstance(move, Move):
            src, dst = move
            move = Move(src, dst, self.chess_rules)
        return self.chess_rules.make_legal_move(move)

    def make_legal_moves(self, moves):
        for move in moves:
            self.make_legal_move(move)

    def set_piece(self, algebraic_move, piece):
        self.chess_rules[algebraic_move] = piece

    def check_move_info(self, algebraic_move, src, dst, *args, **kwargs):
        T.assert_equal(
            self.notation_processor.parse_algebraic_move(algebraic_move),
            Move(src, dst, self.chess_rules, *args, **kwargs)
        )

    @staticmethod
    def assert_position_sets_equal(left, right):
        left = map(Position.make, left)
        right = map(Position.make, right)
        if not isinstance(left, set):
            left = set(left)

        if not isinstance(right, set):
            right = set(right)

        T.assert_sets_equal(left, right)


class ClearedBoardPlayableChessGameTestCase(BasePlayableChessGameTestCase):

    class ClearChessBoard(board.BasicChessBoard):

        @property
        def _new_board_array(self):
            return [pieces.Empty]*4 + [pieces.King(common.color.WHITE)] + [pieces.Empty]*3 + [pieces.Empty]*48 + [pieces.Empty]*4 + [pieces.King(common.color.BLACK)] + [pieces.Empty]*3

    @T.let
    def chess_board(self):
        return self.ClearChessBoard()
