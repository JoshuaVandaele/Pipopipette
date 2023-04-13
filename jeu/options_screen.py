import pygame

from jeu.ui.button import Button
from jeu.ui.popup import Popup
from jeu.ui.textbox import Textbox
from jeu.utils import settings
from jeu.utils.assets_import import resource_path
from jeu.utils.font_manager import FontManager

MARGIN = 32


def options_screen(screen: pygame.surface.Surface):
    """Options screen

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    current_settings = settings.get_settings()
    options_font: FontManager = FontManager(
        resource_path("jeu/assets/fonts/Truculenta.ttf")
    )

    # Initializing on-screen elements #
    options_popup: Popup = Popup(
        screen,
        "Options",
        (screen.get_width() * 0.85, screen.get_height() * 0.8),
        "#0575BB",
    )

    def close_popup():
        """Overwritten close button handler for the popup that saves the settings upon clicking it"""
        config = {}
        if timer := timer_textbox.text:
            config["timer"] = int(timer)
        settings.save(config)
        options_popup.close()

    # Edit close button to make it save
    options_popup.elements[0] = Button(
        screen=options_popup.surface,
        image=pygame.image.load(resource_path("jeu/assets/images/close.png")),
        position=(options_popup.surface.get_width() - 25, 25),
        text=" ",
        font=options_popup.font.get_font(50),
        color="#000000",
        hover_color="#555555",
        action=close_popup,
        detection_offset=options_popup.offset,
    )

    timer_label: pygame.surface.Surface = options_font.get_font(56).render(
        "Timer", True, "white"
    )
    timer_label_rect: pygame.rect.Rect = timer_label.get_rect(
        center=(200 // 2 + MARGIN, options_popup.surface.get_size()[1] // 2 * 0.45)
    )

    default_timer: int = settings.DEFAULT_SETTINGS["timer"]
    timer_textbox: Textbox = Textbox(
        screen=options_popup.surface,
        position=(200 // 2 + MARGIN, options_popup.surface.get_size()[1] // 2 * 0.7),
        placeholder_text=f"{default_timer} seconds",
        placeholder_color="#424242",
        size=(200, 75),
        font=options_font.get_font(40),
        text_color="black",
        background_color="white",
        max_char=3,
        accepted_chars=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    )

    if "timer" in current_settings and current_settings["timer"] != default_timer:
        timer_textbox.text = str(current_settings["timer"])

    options_popup.add_rect(timer_label, timer_label_rect)
    options_popup.add_ui_element(timer_textbox)
    options_popup.run()
