import pygame as pg
import helpers
import pieces
from board import Board
import graphics
from King import King

pg.init()
SIZE = (800, 800)
screen = pg.display.set_mode(SIZE)
pg.display.set_caption('CHESS')

done = False
clock = pg.time.Clock()
game_board = Board(0)
selected_square = False
piece = None
legal_moves = []
turn = 'w'
promoting = False
check = False
checkmate = False
timer = 0

while not done:
    # the main game loop is here - this is to be organised and exported to the file controls.py
    if not checkmate:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                coords = helpers.input_to_board(pg.mouse.get_pos())
                if not promoting:
                    if not selected_square:
                        # on a clean board, this logic parses the first input
                        selected_square = coords
                        selected_piece = game_board.get_piece(coords)
                        if not selected_piece:
                            selected_square = False
                        elif selected_piece.colour == turn:
                            legal_moves = [i for i in game_board.legal_moves(selected_piece)]
                            if selected_piece in King.king_instances[0]:
                                King.castles_check(selected_piece, legal_moves, game_board)
                        else:
                            selected_square = False
                    else:
                        # if a piece has been chosen, move it to the selected square if it is a legal move, else reset
                        selected_square = False
                        for move in legal_moves:
                            if coords[0] == move[0] and coords[1] == move[1]:
                                game_board.move_piece(selected_piece, move)
                                if game_board.is_promoting(selected_piece):
                                    promoting = True
                                if turn == 'w':
                                    turn = 'b'
                                else:
                                    turn = 'w'
                                break
                        legal_moves = []
                        # check if the player is now checkmated here
                        for your_pieces in pieces.Pieces.instances[0]:
                            if your_pieces.colour == turn and your_pieces.pos != 'captured':
                                legal_moves += game_board.legal_moves(your_pieces)
                        if game_board.is_in_check(turn) and not legal_moves:
                            checkmate = True
                        legal_moves = []
                else:
                    # promotions are offered to the player in a drop-down menu, similar to the format on chess.com
                    if coords[0] == selected_piece.pos[0] and 1 <= abs(coords[1]-selected_piece.pos[1]) <= 4:
                        game_board.promote(selected_piece, abs(coords[1] - selected_piece.pos[1]))
                        promoting = False
                check = game_board.is_in_check(turn)
    else:
        print(f'CHECKMATE {turn} IS REKT')
        if timer < 200:
            timer += 1
        else:
            done = True

    graphics.checkers(screen)
    # rendering of the board is handled by graphics.py
    if selected_square:
        graphics.render_select(screen, coords)
    for move in legal_moves:
        graphics.render_moves(screen, move)
    if check:
        king = game_board.get_king(turn)
        graphics.render_check(screen, king)
    for piece in pieces.Pieces.instances[0]:
        if piece.pos != 'captured':
            graphics.render_pieces(screen, piece)
    if promoting:
        graphics.render_promoting(screen, selected_piece)
    pg.display.flip()
    # 20 fps finds a balance between performance and responsiveness - with a frame rate of 10 the game can miss inputs
    clock.tick(60)
