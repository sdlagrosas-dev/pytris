import pygame
import sys
import random

from config import *
from button import Button
from blockfield import BlockField
from tetromino import Tetromino, TETROMINO_SHAPES, TETROMINO_COLORS
from scoreboard import ScoreBoard
from tetromino_queue import TetrominoQueue


def play():
    block_field = BlockField()
    score_board = ScoreBoard()
    tetromino_queue = TetrominoQueue()
    curr_tetromino = tetromino_queue.get_next_piece()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_LSHIFT and tetromino_queue.can_hold:
                    curr_tetromino = tetromino_queue.hold_current_piece(curr_tetromino)
                    curr_tetromino.row = 0  # Reset position for the new/held piece
                    curr_tetromino.col = curr_tetromino.calculate_start_column()
                    tetromino_queue.can_hold = False

        SCREEN.fill((0, 0, 0))

        if block_field.is_game_over():
            game_over()

        # Update and draw the current tetromino
        if curr_tetromino.update(dt, block_field):
            # If update returns True, we need a new piece
            curr_tetromino = tetromino_queue.get_next_piece()

        # Clear completed lines
        lines_cleared = block_field.clear_lines()
        score_board.update_score(lines_cleared)

        # Draw game elements
        block_field.draw(SCREEN)
        curr_tetromino.draw(SCREEN, block_field)
        score_board.draw(SCREEN)
        tetromino_queue.draw(SCREEN)

        dt = GAME_CLOCK.tick(15) / 1000
        pygame.display.flip()
        pygame.display.update()


def pause():
    pause_text = get_font(100).render("PAUSED", True, "#b68f40")
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

    resume_button = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, 300),
        text_input="RESUME",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )
    quit_button = Button(
        image=pygame.image.load("assets/Quit Rect.png"),
        pos=(SCREEN_WIDTH // 2, 450),
        text_input="QUIT",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )

    while True:
        SCREEN.blit(BG_MENU, (0, 0))

        SCREEN.blit(pause_text, pause_rect)
        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [resume_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(menu_mouse_pos):
                    return
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def game_over():

    game_over_text = get_font(100).render("GAME OVER", True, "#b68f40")
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

    replay_button = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, 300),
        text_input="REPLAY",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )
    quit_button = Button(
        image=pygame.image.load("assets/Quit Rect.png"),
        pos=(SCREEN_WIDTH // 2, 450),
        text_input="QUIT",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )

    while True:
        SCREEN.blit(BG_MENU, (0, 0))

        SCREEN.blit(game_over_text, game_over_rect)
        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [replay_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.checkForInput(menu_mouse_pos):
                    play()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("PyTris")

    menu_text = get_font(100).render("PyTris", True, "#b68f40")
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

    play_button = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, 250),
        text_input="PLAY",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )
    options_button = Button(
        image=pygame.image.load("assets/Options Rect.png"),
        pos=(SCREEN_WIDTH // 2, 400),
        text_input="OPTIONS",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )
    quit_button = Button(
        image=pygame.image.load("assets/Quit Rect.png"),
        pos=(SCREEN_WIDTH // 2, 550),
        text_input="QUIT",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White",
    )

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        SCREEN.blit(menu_text, menu_rect)

        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    pass
                    # options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
