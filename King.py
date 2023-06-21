from pieces import Pieces
from Rook import Rook


class King(Pieces):

    king_instances = [[], []]
    queen_move_dict = {0: [1, 0], 1: [1, 1], 2: [0, 1], 3: [-1, 1], 4: [-1, 0], 5: [-1, -1], 6: [0, -1], 7: [1, -1]}
    colour_dict = {'b': 0, 'w': 7}

    def __init__(self, colour, pos, hidden):
        super().__init__(colour, pos, hidden)
        self.cv2_coords = (0, 100*Pieces.colour_to_number[self.colour])
        self.__class__.king_instances[hidden].append(self)

    def get_legal_moves(self, game_board):
        legal_moves = []
        for i in range(8):
            pos = [self.queen_move_dict[i][0] + self.pos[0], self.queen_move_dict[i][1] + self.pos[1]]
            if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
                if game_board.is_square_empty(pos):
                    legal_moves.append(pos)
                elif game_board.is_different_colour(self, pos):
                    legal_moves.append(pos)
        return legal_moves

    def castles_check(self, legal_moves, game_board):
        # a primary function of get_legal_moves is to check which squares a piece is attacking
        # the king cannot castle into an occupied square so the castles check is excluded from get_legal_moves to
        # \prevent a recursion (castles_check calls is_in_check which then calls get_legal_moves)
        if not game_board.is_in_check(self.colour) and self not in game_board.move_history:
            for rook in Rook.rook_instances[0]:
                if rook.colour == self.colour and rook not in game_board.move_history:
                    if rook.pos[0] == 0:
                        can_castle = True
                        for i in range(1, 4):
                            pos = [i + rook.pos[0], self.colour_dict[self.colour]]
                            if not game_board.is_square_empty(pos):
                                can_castle = False
                                break
                            if i > 1 and game_board.is_square_in_check(pos, self.colour):
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.append([2, self.colour_dict[self.colour], 'queenside', rook])
                    else:
                        can_castle = True
                        for i in range(1, 3):
                            pos = [i + self.pos[0], self.colour_dict[self.colour]]
                            if game_board.is_square_in_check(pos, self.colour) or not game_board.is_square_empty(pos):
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.append([6, self.colour_dict[self.colour], 'kingside', rook])
        # kingside and queenside castles are somewhat distinct. if this were a chess 960 program this could probably
        # \be generalised
        # as it is not i have simply hardcoded them instead
        return legal_moves

