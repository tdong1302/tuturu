import pygame
from ui import draw_board, draw_pieces, highlight_moves
from game import Game
from ui import draw_promotion_choices, draw_game_over
import chess

if __name__ == "__main__":
    WIDTH, HEIGHT = 630, 630 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    big_font = pygame.font.Font("assets/font.ttf", 48)
    small_font = pygame.font.Font("assets/font.ttf", 36)
    font = pygame.font.SysFont(None, 48)
    text1 = font.render("AI play White", True, (0, 0, 0))
    text2 = font.render("AI play Black", True, (255, 255, 255))

    background_img = pygame.image.load("assets/background.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    button_width, button_height = 250, 60
    white_rect = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - 80, button_width, button_height)
    black_rect = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 + 20, button_width, button_height)

    while True:
        waiting = True
        ai_color = None
        while waiting:
            screen.blit(background_img, (0, 0))

            pygame.draw.rect(screen, (255, 255, 255), white_rect)
            screen.blit(text1, (
                white_rect.centerx - text1.get_width() // 2,
                white_rect.centery - text1.get_height() // 2
            ))
            pygame.draw.rect(screen, (0, 0, 0), black_rect)
            screen.blit(text2, (
                black_rect.centerx - text2.get_width() // 2,
                black_rect.centery - text2.get_height() // 2
            ))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if white_rect.collidepoint(event.pos):
                        ai_color = chess.WHITE
                        waiting = False
                    elif black_rect.collidepoint(event.pos):
                        ai_color = chess.BLACK
                        waiting = False

        flip = ai_color == chess.WHITE
        game = Game(ai_color=ai_color, flip=flip)
        if game.board.turn == game.ai_color:
            game.ai_thinking = True
            game.ai_move_time = pygame.time.get_ticks()

        running = True
        while running and game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    running = False
                else:
                    game.handle_event(event)

            screen.fill((0, 0, 0))
            draw_board(screen, flip,
                       last_move_from=game.last_move_from,
                       last_move_to=game.last_move_to)
            if game.promoting:
                draw_promotion_choices(screen, game.promotion_color)
            elif game.selected_square is not None and game.history_index == len(game.board.move_stack):
                highlight_moves(screen, game.view_board, game.selected_square, flip)

            draw_pieces(screen, game.view_board, flip)
            game.update_ai_move()

            if game.history_index < len(game.board.move_stack):
                pygame.display.set_caption(f"Chess Game - Xem lại bước {game.history_index}/{len(game.board.move_stack)}")
            else:
                pygame.display.set_caption("Chess Game")

            replay_button = None
            
            game.check_game_end()
            if not game.running:  
                screen.fill((0, 0, 0))
                draw_board(screen, flip,
                           last_move_from=game.last_move_from,
                           last_move_to=game.last_move_to)
                draw_pieces(screen, game.view_board, flip)
                replay_button = draw_game_over(screen, game.board, big_font, small_font)

            pygame.display.flip()
            game.clock.tick(60)

    
            if not game.running and replay_button:
                waiting_for_replay = True
                while waiting_for_replay:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if replay_button.collidepoint(event.pos):
                                waiting_for_replay = False
                                running = False 
                    game.clock.tick(60)