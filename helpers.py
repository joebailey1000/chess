from math import floor

d2 = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
inv_d2 = {v: k for k, v in d2.items()}


def coordinate_helper(coords):
    # input coordinates in algebraic notation as a string e.g. 'f4' or 'g6'
    return [d2[coords[0]], 8 - int(coords[1])]


def input_to_algebraic(coords):
    """converts the pg.mouse.get_pos() input to algebraic notation"""
    coords = [floor(x / 100) for x in coords]
    return inv_d2[coords[0]] + str(8 - coords[1])


def input_to_board(coords):
    # converts the pg.mouse.get_pos() input to the coordinate system used for the board in board.py
    coords = [floor(x / 100) for x in coords]
    return coords
