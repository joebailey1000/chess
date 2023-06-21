from pieces import Pieces


class Queen(Pieces):

    queen_instances = [[], []]
    queen_move_dict = {0: [1, 0], 1: [1, 1], 2: [0, 1], 3: [-1, 1], 4: [-1, 0], 5: [-1, -1], 6: [0, -1], 7: [1, -1]}

    def __init__(self, colour, pos, hidden):
        super().__init__(colour, pos, hidden)
        self.cv2_coords = (100, 100*Pieces.colour_to_number[self.colour])
        self.__class__.queen_instances[hidden].append(self)

    def get_legal_moves(self, game_board):
        legal_moves = []
        for i in range(8):
            for j in range(1, 8):
                pos = [self.queen_move_dict[i][0] * j + self.pos[0],
                       self.queen_move_dict[i][1] * j + self.pos[1]]
                if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                    break
                elif game_board.is_square_empty(pos):
                    legal_moves.append(pos)
                else:
                    if game_board.is_different_colour(self, pos):
                        legal_moves.append(pos)
                    break
        return legal_moves
