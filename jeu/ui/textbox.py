from __future__ import annotations

import pygame

from jeu.ui.ui import UI

DEFAULT_ACCEPTED_CHARACTERS = [chr(i) for i in range(32, 255) if i != 127]
class Textbox(UI):
    def __init__(self: Textbox, screen: pygame.surface.Surface, position: tuple[float, float], placeholder_text: str, font: pygame.font.Font, size: tuple[float, float], text_color: str = "Black", background_color: str = "White", placeholder_color: str = "#E4E4E4", replacement_char: str|None = None, detection_offset: tuple[float, float] = (0, 0), max_char: int = 0, accepted_chars: list[str] = DEFAULT_ACCEPTED_CHARACTERS) -> None:
        """Textbox UI element

        Args:
            screen (pygame.surface.Surface): Screen to update the textbox on
            position (tuple[int, int]): X and Y position of the textbox
            placeholder_text (str): Text to display when the textbox is empty
            font (pygame.font.Font): Font to use for the text
            color (str): Color of the text
            detection_offset (tuple[float, float]): Offset for the mouse/textbox interaction
            max_char (int): Maximum accepted amount of characters
            accepted_chars (list[str]): List of accepted characters
        """
        super().__init__(screen, detection_offset)
        self.focused: bool = False
        self.text: str = ""
        self.size: tuple[float, float] = size
        self.center: tuple[float, float] = tuple(coord/2 for coord in self.size)
        self.surface = pygame.Surface(self.size)
        self.replacement_char = replacement_char
        if self.replacement_char:
            self.replacement_char = self.replacement_char[:1]

        self.position = position
        self.font = font
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.background_color = background_color
        self.placeholder_text = placeholder_text
        self.placeholder_text_render = self.font.render(
            self.placeholder_text, True, self.placeholder_color)
        self.rect = self.surface.get_rect(center=self.position)
        self.placeholder_text_rect = self.placeholder_text_render.get_rect(
            center=self.center)
        self.max_char: int = max_char
        self.accepted_chars: list[str] = accepted_chars

    def update_render(self: Textbox) -> None:
        """Updates the button

        Args:
            screen (pygame.surface.Surface): Screen to update the button on
        """
        self.surface.fill(self.background_color)
        if self.text == "":
            self.surface.blit(self.placeholder_text_render,
                              self.placeholder_text_rect)
        else:
            if self.replacement_char:
                text_render = self.font.render(self.replacement_char*len(self.text), True, self.text_color)
            else:
                text_render = self.font.render(self.text, True, self.text_color)
            self.surface.blit(
                text_render, text_render.get_rect(center=self.center))
        self.screen.blit(self.surface, self.rect)
    
    def _process_input(self, event: pygame.event.Event):
        """Processes the keyboard keydown event

        Args:
            event (pygame.event.Event): Keydown event to process
        """
            
        match event.key:
            case pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            case pygame.K_ESCAPE:
                self.focused = False
            case _:
                # If we haven't hit the max char limit/there isn't one,
                # and if the character is in the list of accepted chars/there isn't one, append to the string
                if (self.max_char == 0 or len(self.text) < self.max_char) and (
                    not self.accepted_chars or event.unicode in self.accepted_chars
                ):
                    self.text += event.unicode

    def update(self: Textbox, event: pygame.event.Event):
        """Updates the textbox according to a give event.

        Args:
            event (pygame.event.Event): Event to process
        """
        mouse_pos: tuple[float, float] = (pygame.mouse.get_pos()[0]-self.detection_offset[0], pygame.mouse.get_pos()[1]-self.detection_offset[1])
        match event.type:
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.repeat_settings = pygame.key.get_repeat()
                    pygame.key.set_repeat(500, 50)
                    self.focused = True
                else:
                    try:
                        pygame.key.set_repeat(*self.repeat_settings)
                    except Exception:
                        pass
                    self.focused = False
            case pygame.KEYDOWN:
                if self.focused:
                    self._process_input(event)