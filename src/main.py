import pygame
import sys
from config import *
from button import Button


def play():
    print("Play button clicked")


def main():
    pygame.init()
    pygame.display.set_caption("PyTris")

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

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

        SCREEN.blit(menu_text, menu_rect)

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
