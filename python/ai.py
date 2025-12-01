def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        print(text.encode("utf-8", errors="replace").decode("utf-8"))

import chess
import time
import chess.polyglot
from threading import Thread
from queue import Queue
from searcher import Searcher  
class AI:
    def __init__(self):
        self.move = None

    def run_search_process(self, board_state, return_queue):
            def search_and_update():
                try:
                    start = time.time()

                    # ⚡ Ưu tiên tìm trong sách khai cuộc trước
                    move = None
                    try:
                        with chess.polyglot.open_reader("baron30.bin") as reader:
                            try:
                                entry = reader.find(board_state)
                                move = entry.move
                                safe_print(f"[AI] Sử dụng sách khai cuộc: {move}")
                            except IndexError:
                                pass
                    except FileNotFoundError:
                        safe_print("[Lỗi] Không tìm thấy baron30.bin")
                    if move is None:
                        searcher = Searcher()
                        move = searcher.iterative_deepening(board_state, max_depth=7, time_limit=9)
                        safe_print("Current turn:", "White" if board_state.turn == chess.WHITE else "Black")
                        safe_print(f"[AI] Đã chọn nước đi: {move} trong {time.time() - start:.2f} giây")

                    self.move = move
                    if return_queue:
                        return_queue.put(move)

                except Exception as e:
                    safe_print("[Lỗi] Lỗi trong tìm kiếm:", e)
                    self.move = None
                    if return_queue:
                        return_queue.put(None)

            Thread(target=search_and_update).start()

    def update_ai_move(self, game, board_state):
        self.move = None
        return_queue = Queue()

        try:
            with chess.polyglot.open_reader("baron30.bin") as reader:
                try:
                    entry = reader.find(board_state)
                    self.move = entry.move
                    safe_print(f"[AI] Sử dụng sách khai cuộc: {self.move}")
                    game.board.push(self.move)
                    game.history_index = len(game.board.move_stack)
                    game.view_board = game.board.copy()
                    game.last_move_from = self.move.from_square 
                    game.last_move_to = self.move.to_square 
                    game.check_game_end()
                    if hasattr(game, 'root'):
                        game.root.title("Cờ vua - Đã xong")
                    return
                except IndexError:
                    safe_print("[AI] Không tìm thấy nước đi trong sách khai cuộc. Dùng Searcher.")
        except FileNotFoundError:
            safe_print("[Lỗi] Không tìm thấy tệp baron30.bin. Dùng Searcher.")
        except Exception as e:
            safe_print("[Lỗi] Lỗi khi mở sách khai cuộc:", e)

        self.run_search_process(board_state, return_queue)

        def check_result():
            if self.move and self.move in game.board.legal_moves:
                game.board.push(self.move)
                game.history_index = len(game.board.move_stack)
                game.view_board = game.board.copy()
                game.last_move_from = self.move.from_square 
                game.last_move_to = self.move.to_square  
                game.check_game_end()
                if hasattr(game, 'root'):
                    game.root.title("Cờ vua - Đã xong")
            elif not self.move:
                if hasattr(game, 'root'):
                    game.root.after(50, check_result)
                else:
                    time.sleep(0.05)
                    Thread(target=check_result).start()

        if hasattr(game, 'root'):
            game.root.title("AI đang nghĩ...")
            game.root.after(50, check_result)
        else:
            check_result()