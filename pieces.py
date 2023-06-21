class Pieces:

    instances = [[], []]

    colour_to_number = {'w': 0, 'b': 1}

    def __init__(self, colour, pos, hidden):
        self.colour = colour
        self.pos = pos
        self.__class__.instances[hidden].append(self)

    def update_pos(self, new_pos):
        self.pos = new_pos

    def get_legal_moves(self, game_board):
        pass

    def assimilate_positions(self):
        for i in self.instances[0]:
            self.instances[1][self.instances[0].index(i)].pos = i.pos

