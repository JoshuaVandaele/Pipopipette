import sys

import pygame

from jeu.game import game
from jeu.login_screen import login_screen
from jeu.options_screen import options_screen
from jeu.ui.button import Button
from jeu.ui.popup import Popup
from jeu.ui.textbox import Textbox
from jeu.ui.ui import UI
from jeu.utils.assets_import import resource_path
from jeu.utils.font_manager import FontManager
from jeu.utils import settings
from jeu.utils.tools import gamemode

MAX_SIZE = 7
MIN_SIZE = 2

def main_menu(screen: pygame.surface.Surface):
    """Main menu of the game.

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    clock: pygame.time.Clock = pygame.time.Clock()

    pygame.display.set_caption("Menu")

    menu_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))

    uninteraction_timer = 0

    def quit():
        """Quits the program
        """
        pygame.quit()
        sys.exit()

    def play_button_handler(screen): 
        """ Popup that lets you select a size in this format:
        +-------------------------+
        |          Size           |
        | (Size) X (Size)  [OK]   |
        | [ 3x3 ] [ 5x5 ] [ 7x7 ] |
        +-------------------------+
        
        And the gamemode in this one:
        +-----------------------------+
        |          Game mode          |
        |                             |
        | [local] [A.I] [multiplayer] |
        +-----------------------------+

        Args:
            screen (_type_): Screen to display the popup on
        """
        # Create the size popup
        size_popup = Popup(
            screen=screen,
            title="Size",
            size=(1280//2, 720//2.5),
            color="#0575BB"
        )
        
        def play(size: tuple[int, int]):
            """
            Display the game mode selection popup and start the game with the chosen mode and board size.

            Args:
                size (tuple[int, int]): The desired board size as a tuple of width and height.
            """
            gamemode_popup = Popup(
                screen=screen,
                title="Game mode",
                size=(1280//2, 720//2.5),
                color="#0575BB"
            )
            
            mode: gamemode
            
            def change_gamemode(new_mode: gamemode):
                """
                Update the game mode and close the game mode selection popup.

                Args:
                    new_mode (gamemode): The new game mode to be set (e.g., LOCAL, AI, or ONLINE).
                """
                nonlocal mode
                mode = new_mode
                gamemode_popup.close()
            
            gammode_popup_local_button = Button(
                screen=gamemode_popup.surface,
                image=None,
                position=(gamemode_popup.surface.get_size()[0]//2*0.5, gamemode_popup.surface.get_size()[1]//1.6),
                text="LOCAL",
                font=menu_font.get_font(56),
                color="white",
                hover_color="black",
                action = lambda: change_gamemode(gamemode.LOCAL)
            )
            
            gammode_popup_ai_button = Button(
                screen=gamemode_popup.surface,
                image=None,
                position=(gamemode_popup.surface.get_size()[0]//2*1, gamemode_popup.surface.get_size()[1]//1.6),
                text="AI",
                font=menu_font.get_font(56),
                color="white",
                hover_color="black",
                action = lambda: change_gamemode(gamemode.AI)
            )
            
            gammode_popup_online_button = Button(
                screen=gamemode_popup.surface,
                image=None,
                position=(gamemode_popup.surface.get_size()[0]//2*1.5, gamemode_popup.surface.get_size()[1]//1.6),
                text="ONLINE",
                font=menu_font.get_font(56),
                color="white",
                hover_color="black",
                action = lambda: change_gamemode(gamemode.ONLINE)
            )
            
            gamemode_popup.add_ui_element(gammode_popup_ai_button)
            gamemode_popup.add_ui_element(gammode_popup_local_button)
            gamemode_popup.add_ui_element(gammode_popup_online_button)
            
            gamemode_popup.run()
            game(screen, mode=mode, size=size, config=settings.get_settings()) #type: ignore
            gamemode_popup.close() 
            size_popup.close()

        # Create the rightmost size select button
        size_popup_3x3_button = Button(
            screen=size_popup.surface,
            image=None,
            position=(size_popup.surface.get_size()[0]//2*0.5, size_popup.surface.get_size()[1]//1.25),
            text="3x3",
            font=menu_font.get_font(56),
            color="white",
            hover_color="black",
            action = lambda: play((3, 3)) 
        )

        # Create the center size select button
        size_popup_5x5_button = Button(
            screen=size_popup.surface,
            image=None,
            position=(size_popup.surface.get_size()[0]//2, size_popup.surface.get_size()[1]//1.25),
            text="5x5",
            font=menu_font.get_font(56),
            color="white",
            hover_color="black",
            action = lambda: play((5, 5)) 
        )


        # Create the leftmost size select button
        size_popup_7x7_button = Button(
            screen=size_popup.surface,
            image=None,
            position=(size_popup.surface.get_size()[0]//2*1.5, size_popup.surface.get_size()[1]//1.25),
            text="7x7",
            font=menu_font.get_font(56),
            color="white",
            hover_color="black",
            action = lambda: play((7, 7)) 
        )


        # Create the x-size select textbox
        size_popup_custom_size_x_textbox = Textbox(
            screen=size_popup.surface,
            position=(size_popup.surface.get_size()[0]//2*0.55, size_popup.surface.get_size()[1]//2),
            placeholder_text=F"{MIN_SIZE}-{MAX_SIZE}",
            placeholder_color="#424242",
            size=(125, 75),
            font=menu_font.get_font(56),
            text_color="black",
            background_color="white",
            max_char = 2,
            accepted_chars = ["0","1","2","3","4","5","6","7","8","9"]
        )

        # Create the y-size select textbox
        size_popup_custom_size_y_textbox = Textbox(
            screen=size_popup.surface,
            position=(size_popup.surface.get_size()[0]//2*1.15, size_popup.surface.get_size()[1]//2),
            placeholder_text=F"{MIN_SIZE}-{MAX_SIZE}",
            placeholder_color="#424242",
            size=(125, 75),
            font=menu_font.get_font(56),
            text_color="black",
            background_color="white",
            max_char = 2,
            accepted_chars = ["0","1","2","3","4","5","6","7","8","9"]
        )

        def confirm_custom_size_button_handler():
            """Handler for the custom size confirm button
            Will only allow sizes between MAX_SIZE and MIN_SIZE,
            and fall back to them if they're exceeded
            """
            nonlocal uninteraction_timer
            x_size: int = 0
            y_size: int = 0
            x_size_text: str = size_popup_custom_size_x_textbox.text
            y_size_text: str = size_popup_custom_size_y_textbox.text
            if x_size_text:
                x_size = int(x_size_text)
            else:
                x_size = 5
            
            if y_size_text:
                y_size = int(y_size_text)
            else:
                y_size = 5
            
            if x_size > MAX_SIZE:
                x_size = MAX_SIZE
            elif x_size < MIN_SIZE:
                x_size = MIN_SIZE
            
            if y_size > MAX_SIZE:
                y_size = MAX_SIZE
            elif y_size < MIN_SIZE:
                y_size = MIN_SIZE
            
            play((x_size, y_size)) 

        # Create the custom size confirm button
        size_popup_confirm_custom_size_button = Button(
            screen=size_popup.surface,
            image=None,
            position=(size_popup.surface.get_size()[0]//2*1.5, size_popup.surface.get_size()[1]//2),
            text="OK",
            font=menu_font.get_font(64),
            color="white",
            hover_color="black",
            action=confirm_custom_size_button_handler
        )

        # Creates the "X" to be displayed between the two textboxes
        x_label: pygame.surface.Surface = menu_font.get_font(96).render(f"x", True, "white")
        x_rect: pygame.rect.Rect = x_label.get_rect(center=(size_popup.surface.get_size()[0]//2*0.85, size_popup.surface.get_size()[1]//2*0.95))

        # Add all the created elements to the popup and run it
        size_popup.add_ui_element(size_popup_3x3_button)
        size_popup.add_ui_element(size_popup_5x5_button)
        size_popup.add_ui_element(size_popup_7x7_button)
        size_popup.add_ui_element(size_popup_custom_size_x_textbox)
        size_popup.add_ui_element(size_popup_custom_size_y_textbox)
        size_popup.add_ui_element(size_popup_confirm_custom_size_button)
        size_popup.add_rect(x_label, x_rect)

        size_popup.run()
        size_popup.close()
        uninteraction_timer = 10

    # Initializing on-screen elements #
    background: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/menu_background.png"))

    menu_text: pygame.surface.Surface = menu_font.get_font(
        100).render("PIPOPIPETTE", True, "#EEEEEE")
    menu_rect: pygame.rect.Rect = menu_text.get_rect(center=(640, 75))

    play_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Play Rect.png")),
        position=(640, 250),
        text="PLAY",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=lambda: play_button_handler(screen)
    )
    options_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Options Rect.png")),
        position=(640, 400),
        text="OPTIONS",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=lambda: options_screen(screen)
    )
    quit_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Quit Rect.png")),
        position=(640, 550),
        text="QUIT",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=quit
    )

    def account_button_handler():
        nonlocal uninteraction_timer
        login_screen(screen)
        uninteraction_timer = 10

    account_button = Button(screen=screen, image=pygame.image.load(resource_path("jeu/assets/images/User.png")),
                            position=(1280-75, 75),
                            text=" ",
                            font=menu_font.get_font(75),
                            color="#FFFFFF",
                            hover_color="#FFFFFF",
                            action=account_button_handler
                            )
    # Store all UI elements in a list for easy access
    menu_buttons: tuple[UI, ...] = (account_button, play_button, options_button, quit_button)

    while True:
        if uninteraction_timer > 0:
            uninteraction_timer -= 1
        print(int(clock.get_fps()), end=" FPS    \r")
        # Blit the background to screen first /!\
        screen.blit(background, (0, 0))
        # Display all text on screen
        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    # Clear FPS counter from console
                    print("            ", end="\r")
            # Update all UI elements
            for button in menu_buttons:
                if uninteraction_timer <= 0:
                    button.update(event)
        # Update all UI elements
        for button in menu_buttons:
            button.update_render()
        # Update the display
        pygame.display.update()
        # Tick the clock used to calculate the FPS
        clock.tick()
