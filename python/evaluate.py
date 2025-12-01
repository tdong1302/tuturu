import chess
import chess

PAWN_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

PAWN_ENDGAME_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    0, 0, 0, 0, 0, 0, 0, 0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,   0,  5,  5,  5,  5,  0, -5,
     0,   0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_START = [
    -80, -70, -70, -70, -70, -70, -70, -80,
    -60, -60, -60, -60, -60, -60, -60, -60,
    -40, -50, -50, -60, -60, -50, -50, -40,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,  -5,  -5,  -5,  -5,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

KING_END = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -5,   0,   5,   5,   5,   5,   0,  -5,
    -10, -5,  20,  30,  30,  20,  -5, -10,
    -15, -10, 35,  45,  45,  35, -10, -15,
    -20, -15, 30,  40,  40,  30, -15, -20,
    -25, -20, 20,  25,  25,  20, -20, -25,
    -30, -25,  0,   0,   0,   0, -25, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

piece_square_tables = {
    chess.PAWN: (PAWN_TABLE, PAWN_ENDGAME_TABLE),
    chess.KNIGHT: (KNIGHT_TABLE, KNIGHT_TABLE),
    chess.BISHOP: (BISHOP_TABLE, BISHOP_TABLE),
    chess.ROOK: (ROOK_TABLE, ROOK_TABLE),
    chess.QUEEN: (QUEEN_TABLE, QUEEN_TABLE),
    chess.KING: (KING_START, KING_END)
}

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

def get_material_info(board, color):
    pieces = board.piece_map()
    value = 0
    num = {pt: 0 for pt in piece_values}
    for sq, pc in pieces.items():
        if pc.color == color:
            num[pc.piece_type] += 1
            value += piece_values[pc.piece_type]
    endgame_score = (
        num[chess.QUEEN] * 45 + num[chess.ROOK] * 20 +
        num[chess.BISHOP] * 10 + num[chess.KNIGHT] * 10
    )
    endgame_weight = max(0, 1 - endgame_score / 152)
    return value, endgame_weight, num

def evaluate_piece_square(board, color, endgame_t):
    value = 0
    for sq in chess.SQUARES:
        pc = board.piece_at(sq)
        if pc and pc.color == color:
            t_early, t_end = piece_square_tables[pc.piece_type]
            table_val = t_early[sq] * (1 - endgame_t) + t_end[sq] * endgame_t
            value += table_val
    return value

def evaluate_board(board):
    if board.is_checkmate():
        return -999999 if board.turn == chess.WHITE else 999999

    white_mat, white_end, white_count = get_material_info(board, chess.WHITE)
    black_mat, black_end, black_count = get_material_info(board, chess.BLACK)

    white_score = white_mat
    black_score = black_mat

    white_score += evaluate_piece_square(board, chess.WHITE, white_end)
    black_score += evaluate_piece_square(board, chess.BLACK, black_end)

    eval_score = white_score - black_score
    return eval_score if board.turn == chess.WHITE else -eval_score
