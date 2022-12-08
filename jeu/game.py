import time

import pygame

from jeu.ui.button import Button
from jeu.ui.ui import UI
from jeu.utils.assets_import import resource_path
from jeu.utils.font_manager import FontManager
from jeu.engine.Pipopipette import Pipopipette

LINE_WIDTH = 9
HEIGHT_OFFSET = 250
WIDTH_OFFSET = 200
PLAYER1_COLOR = "#0000FF"
PLAYER2_COLOR = "#FF0000"

def formatted_score(score: int) -> str:
    return f"{score:03d}"


def formatted_time(time_in_seconds: int) -> str:
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def get_timer_label(start_time_in_seconds: float, font: FontManager):
    time_elapsed_in_seconds = int(time.time() - start_time_in_seconds)
    timer_label: pygame.surface.Surface = font.get_font(75).render(
        formatted_time(time_elapsed_in_seconds), True, "#EEEEEE")
    timer_rect: pygame.rect.Rect = timer_label.get_rect(center=(640, 50))
    return (timer_label, timer_rect)


def get_score_label(score: int, font: FontManager, player1: bool):
    if player1:
        xpos: int = 100
        color: str = PLAYER1_COLOR
    else:
        xpos: int = 1280-100
        color: str = PLAYER2_COLOR
    player_score_label: pygame.surface.Surface = font.get_font(
        75).render(f"{score:03d}", True, color)
    player_score_rect: pygame.rect.Rect = player_score_label.get_rect(
        center=(xpos, 650))
    return (player_score_label, player_score_rect)


def game(screen: pygame.surface.Surface, size: tuple[int, int] = (10, 5)):
    """Game screen

    Args:
        screen (pygame.surface.Surface): Screen to display the game on
    """

    pipo: Pipopipette = Pipopipette(*size)

    [print(str(x)) for x in pipo.list_square]

    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Pipopipette")

    game_font: FontManager = FontManager(
        resource_path("jeu/assets/fonts/Truculenta.ttf"))

    background: pygame.surface.Surface = pygame.image.load(
        resource_path("jeu/assets/images/game_background.png"))

    labels: dict[str, tuple[pygame.surface.Surface, pygame.rect.Rect]] = {}
    start_time_in_seconds: float = time.time()

    player1_label: pygame.surface.Surface = game_font.get_font(
        33).render("Playername01", True, "#EEEEEE")
    player1_rect: pygame.rect.Rect = player1_label.get_rect(center=(100, 593))
    player2_label: pygame.surface.Surface = game_font.get_font(
        33).render("Playername02", True, "#EEEEEE")
    player2_rect: pygame.rect.Rect = player2_label.get_rect(
        center=(1280-100, 593))

    labels["timer"] = get_timer_label(time.time(), game_font)
    labels["player1"] = (player1_label, player1_rect)
    labels["player2"] = (player2_label, player2_rect)
    labels["player1_score"] = get_score_label(0, game_font, True)
    labels["player2_score"] = get_score_label(0, game_font, False)

    started = False

    grid_height = 1280-WIDTH_OFFSET
    grid_width = 720-HEIGHT_OFFSET
    segments_height = grid_height//size[0]
    segments_width = grid_width//size[1]

    board_elements: list[UI] = []
    fillers: list[pygame.Rect] = []

    def get_segment_id(i: int, j: int):
        return i+size[0]*j

    def update_board():
        board_elements = []
        fillers: list[pygame.Rect] = []
        for i in range(size[0]+1):
            for j in range(size[1]+1):
                x_position: int = segments_height*i+HEIGHT_OFFSET//1.75-22  # type: ignore
                y_position: int = segments_width*j+WIDTH_OFFSET//1.75  # type: ignore
                filler = pygame.Rect(x_position, y_position,
                                     LINE_WIDTH, LINE_WIDTH)
                filler.center = (x_position-LINE_WIDTH*2.3,  # type: ignore
                                 y_position-LINE_WIDTH*2.3)
                fillers.append(filler)
                if i != size[0]:
                    def segment_handler(id):
                        print("Seg ID: ",id)

                    x_segment: Button = Button(
                        screen=screen,
                        image=pygame.image.load(resource_path(
                            "jeu/assets/images/square.png")),
                        position=(x_position+LINE_WIDTH, y_position),
                        text="",
                        font=game_font.get_font(10),
                        color="WHITE",
                        hover_color="BLACK",
                        action=lambda i=i, j=j: segment_handler(get_segment_id(i, j)),
                        enforced_size=(segments_height-LINE_WIDTH, LINE_WIDTH)
                    )
                    board_elements.append(x_segment)
                if j != size[1]:
                    # def segment_handler():
                    #     pass
                    y_segment: Button = Button(
                        screen=screen,
                        image=pygame.image.load(resource_path(
                            "jeu/assets/images/square.png")),
                        position=(x_position, y_position+LINE_WIDTH),
                        text="",
                        font=game_font.get_font(10),
                        color="WHITE",
                        hover_color="BLACK",
                        action=lambda: print("clickW"),
                        enforced_size=(LINE_WIDTH, segments_width-LINE_WIDTH)
                    )
                    board_elements.append(y_segment)
        return board_elements, fillers

    board_elements, fillers = update_board()
    while True:
        if started:
            labels["timer"] = get_timer_label(start_time_in_seconds, game_font)
            labels["player1_score"] = get_score_label(0, game_font, True)
            labels["player2_score"] = get_score_label(5, game_font, False)
        print(int(clock.get_fps()), end=" FPS    \r")
        screen.blit(background, (0, 0))
        for surface, rect in labels.values():
            screen.blit(surface, rect)

        for event in pygame.event.get():
            for element in board_elements:
                element.update(event)
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    if not started:
                        started = True
                        start_time_in_seconds = time.time()
                    # Clear FPS counter from console
                    print("            ", end="\r")
        for filler in fillers:
            pygame.draw.rect(screen, "#EEEEEE", filler)
        for element in board_elements:
            element.update_render()
        pygame.display.update()
        clock.tick()
