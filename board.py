from pieces import Pieces
from Knight import Knight
from Pawn import Pawn
from Rook import Rook
from King import King
from Queen import Queen
from Bishop import Bishop
import pygame as pg

pg.mixer.init()
airhorn = pg.mixer.Sound('airhorn.mp3')


class Board:

    board_history = []
    move_history = []

    def __init__(self, shadow):
        self.shadow = shadow
        self._board = self.array()
        self._board = self.initialise_board(self._board, self.shadow)

    @staticmethod
    def array():
        # this method constructs an 8x8 array for pieces to be placed on
        board = []
        for file in range(8):
            board.append([])
            for rank in range(8):
                board[file].append(None)
        return board

    def initialise_board(self, board, hidden):
        # places pieces on the board - used for both the game and shadow boards
        d = {0: 'b', 1: 'b', 6: 'w', 7: 'w'}
        for c in [0, 7]:
            Knight(d[c], [1, c], hidden)
            Knight(d[c], [6, c], hidden)
            Bishop(d[c], [2, c], hidden)
            Bishop(d[c], [5, c], hidden)
            Rook(d[c], [0, c], hidden)
            Rook(d[c], [7, c], hidden)
            Queen(d[c], [3, c], hidden)
            King(d[c], [4, c], hidden)

        for c in [1, 6]:
            for file in range(8):
                Pawn(d[c], [file, c], hidden)

        for piece in Pieces.instances[hidden]:
            board[piece.pos[0]][piece.pos[1]] = (piece, piece.colour)
        if not hidden:
            self.board_history.append(board)
        return board

    def get_piece(self, coords):
        if self.is_square_empty(coords):
            return False
        return self._board[coords[0]][coords[1]][0]

    def move_piece(self, piece, new_pos):
        colour_dict = {'b': 0, 'w': 7}
        self.move_history.append([piece, [new_pos[0]-piece.pos[0], new_pos[1]-piece.pos[1]]])
        self._board[piece.pos[0]][piece.pos[1]] = None
        if not self.is_square_empty(new_pos):
            self._board[new_pos[0]][new_pos[1]][0].update_pos('captured')
        piece.update_pos(new_pos)
        self._board[piece.pos[0]][piece.pos[1]] = (piece, piece.colour)
        self.board_history.append(self._board)
        if len(new_pos) > 2:
            if new_pos[2] == 'en passant':
                captured = self.get_piece([piece.pos[0], piece.pos[1] - Pawn.pawn_move_dict[piece.colour]])
                self._board[piece.pos[0]][piece.pos[1] - Pawn.pawn_move_dict[piece.colour]] = None
                captured.update_pos('captured')
                if not self.shadow:
                    pg.mixer.Sound.play(airhorn)
            elif new_pos[2] == 'queenside':
                new_pos[3].update_pos([3, colour_dict[piece.colour]])
                self._board[3][colour_dict[piece.colour]] = (new_pos[3], new_pos[3].colour)
            elif new_pos[2] == 'kingside':
                new_pos[3].update_pos([5, colour_dict[piece.colour]])
                self._board[5][colour_dict[piece.colour]] = (new_pos[3], new_pos[3].colour)

    def is_square_empty(self, pos):
        return self._board[pos[0]][pos[1]] is None

    def is_different_colour(self, piece, pos):
        return self._board[pos[0]][pos[1]][1] != piece.colour

    def legal_moves(self, piece):
        legal_moves = piece.get_legal_moves(self)
        for king in King.king_instances[1]:
            if king.colour == piece.colour:
                your_king = king
        not_legal_moves = []
        for move in legal_moves:
            self.set_shadow_board()
            shadow_board.move_piece(shadow_board._board[piece.pos[0]][piece.pos[1]][0], move)
            enemy_moves = []
            for enemy in Pieces.instances[1]:
                if enemy.colour != piece.colour and enemy.pos != 'captured':
                    enemy_moves += shadow_board.get_legal_moves(enemy)
            if your_king.pos in enemy_moves:
                not_legal_moves.append(move)
        for move in not_legal_moves:
            if move in legal_moves:
                legal_moves.remove(move)
        return legal_moves

    def get_legal_moves(self, piece):
        return piece.get_legal_moves(self)

    def return_board_state(self):
        return self._board

    def is_promoting(self, piece):
        if piece in Pawn.pawn_instances[self.shadow]:
            return piece.pos[1] == 7 * (1 + Pawn.pawn_move_dict[piece.colour]//2)
        return False

    def promote(self, piece, promoted_piece):
        pos = piece.pos
        self._board[pos[0]][pos[1]] = None
        # when promoting, the shadow board must also inherit the new piece
        # without doing this, a mismatch is created in Pieces.instances, which causes a crash upon promotion
        # as of now, an engine will not be able to promote on the shadow board - this will be changed when necessary
        match promoted_piece:
            case 1:
                Knight(piece.colour, piece.pos, 0)
                Knight(piece.colour, piece.pos, 1)
            case 2:
                Bishop(piece.colour, piece.pos, 0)
                Bishop(piece.colour, piece.pos, 1)
            case 3:
                Rook(piece.colour, piece.pos, 0)
                Rook(piece.colour, piece.pos, 1)
            case 4:
                Queen(piece.colour, piece.pos, 0)
                Queen(piece.colour, piece.pos, 1)
        for promoted_piece in Pieces.instances[self.shadow]:
            if promoted_piece.pos == pos:
                self._board[pos[0]][pos[1]] = [promoted_piece, promoted_piece.colour]
        piece.update_pos('captured')

    def set_shadow_board(self):
        # the shadow board can be freely changed without altering the game board
        # this has two purposes - testing if a move will place your king in check, and allowing the engine to calculate
        Pieces.assimilate_positions(Pieces)
        shadow_board._board = self.array()
        for piece in Pieces.instances[1]:
            if piece.pos != 'captured':
                shadow_board._board[piece.pos[0]][piece.pos[1]] = (piece, piece.colour)

    def is_in_check(self, colour):
        for king in King.king_instances[0]:
            if king.colour == colour:
                your_king = king
        enemy_moves = []
        for enemy in Pieces.instances[0]:
            if enemy.colour != colour and enemy.pos != 'captured':
                enemy_moves += self.get_legal_moves(enemy)
        if your_king.pos in enemy_moves:
            return True
        return False

    def is_square_in_check(self, pos, colour):
        enemy_moves = []
        for enemy in Pieces.instances[0]:
            if enemy.colour != colour and enemy.pos != 'captured':
                enemy_moves += self.get_legal_moves(enemy)
        if pos in enemy_moves:
            return True
        return False

    def get_king(self, colour):
        for king in King.king_instances[0]:
            if king.colour == colour:
                return king


shadow_board = Board(1)
