import pygame as pg

# establish the colours used
DARK_SQUARES = (118, 150, 86)
LIGHT_SQUARES = (238, 238, 210)
MOVE_SQUARES = (186, 202, 68)
CHECK_SQUARES = (255, 0, 0)
WHITE = (255, 255, 255)
# using pygame subsurfaces and manually scaling the image proved simpler than using cv2 in this case
pieces_image = pg.image.load('lichesspieces2.png')

# the rendering uses the 800*800 coordinate system to display objects


def checkers(screen):
    screen.fill(LIGHT_SQUARES)
    for x in range(4):
        for y in range(4):
            pg.draw.rect(screen, DARK_SQUARES, [200 * x + 100, 200 * y, 100, 100], 0)
            pg.draw.rect(screen, DARK_SQUARES, [200 * x, 200 * y + 100, 100, 100], 0)


def render_select(screen, coords):
    pg.draw.rect(screen, MOVE_SQUARES, [coords[0]*100, coords[1]*100, 100, 100])


def render_moves(screen, move):
    pg.draw.circle(screen, MOVE_SQUARES, (move[0] * 100 + 50, move[1] * 100 + 50), 25)


def render_pieces(screen, piece):
    # pieces are assigned a pair of coordinates called cv2_coords
    # this instructs python how to slice the image 'lichesspieces2.png' to display the correct piece
    surface = pieces_image.subsurface(piece.cv2_coords[0], piece.cv2_coords[1], 100, 100)
    screen.blit(surface, (1+piece.pos[0] * 100, piece.pos[1] * 100))


def render_promoting(screen, piece):
    match piece.colour:
        case 'w':
            pg.draw.rect(screen, WHITE, [piece.pos[0]*100, 100, 100, 400])
            screen.blit(pieces_image.subsurface(300, 0, 100, 100), (piece.pos[0] * 100, 100))
            screen.blit(pieces_image.subsurface(200, 0, 100, 100), (piece.pos[0] * 100, 200))
            screen.blit(pieces_image.subsurface(400, 0, 100, 100), (piece.pos[0] * 100, 300))
            screen.blit(pieces_image.subsurface(100, 0, 100, 100), (piece.pos[0] * 100, 400))
        case 'b':
            pg.draw.rect(screen, WHITE, [piece.pos[0] * 100, 300, 100, 400])
            screen.blit(pieces_image.subsurface(300, 100, 100, 100), (piece.pos[0] * 100, 600))
            screen.blit(pieces_image.subsurface(200, 100, 100, 100), (piece.pos[0] * 100, 500))
            screen.blit(pieces_image.subsurface(400, 100, 100, 100), (piece.pos[0] * 100, 400))
            screen.blit(pieces_image.subsurface(100, 100, 100, 100), (piece.pos[0] * 100, 300))


def render_check(screen, king):
    pg.draw.rect(screen, CHECK_SQUARES, [king.pos[0] * 100, king.pos[1] * 100, 100, 100])

