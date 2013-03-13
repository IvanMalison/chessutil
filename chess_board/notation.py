from . import common
from . import rules
from .board import BasicChessBoard


class ChessNotationProcessor(object):

	@classmethod
	def file_to_index(cls, file_char):
		return ord(file_char) - 97

	@classmethod
	def rank_to_index(cls, rank):
		return rank - 1

	@classmethod
	def square_name_to_indices(cls, square_name):
		file_char, rank_char = square_name
		return cls.rank_to_index(int(rank_char)), cls.file_to_index(file_char)

	def __init__(self, board=None):
		if board == None:
			board = BasicChessBoard()
		self._board = board
		self._rules = rules.ChessRules(self._board)
		self._piece_char_to_function_map = {
			'K': self._parse_king_move,
			'Q': self._parse_queen_move,
			'R': self._parse_rook_move,
			'B': self._parse_bishop_move,
			'N': self._parse_knight_move,
		}

	def make_move_with_uci_notation(self, move):
		return self.make_move_with_square_names(move[:2], move[2:])

	def make_move_with_square_names(self, source, dest):
		return self.make_move(
			self.square_name_to_indices(source),
			self.square_name_to_indices(dest)
		)

	def parse_algebraic_move(self, algebraic_move):
		algebraic_move = algebraic_move.strip(' \n+')

		# Handle Castling
		if algebraic_move == "O-O":
			if self._board.action == common.WHITE:
				return ((0, 4), (0, 6))
			else:
				return ((7, 4), (7, 6))

		if algebraic_move == "O-O-O":
			if self._board.action == common.WHITE:
				return ((4, 0), (2, 0))
			else:
				return ((4, 7), (2, 7))

		if algebraic_move[0].islower():
			return self._parse_pawn_move(algebraic_move)
		else:
			piece_type = algebraic_move[0]
			disambiguation = algebraic_move[1:-2]
			disambiguation.strip('x')
			destination = self.square_name_to_indices(algebraic_move[-2:])
			if disambiguation:
				pass
			else:
				return self._piece_char_to_function_map[piece_type](destination)

	def _parse_king_move(self, destination):
		return (self.get_king_postion_for_color(), destination)

	def _parse_queen_move(self, destination, disambiguation=None):
		pass

	def _parse_rook_move(self, destination, disambiguation=None):
		pass

	def _parse_bishop_move(self, destination, disambiguation=None):
		pass

	def _parse_knight_move(self, destination, disambiguation=None):
		pass

	def _parse_pawn_move(self, algebraic_move):
        # Clean up the textmove
		"".join(algebraic_move.split("e.p."))

		if '=' in algebraic_move:
			return None

		destination = self.square_name_to_indices(algebraic_move[-2:])
		disambiguation = algebraic_move[:-2]
		if disambiguation:
			source = (destination[0] - 1, self.file_to_index(disambiguation[0]))
		elif destination[0] == 3 and not self._board.get_piece(2, destination[1]):
			source = (1, destination[1])
		else:
			source = (destination[0] - 1, destination[1])

		return (source, destination)
