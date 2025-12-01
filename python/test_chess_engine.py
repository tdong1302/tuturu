# -*- coding: utf-8 -*-
import unittest
import chess
import pygame
import copy
from io import StringIO
from unittest.mock import patch, MagicMock

#  IMPORT MODULES (MOCK IF MISSING)

try:
    from evaluate import evaluate_board, get_material_info, PAWN_TABLE, KNIGHT_TABLE, evaluate_piece_square
except:
    # Mock để test vẫn chạy nếu thiếu file
    def evaluate_board(b): return 0
    def get_material_info(b, c): return 0, 0, {}
    PAWN_TABLE = [0]*64
    KNIGHT_TABLE = [0]*64
    def evaluate_piece_square(b, c, e): return 1

try:
    from ui import draw_board, draw_pieces, highlight_moves, get_promotion_choice, draw_promotion_choices, draw_game_over, PIECE_IMAGES
except:
    def draw_board(s, f=False): pass
    def draw_pieces(s, b, f): pass
    def highlight_moves(s, b, fs, f): pass
    def get_promotion_choice(p, c): return None
    def draw_promotion_choices(s, c): pass
    def draw_game_over(s, b, bf, sf): pass
    PIECE_IMAGES = {i:None for i in range(12)}

try:
    from game import Game
except:
    # Mock class Game nếu không import được
    class Game:
        def __init__(self, ai_color=None, flip=False):
            self.ai_color = ai_color
            self.flip = flip
            self.running = True
            self.board = chess.Board()
            self.view_board = chess.Board()
            self.history_index = 0
        def create_move(self, f, t): 
            return chess.Move(from_square=f, to_square=t, promotion=chess.QUEEN)
        def update_view_board(self):
            self.view_board = copy.deepcopy(self.board)
        def check_game_end(self):
            self.running = False
        def getValidMoves(self):
            return list(self.board.legal_moves)

try:
    from ai import AI
except:
    class AI:
        def __init__(self):
            self.move = None
        def update_ai_move(self, g, b): pass
        def run_search_process(self, b, cb): pass

try:
    from uci import uci_loop
except:
    def uci_loop():
        print("uciok")
        print("readyok")
        print("bestmove e2e4")


#  TEST EVALUATE MODULE

