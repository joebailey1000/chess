from pieces import Pieces


class Knight(Pieces):

    knight_instances = [[], []]
    knight_move_dict = {0: [2, 1], 1: [2, -1], 2: [-2, 1], 3: [-2, -1], 4: [1, 2], 5: [1, -2], 6: [-1, 2], 7: [-1, -2]}

    def __init__(self, colour, pos, hidden):
        super().__init__(colour, pos, hidden)
        self.cv2_coords = (300, 100*Pieces.colour_to_number[self.colour])
        self.__class__.knight_instances[hidden].append(self)

    def get_legal_moves(self, game_board):
        legal_moves = []
        for i in range(8):
            pos = [self.knight_move_dict[i][0] + self.pos[0],
                   self.knight_move_dict[i][1] + self.pos[1]]
            if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
                if game_board.is_square_empty(pos):
                    legal_moves.append(pos)
                elif game_board.is_different_colour(self, pos):
                    legal_moves.append(pos)
        return legal_moves
