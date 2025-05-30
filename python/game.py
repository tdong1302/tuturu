import pygame
import chess
import copy
from ai import AI

class Game:
    def __init__(self, ai_color=chess.BLACK, flip=False):  
        self.board = chess.Board()
        self.view_board = self.board.copy()
        self.history_index = 0
        self.selected_square = None
        self.ai_thinking = False
        self.ai_color = ai_color
        self.ai_move_time = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.ai = AI()
        self.flip = flip  # Thêm biến flip để xác định hướng bàn cờ
        self.last_move_from = None # Lưu vị trí quân cờ đã đi
        self.last_move_to = None # Lưu vị trí quân cờ đã đi
        print(f"[Debug] Game started. AI chơi màu {'Trắng' if self.ai_color == chess.WHITE else 'Đen'}")


    def handle_event(self, event):
        if not self.running:
            return  
        if event.type == pygame.MOUSEBUTTONDOWN and not self.ai_thinking:
            x, y = pygame.mouse.get_pos()
            col, row = x // 75, y // 75
            if self.flip:
                col = 7 - col
                row = 7 - row
            square = chess.square(col, 7 - row)

            if self.selected_square is None:
                if self.board.piece_at(square) and self.board.color_at(square) == self.board.turn:
                    self.selected_square = square
            else:
                move = self.create_move(self.selected_square, square)
                if move in self.board.legal_moves:
                    self.last_move_from = move.from_square
                    self.last_move_to = move.to_square
                    self.board.push(move)
                    self.history_index = len(self.board.move_stack)
                    self.view_board = self.board.copy()  
                    self.check_game_end()
                    if self.board.turn == self.ai_color and not self.ai_thinking:
                        self.ai_thinking = True
                        self.ai_move_time = pygame.time.get_ticks()
                self.selected_square = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.history_index = max(0, self.history_index - 1)
                self.update_view_board()
            elif event.key == pygame.K_RIGHT:
                self.history_index = min(len(self.board.move_stack), self.history_index + 1)
                self.update_view_board()

    def update_view_board(self):
        """Cập nhật view_board dựa trên history_index"""
        self.view_board = chess.Board()
        for move in self.board.move_stack[:self.history_index]:
            self.view_board.push(move)

    def create_move(self, from_sq, to_sq):
        piece = self.board.piece_at(from_sq)
        if piece and piece.piece_type == chess.PAWN:
            rank = chess.square_rank(to_sq)
            if (piece.color == chess.WHITE and rank == 7) or (piece.color == chess.BLACK and rank == 0):
                return chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
        return chess.Move(from_sq, to_sq)

    def update_ai_move(self):
        if self.running and self.board.turn == self.ai_color and self.ai_thinking and pygame.time.get_ticks() - self.ai_move_time >= 1000:
            board_copy = copy.deepcopy(self.board)
            self.ai.update_ai_move(self, board_copy)
            self.view_board = self.board.copy()  
            self.ai_thinking = False

            if self.board.move_stack:
                last_move = self.board.move_stack[-1]
                self.last_move_from = last_move.from_square
                self.last_move_to = last_move.to_square


    def check_game_end(self):
        if self.board.is_checkmate():
            print("Chiếu hết!")
            self.running = False
        elif self.board.is_stalemate():
            print("Hết nước đi (Stalemate)!")
            self.running = False
        elif self.board.is_insufficient_material():
            print("Hòa vì thiếu quân!")
            self.running = False
        elif self.board.is_seventyfive_moves():
            print("Hòa do 75 nước không ăn quân hoặc đi tốt!")
            self.running = False
        elif self.board.can_claim_threefold_repetition():
            print("Hòa do lặp lại vị trí!")
            self.running = False

    def getValidMoves(self):
        return [move for move in self.board.legal_moves]