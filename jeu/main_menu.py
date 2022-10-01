import sys

import pygame
from jeu.ui.button import Button
from jeu.utils.font_manager import FontManager


def main_menu(screen: pygame.surface.Surface):
    """Main menu of the game.

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    clock: pygame.time.Clock = pygame.time.Clock()
    
    pygame.display.set_caption("Menu")

    menu_font: FontManager = FontManager("jeu/assets/fonts/Truculenta.ttf")

    def quit():
        pygame.quit()
        sys.exit()

    # Initializing on-screen elements #
    background: pygame.surface.Surface = pygame.image.load("jeu/assets/images/menu_background.png")

    menu_text: pygame.surface.Surface = menu_font.get_font(100).render("MAIN MENU", True, "#EEEEEE")
    menu_rect: pygame.rect.Rect = menu_text.get_rect(center=(640, 100))

    play_button = Button(image=pygame.image.load("jeu/assets/images/Play Rect.png"),
                         position=(640, 250),
                         text="PLAY",
                         font=menu_font.get_font(75),
                         color="#FFFFFF",
                         hover_color="#d7fcd4",
                         action=lambda: print("Play!")
                         )
    options_button = Button(image=pygame.image.load("jeu/assets/images/Options Rect.png"),
                            position=(640, 400),
                            text="OPTIONS",
                            font=menu_font.get_font(75),
                            color="#FFFFFF",
                            hover_color="#d7fcd4",
                            action=lambda: print("Options!")
                            )
    quit_button = Button(image=pygame.image.load("jeu/assets/images/Quit Rect.png"),
                         position=(640, 550),
                         text="QUIT",
                         font=menu_font.get_font(75),
                         color="#FFFFFF",
                         hover_color="#d7fcd4",
                         action=quit
                         )

    while True:
        print(int(clock.get_fps()), end=" FPS    \r")
        screen.blit(background, (0, 0))

        menu_buttons: tuple[Button, ...] = (
            play_button, options_button, quit_button)
        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    print("            ", end="\r")  # Clear FPS counter from console
            for button in menu_buttons:
                button.update(event)
        for button in menu_buttons:
            button.update_render(screen)

        pygame.display.update()
        clock.tick()