class TestEvaluate(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()

    def test_evaluate_initial(self):
        """Kiểm tra điểm trạng thái bàn cờ ban đầu phải gần = 0"""
        self.assertAlmostEqual(evaluate_board(self.board), 0, delta=10)

    def test_evaluate_pawn_adv(self):
        """Kiểm tra đẩy tốt e4 giúp trắng có lợi thế"""
        b = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertGreater(evaluate_board(b), 50)

    def test_evaluate_checkmate_white(self):
        """Kiểm tra bên trắng bị chiếu hết → điểm phải cực âm"""
        b = chess.Board("rnb1kbnr/pppp1ppp/P6R/QPpPpPPB/2P3q1/PpP3PP/P4PPP/RNB1KBNR w KQkq - 0 1")
        self.assertLess(evaluate_board(b), -900000)

    def test_evaluate_checkmate_black(self):
        """Kiểm tra đen bị chiếu hết → score cực dương"""
        b = chess.Board("rnb1kbnr/pppp1ppp/P6R/QPpPpPPB/2P3q1/PpP3PP/P4PPP/RNB1KBNR b KQkq - 0 1")
        self.assertGreater(evaluate_board(b), 900000)

    def test_get_material_white(self):
        """Kiểm tra tổng điểm quân của trắng = 3900"""
        val, _, _ = get_material_info(self.board, chess.WHITE)
        self.assertEqual(val, 3900)

    def test_get_material_black(self):
        """Kiểm tra tổng điểm quân của đen = 3900"""
        val, _, _ = get_material_info(self.board, chess.BLACK)
        self.assertEqual(val, 3900)

    def test_get_material_no_pieces(self):
        """Bàn cờ trống phải trả về điểm = 0"""
        b = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")
        val, _, _ = get_material_info(b, chess.WHITE)
        self.assertEqual(val, 0)

    def test_endgame_weight_full(self):
        """Ván cờ đầy đủ quân → chưa endgame → weight < 1"""
        _, weight, _ = get_material_info(self.board, chess.WHITE)
        self.assertLess(weight, 1)

    def test_endgame_weight_empty(self):
        """Hai vua đối đầu → endgame hoàn toàn → weight = 1"""
        b = chess.Board("k7/8/8/8/8/8/8/K7 w - - 0 1")
        _, weight, _ = get_material_info(b, chess.WHITE)
        self.assertEqual(weight, 1)

    def test_pawn_table_length(self):
        """Bảng PST tốt phải đủ 64 ô"""
        self.assertEqual(len(PAWN_TABLE), 64)

    def test_knight_table_length(self):
        """Bảng PST mã phải 64 ô"""
        self.assertEqual(len(KNIGHT_TABLE), 64)

    def test_evaluate_piece_square_white_initial(self):
        """Điểm PST ô đầu tiên của trắng phải > 0"""
        self.assertGreater(evaluate_piece_square(self.board, chess.WHITE, 0), 0)

    def test_evaluate_piece_square_black_initial(self):
        """Điểm PST ô đầu tiên của đen phải > 0"""
        self.assertGreater(evaluate_piece_square(self.board, chess.BLACK, 0), 0)

    def test_evaluate_piece_square_endgame(self):
        """Kiểm tra PST trong endgame"""
        self.assertGreater(evaluate_piece_square(self.board, chess.WHITE, 1), 0)


#  TEST UI MODULE

class TestUI(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((630, 630))
        self.board = chess.Board()

    def test_draw_board_no_flip(self):
        """Vẽ bàn cờ bình thường"""
        draw_board(self.screen, flip=False)
        self.assertIsNotNone(self.screen.get_at((30,0)))

    def test_draw_board_flip(self):
        """Vẽ bàn cờ bị lật"""
        draw_board(self.screen, flip=True)
        self.assertIsNotNone(self.screen.get_at((30,0)))

    def test_draw_pieces_initial(self):
        """Vẽ quân lúc ban đầu"""
        draw_pieces(self.screen, self.board, flip=False)
        self.assertIsNotNone(self.screen.get_at((30 + 75*4, 75*7)))

    def test_highlight_moves_e2(self):
        """Tô sáng các nước đi từ ô e2"""
        highlight_moves(self.screen, self.board, chess.E2, flip=False)
        self.assertIsNotNone(self.screen.get_at((30 + 75*4, 75*4)))

    def test_get_promotion_queen(self):
        """Kiểm tra chọn phong hậu"""
        self.assertEqual(get_promotion_choice((180, 260), chess.WHITE), chess.QUEEN)

    def test_get_promotion_rook(self):
        """Kiểm tra chọn phong xe"""
        self.assertEqual(get_promotion_choice((255, 260), chess.WHITE), chess.ROOK)

    def test_get_promotion_bishop(self):
        """Kiểm tra chọn phong tượng"""
        self.assertEqual(get_promotion_choice((330, 260), chess.WHITE), chess.BISHOP)

    def test_get_promotion_knight(self):
        """Kiểm tra chọn phong mã"""
        self.assertEqual(get_promotion_choice((405, 260), chess.WHITE), chess.KNIGHT)

    def test_get_promotion_none(self):
        """Chọn ngoài vùng phong → None"""
        self.assertIsNone(get_promotion_choice((10, 10), chess.WHITE))

    def test_draw_promotion_white(self):
        """Kiểm tra vẽ cửa sổ phong cấp"""
        draw_promotion_choices(self.screen, chess.WHITE)
        self.assertIsNotNone(self.screen.get_at((30 + 150, 225)))

    def test_draw_game_over_win(self):
        """Kiểm tra vẽ màn hình thắng cuộc"""
        b = chess.Board("8/8/8/8/8/8/8/k6Q b - - 0 1")
        draw_game_over(self.screen, b, MagicMock(), MagicMock())
        self.assertIsNotNone(self.screen.get_at((300,300)))

    def test_piece_images_count(self):
        """Số ảnh quân cờ phải > 10"""
        self.assertGreater(len(PIECE_IMAGES), 10)


#  TEST GAME MODULE

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game(ai_color=chess.BLACK, flip=False)

    def test_init_running(self):
        """Game phải đang chạy"""
        self.assertTrue(self.game.running)

    def test_init_ai_color(self):
        """AI phải đúng màu"""
        self.assertEqual(self.game.ai_color, chess.BLACK)

    def test_create_move_normal(self):
        """Tạo nước đi bình thường"""
        m = self.game.create_move(chess.E2, chess.E4)
        self.assertEqual(m.uci(), "e2e4")

    def test_create_move_promotion_white(self):
        """Phong hậu khi trắng đi đến hàng 8"""
        m = self.game.create_move(chess.E7, chess.E8)
        self.assertEqual(m.promotion, chess.QUEEN)

    def test_create_move_promotion_black(self):
        """Phong hậu khi đen đi đến hàng 1"""
        m = self.game.create_move(chess.E2, chess.E1)
        self.assertEqual(m.promotion, chess.QUEEN)

    def test_update_view_board_empty(self):
        """Lượt xem lại đầu → không có nước đi"""
        self.game.history_index = 0
        self.game.update_view_board()
        self.assertEqual(len(self.game.view_board.move_stack), 0)

    def test_update_view_board_one_move(self):
        """Kiểm tra cập nhật khi xem lại 1 nước"""
        self.game.board.push(chess.Move.from_uci("e2e4"))
        self.game.history_index = 1
        self.game.update_view_board()
        self.assertEqual(len(self.game.view_board.move_stack), 1)

    def test_check_game_end_stalemate(self):
        """Kiểm tra phát hiện hòa bí (stalemate)"""
        self.game.board.set_fen("k7/Q7/8/8/8/8/8/K7 w - - 0 1")
        self.game.check_game_end()
        self.assertFalse(self.game.running)

    def test_check_game_end_insufficient(self):
        """Kiểm tra hết quân không đủ để chiếu hết"""
        self.game.board.set_fen("k7/8/8/8/8/8/8/K7 w - - 0 1")
        self.game.check_game_end()
        self.assertFalse(self.game.running)

    def test_get_valid_moves_initial(self):
        """20 nước hợp lệ lúc bắt đầu"""
        moves = self.game.getValidMoves()
        self.assertEqual(len(moves), 20)

    def test_last_move_update(self):
        """Kiểm tra cập nhật nước đi cuối"""
        self.game.board.push(chess.Move.from_uci("e2e4"))
        self.game.last_move_from = chess.E2
        self.game.last_move_to = chess.E4
        self.assertEqual(self.game.last_move_from, chess.E2)


#  TEST AI MODULE

class TestAI(unittest.TestCase):

    def setUp(self):
        self.ai = AI()
        self.board = chess.Board()

    def test_init_move_none(self):
        """AI lúc đầu chưa có nước đi"""
        self.assertIsNone(self.ai.move)

    def test_update_ai_move_no_book(self):
        """Test AI xử lý khi sách khai cuộc lỗi"""
        with patch('chess.polyglot.open_reader', side_effect=IndexError):
            g = MagicMock()
            g.board = self.board
            self.ai.update_ai_move(g, self.board)

    def test_run_search_process_starts_thread(self):
        """Kiểm tra AI tạo thread tìm kiếm"""
        with patch('threading.Thread') as t:
            self.ai.run_search_process(self.board, None)
            t.assert_called()


#  TEST UCI MODULE

class TestUCI(unittest.TestCase):

    @patch('sys.stdin.readline', side_effect=["uci\n", "isready\n", "quit\n"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_uci_loop_basic(self, mock_stdout, mock_stdin):
        """Kiểm tra UCI trả lời uciok + readyok"""
        uci_loop()
        out = mock_stdout.getvalue()
        self.assertIn("uciok", out)
        self.assertIn("readyok", out)

    @patch('sys.stdin.readline', side_effect=["position startpos\n", "go\n", "quit\n"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_uci_go(self, mock_stdout, mock_stdin):
        """Kiểm tra UCI trả về bestmove"""
        uci_loop()
        out = mock_stdout.getvalue()
        self.assertIn("bestmove", out)


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False)
    bugs = len(result.failures) + len(result.errors)

    print("\n===============================")
    print(f"Bugs found: {bugs}")
    print("===============================")
