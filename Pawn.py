from pieces import Pieces


class Pawn(Pieces):

    pawn_instances = [[], []]
    pawn_move_dict = {'b': 1, 'w': -1}

    def __init__(self, colour, pos, hidden):
        super().__init__(colour, pos, hidden)
        self.cv2_coords = (500, 100*Pieces.colour_to_number[self.colour])
        self.__class__.pawn_instances[hidden].append(self)

    def get_legal_moves(self, game_board):
        legal_moves = []
        pos = [self.pos[0], self.pos[1] + self.pawn_move_dict[self.colour]]
        if game_board.is_square_empty(pos):
            legal_moves.append([pos[0], pos[1]])
            if pos[1] == (7 - (3 * self.pawn_move_dict[self.colour])) // 2 and \
                    game_board.is_square_empty([pos[0], (7 - self.pawn_move_dict[self.colour]) // 2]):
                legal_moves.append([self.pos[0], self.pos[1] + 2 * self.pawn_move_dict[self.colour]])
        for i in [1, -1]:
            pos = [self.pos[0] + i, self.pos[1] + self.pawn_move_dict[self.colour]]
            if 0 <= pos[0] <= 7 and not game_board.is_square_empty(pos) and game_board.is_different_colour(self, pos):
                legal_moves.append(pos)
            if self.pos[1] == (7 + self.pawn_move_dict[self.colour]) / 2:
                if not game_board.is_square_empty([self.pos[0] + i, self.pos[1]]):
                    en_passant_check = game_board.get_piece([self.pos[0] + i, self.pos[1]])
                    if en_passant_check in self.pawn_instances[0] and en_passant_check in game_board.move_history[-1]:
                        if game_board.move_history[-1][1] == [0, (0 - self.pawn_move_dict[self.colour]) * 2]:
                            pos += ['en passant', en_passant_check]
                            legal_moves.append(pos)
        return legal_moves

