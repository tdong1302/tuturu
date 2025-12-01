import pygame
import chess
import os

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
big_font = None
small_font = None

BASE_DIR = os.path.dirname(__file__)
PIECE_IMAGES = {}

PIECE_IMAGES = {}
PIECES = ['p', 'r', 'n', 'b', 'q', 'k', 'p1', 'r1', 'n1', 'b1', 'q1', 'k1']
for piece in PIECES:
    try:
        path = os.path.join(BASE_DIR, 'assets', f'{piece}.png')
        PIECE_IMAGES[piece] = pygame.image.load(path)
        PIECE_IMAGES[piece] = pygame.transform.scale(PIECE_IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))
    except pygame.error:
        print(f"Could not load image for piece {piece}")

def draw_board(screen, flip=False, last_move_from=None, last_move_to=None):
    font = pygame.font.SysFont(None, 30)
    BAR_WIDTH = 30
    BAR_HEIGHT = 30
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, BAR_WIDTH, HEIGHT + BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, HEIGHT, WIDTH + BAR_WIDTH, BAR_HEIGHT))

    for row in range(8):
        for col in range(8):
            r = 7 - row if flip else row
            c = 7 - col if flip else col
            color = WHITE if (r + c) % 2 == 0 else BROWN
            if last_move_from is not None:
                from_rank = chess.square_rank(last_move_from)
                from_file = chess.square_file(last_move_from)
                from_row = 7 - from_rank if not flip else from_rank
                from_col = from_file if not flip else 7 - from_file
                if row == from_row and col == from_col:
                    color = "#ADD8E6"
            if last_move_to is not None:
                to_rank = chess.square_rank(last_move_to)
                to_file = chess.square_file(last_move_to)
                to_row = 7 - to_rank if not flip else to_rank
                to_col = to_file if not flip else 7 - to_file
                if row == to_row and col == to_col:
                    color = "#ADD8E6"
            pygame.draw.rect(screen, color, pygame.Rect(BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for row in range(8):
        display_rank = 8 - row if not flip else row + 1
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        rank = str(display_rank)
        text = font.render(rank, True, (255, 0, 0))
        screen.blit(text, (BAR_WIDTH // 2 - text.get_width() // 2, y - text.get_height() // 2))
    for col in range(8):
        display_file = col if not flip else 7 - col
        x = BAR_WIDTH + col * SQUARE_SIZE + SQUARE_SIZE // 2
        file = chr(ord('a') + display_file)
        text = font.render(file, True, (255, 0, 0))
        screen.blit(text, (x - text.get_width() // 2, HEIGHT + BAR_HEIGHT // 2 - text.get_height() // 2))

def draw_pieces(screen, board, flip=False, animating=False, anim_piece=None, anim_pos=None):
    BAR_WIDTH = 30
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and (not animating or piece != anim_piece):
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            row = 7 - rank if not flip else rank
            col = file if not flip else 7 - file
            symbol = piece.symbol()
            key = symbol.lower() if piece.color == chess.BLACK else symbol.lower() + "1"
            if key in PIECE_IMAGES:
                screen.blit(PIECE_IMAGES[key], (BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE))
    if animating and anim_piece and anim_pos:
        symbol = anim_piece.symbol()
        key = symbol.lower() if anim_piece.color == chess.BLACK else symbol.lower() + "1"
        if key in PIECE_IMAGES:
            screen.blit(PIECE_IMAGES[key], anim_pos)

def highlight_moves(screen, board, from_square, flip=False):
    BAR_WIDTH = 30
    overlay_color = (144, 238, 144, 100)
    overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill(overlay_color)
    for move in board.legal_moves:
        if move.from_square == from_square:
            to_rank = chess.square_rank(move.to_square)
            to_file = chess.square_file(move.to_square)
            row = 7 - to_rank if not flip else to_rank
            col = to_file if not flip else 7 - to_file
            screen.blit(overlay, (BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_promotion_choices(screen, color):
    BAR_WIDTH = 30
    options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    names = ['q', 'r', 'b', 'n']
    if color == chess.WHITE:
        names = [n + '1' for n in names]
    center_x = BAR_WIDTH + 300
    center_y = 300
    for i, name in enumerate(names):
        rect = pygame.Rect(center_x - 150 + i * 75, center_y - 75, 75, 75)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        screen.blit(PIECE_IMAGES[name], (center_x - 150 + i * 75, center_y - 75))

def draw_game_over(screen, board, big_font, small_font):
    BAR_WIDTH = 30
    BAR_HEIGHT = 30
    outcome = board.outcome()
    if outcome is None:
        return
    if outcome.winner is None:
        result_text = "Draw!"
        image_path = "assets/draw.png"
    elif outcome.winner:
        result_text = "White wins!"
        image_path = "assets/win.png"
    else:
        result_text = "Black wins!"
        image_path = "assets/loss.png"
    overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + BAR_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    try:
        result_image = pygame.image.load(image_path).convert_alpha()
        result_image = pygame.transform.scale(result_image, (150, 150))
        image_rect = result_image.get_rect(center=((WIDTH + BAR_WIDTH) // 2, HEIGHT // 2 - 120))
        screen.blit(result_image, image_rect)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    text_surface = big_font.render(result_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((WIDTH + BAR_WIDTH) // 2, HEIGHT // 2 + 10))
    screen.blit(text_surface, text_rect)
    button_rect = pygame.Rect((WIDTH + BAR_WIDTH) // 2 - 80, HEIGHT // 2 + 70, 160, 50)
    pygame.draw.rect(screen, (70, 130, 180), button_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=10)
    button_text = small_font.render("Play again", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    return button_rect

def get_promotion_choice(pos, color):
    BAR_WIDTH = 30
    x, y = pos
    center_x = BAR_WIDTH + 300
    center_y = 300
    if center_y - 75 <= y <= center_y and center_x - 150 <= x <= center_x + 150:
        index = (x - (center_x - 150)) // 75
        options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        return options[index]
    return None