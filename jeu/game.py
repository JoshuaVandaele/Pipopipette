import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pygame

from jeu.engine.Pipopipette import Pipopipette
from jeu.engine.PipopipetteAI import PipopipetteAI
from jeu.engine.PipopipetteGameplay import PipopipetteGameplay
from jeu.ui.button import Button
from jeu.ui.popup import Popup
from jeu.ui.ui import UI
from jeu.utils.assets_import import resource_path
from jeu.utils.font_manager import FontManager
from jeu.utils.settings import DEFAULT_SETTINGS
from jeu.utils.tools import gamemode

LINE_WIDTH = 9
HEIGHT_OFFSET = 250
WIDTH_OFFSET = 200
PLAYER1_COLOR = "blue"
PLAYER2_COLOR = "red"
PLAYER_COLORS = (PLAYER1_COLOR, PLAYER2_COLOR)
PLAYER_COUNT = 2
EXECUTOR = ThreadPoolExecutor(max_workers=2)


def quit():
    """Quits the program"""
    EXECUTOR.shutdown(wait=True)
    pygame.quit()
    sys.exit()


def formatted_score(score: int) -> str:
    """Returns an integer into a formatted string

    Args:
        score (int): Score

    Returns:
        str: Formatted string with three digits
    """
    return f"{score:03d}"


def formatted_time(time_in_seconds: int) -> str:
    """Formats time in seconds into time in minutes and seconds

    Args:
        time_in_seconds (int): Time in seconds

    Returns:
        str: time in the format "mm:ss"
    """
    minutes, seconds = divmod(time_in_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def get_stopwatch_label(
    start_time_in_seconds: float, font: FontManager
) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
    """Returns a new timer rect and label for the current elapsed time

    Args:
        start_time_in_seconds (float): Time in seconds since the timer has started
        font (FontManager): Font used to display the timer

    Returns:
        tuple[pygame.surface.Surface, pygame.rect.Rect]: Surface and rect for the newly created timer text
    """
    time_elapsed_in_seconds = int(time.time() - start_time_in_seconds)
    timer_label: pygame.surface.Surface = font.get_font(75).render(
        formatted_time(time_elapsed_in_seconds), True, "#EEEEEE"
    )
    timer_rect: pygame.rect.Rect = timer_label.get_rect(center=(640, 50))
    return (timer_label, timer_rect)


def get_score_label(
    score: int, font: FontManager, player1: bool
) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
    """Returns a new score rect and label for the player one or two

    Args:
        score (int): Score for the player
        font (FontManager): Font to display the socre in
        player1 (bool): Player 1 - True, Player 2 - False

    Returns:
        tuple[pygame.surface.Surface, pygame.rect.Rect]: Surface and rect for the newly created score text
    """
    # Depending on the player selected, the position and color of the text is different
    if player1:
        xpos: int = 100
        color: str = PLAYER1_COLOR
    else:
        xpos: int = 1280 - 100
        color: str = PLAYER2_COLOR
    player_score_label: pygame.surface.Surface = font.get_font(75).render(
        f"{score:03d}", True, color
    )
    player_score_rect: pygame.rect.Rect = player_score_label.get_rect(
        center=(xpos, 650)
    )
    return (player_score_label, player_score_rect)


def game(
    screen: pygame.surface.Surface,
    mode: gamemode,
    size: tuple[int, int] = (5, 5),
    players: tuple[str, str] = ("Playername00", "Playername01"),
    config: dict[str, Any] = DEFAULT_SETTINGS,
):
    """Game screen, to play the game of Pipopipette

    Args:
        screen (pygame.surface.Surface): Screen to display the game onto
        size (tuple[int, int]): Size of the grid to play on
        players (tuple[str, str]): Tuple of usernames to display for the players
        mode (int): Game mode. 0 -> Player vs Player (local), 1 -> Player vs AI, 2 -> Player vs Player (online)
        config (dict[str, Any]): Configuration
    """
    # Initialize game
    pipo: Pipopipette = Pipopipette(*size)
    gameplay: PipopipetteGameplay = PipopipetteGameplay(
        list_player_name=list(players), pipopipette=pipo
    )

    # Initialize pygame
    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Pipopipette")

    # Pre-load fonts
    game_font: FontManager = FontManager(
        resource_path("jeu/assets/fonts/Truculenta.ttf")
    )

    # Load background
    background: pygame.surface.Surface = pygame.image.load(
        resource_path("jeu/assets/images/game_background.png")
    )

    # Initialize values
    labels: dict[str, tuple[pygame.surface.Surface, pygame.rect.Rect]] = {}
    start_time_in_seconds: float = time.time()

    # Initialize player usernames labels
    player1_label: pygame.surface.Surface = game_font.get_font(33).render(
        players[0], True, "#EEEEEE"
    )
    player1_rect: pygame.rect.Rect = player1_label.get_rect(center=(100, 593))
    player2_label: pygame.surface.Surface = game_font.get_font(33).render(
        players[1], True, "#EEEEEE"
    )
    player2_rect: pygame.rect.Rect = player2_label.get_rect(center=(1280 - 100, 593))

    # Load and create end popup
    end_popup = Popup(
        screen=screen,
        title="Game Over",
        size=(1280 // 1.9, 720 // 1.5),
        color="#0575BB",
    )

    def restart_button_handler():
        end_popup.active = False
        game(screen, mode, size, players, config)

    # Add a vertically centered restart button
    end_popup_restart_button = Button(
        screen=end_popup.surface,
        image=None,
        position=(
            end_popup.surface.get_size()[0] // 2,
            end_popup.surface.get_size()[1] // 1.2,
        ),
        text="Try Again",
        font=game_font.get_font(48),
        color="white",
        hover_color="black",
        action=restart_button_handler,
    )
    # register it to the end popup
    end_popup.add_ui_element(end_popup_restart_button)

    # Initialise text on screen
    labels["timer"] = get_stopwatch_label(time.time(), game_font)
    labels["player1"] = (player1_label, player1_rect)
    labels["player2"] = (player2_label, player2_rect)
    labels["player1_score"] = get_score_label(0, game_font, True)
    labels["player2_score"] = get_score_label(0, game_font, False)

    started = False
    # Pre-calculate variables used for positioning
    grid_height = 1280 - WIDTH_OFFSET
    grid_width = 720 - HEIGHT_OFFSET
    segments_height = grid_height // size[0]
    segments_width = grid_width // size[1]

    # Initialise variables used for the game
    board_elements: list[UI] = []
    fillers: list[pygame.Rect] = []
    owned_segments: dict[tuple[int, int, str], int] = {}

    def ij_from_square_id(square_id: int, side: str) -> tuple[int, int]:
        if side in {"t", "d"}:
            gi: int = square_id % gameplay.pipopipette.WIDTH
            gj: int = square_id // gameplay.pipopipette.WIDTH
            if side == "d":
                gj += 1
        else:
            gj: int = square_id // gameplay.pipopipette.WIDTH
            gi: int = square_id % gameplay.pipopipette.WIDTH
            if side == "r" and gi == gameplay.pipopipette.WIDTH - 1:
                gi += 1
        return gi, gj

    def segment_handler(square_id: int, side: str):
        """Handles the clicking of a square's segment

        Args:
            square_id (int): id of the clicked square
            side (str): side which was clicked on the square
        """
        gi, gj = ij_from_square_id(square_id, side)

        print(square_id, side, gi, gj)
        nonlocal owned_segments
        nonlocal start_time_in_seconds
        if gameplay.pipopipette.valid_target(square_id, side):
            old_score: list[int] = gameplay.get_score()
            gameplay.set_player_target(square_id, side)
            owned_segments[(gi, gj, side)] = gameplay.current_player_ID
            new_score: list[int] = gameplay.get_score()
            if (
                old_score[gameplay.current_player_ID]
                >= new_score[gameplay.current_player_ID]
            ):
                gameplay.next_player()
                if "timer" in config and config["timer"] > 0:
                    start_time_in_seconds = time.time()
                match mode:
                    case gamemode.AI:
                        old_score = []
                        while old_score != new_score:
                            old_score: list[int] = gameplay.get_score()
                            print(gameplay.game_over())
                            a_square, a_side = PipopipetteAI.move_minmax(
                                gameplay, depth=3
                            )
                            if not a_side:
                                print("Not", a_side)
                                break
                            ai, aj = ij_from_square_id(a_square, a_side)  # type: ignore
                            gameplay.set_player_target(a_square, a_side)  # type: ignore
                            owned_segments[
                                (ai, aj, a_side)
                            ] = gameplay.current_player_ID
                            new_score: list[int] = gameplay.get_score()
                    case gamemode.ONLINE:
                        raise NotImplementedError(
                            "Online multiplayer hasn't been implemented yet."
                        )
                gameplay.next_player()
                if "timer" in config and config["timer"] > 0:
                    start_time_in_seconds = time.time()
        else:
            # Screen shake / Red tint?
            print(square_id, side, (gi, gj), "is not a valid target!")

    def update_board() -> tuple[list[UI], list[pygame.Rect]]:
        """Updates the board

        Returns:
            tuple[list[UI], list[pygame.Rect]]: List of board elements to display
        """
        board_elements: list[UI] = []
        fillers: list[pygame.Rect] = []
        counter = {}
        for i in range(size[0] + 1):
            for j in range(size[1] + 1):
                # Calculates the position of the segment
                x_position: int = segments_height * i + HEIGHT_OFFSET // 1.75 - 22  # type: ignore
                y_position: int = segments_width * j + WIDTH_OFFSET // 1.75  # type: ignore
                # Fillers are the gray square in-between each segments, they can not be interacted with
                filler = pygame.Rect(x_position, y_position, LINE_WIDTH, LINE_WIDTH)
                filler.center = (  # type: ignore
                    x_position - LINE_WIDTH * 2.3,
                    y_position - LINE_WIDTH * 2.3,
                )
                fillers.append(filler)

                if i != size[0]:
                    # Select the color based on who owns the segment
                    color: str = "white"
                    for side in ("t", "d"):
                        if (i, j, side) in owned_segments:
                            color = PLAYER_COLORS[owned_segments[(i, j, side)]]

                    def vertical_segment_handler(i: int, j: int):
                        """Calculates the square's ID and segment clicked and calls `segment_handler`

                        Args:
                            i (int): horizontal position of the segment
                            j (int): vertical position of the segment
                        """
                        square_id = i + size[0] * j
                        side: str = "t"
                        if square_id > len(pipo.list_square) - 1:
                            side = "d"
                            square_id = square_id - size[0]

                        EXECUTOR.submit(segment_handler, square_id, side)

                    # Create a vertical segment
                    x_segment: Button = Button(
                        screen=screen,
                        image=pygame.image.load(
                            resource_path(f"jeu/assets/images/{color}.png")
                        ),
                        position=(x_position + LINE_WIDTH, y_position),
                        text="",
                        font=game_font.get_font(10),
                        color="WHITE",
                        hover_color="BLACK",
                        action=lambda i=i, j=j: vertical_segment_handler(i, j),
                        enforced_size=(segments_height - LINE_WIDTH, LINE_WIDTH),
                    )
                    board_elements.append(x_segment)
                if j != size[1]:
                    # Select the color based on who owns the segment
                    color: str = "white"

                    for key in counter:
                        counter[key] -= 1
                        if counter[key] == 0:
                            color = PLAYER_COLORS[owned_segments[key]]

                    if (i, j, "l") in owned_segments:
                        color = PLAYER_COLORS[owned_segments[(i, j, "l")]]

                    if (i, j, "r") in owned_segments:
                        if i == gameplay.pipopipette.WIDTH:
                            color = PLAYER_COLORS[owned_segments[(i, j, "r")]]
                        else:
                            counter[(i, j, "r")] = gameplay.pipopipette.WIDTH

                    def horizontal_segment_handler(i: int, j: int):
                        """Calculates the square's ID and segment clicked and calls `segment_handler`

                        Args:
                            i (int): horizontal position of the segment
                            j (int): vertical position of the segment
                        """
                        newi: int = i - (i // size[0])
                        side: str = "l"
                        if i % size[0] == 0 and i != newi:
                            side = "r"
                        square_id = newi + size[0] * j

                        EXECUTOR.submit(segment_handler, square_id, side)

                    # Creates a horizontal segment
                    y_segment: Button = Button(
                        screen=screen,
                        image=pygame.image.load(
                            resource_path(f"jeu/assets/images/{color}.png")
                        ),
                        position=(x_position, y_position + LINE_WIDTH),
                        text="",
                        font=game_font.get_font(10),
                        color="WHITE",
                        hover_color="BLACK",
                        action=lambda i=i, j=j: horizontal_segment_handler(i, j),
                        enforced_size=(LINE_WIDTH, segments_width - LINE_WIDTH),
                    )
                    board_elements.append(y_segment)
        return board_elements, fillers

    def player_can_interact() -> bool:
        """Weither or not the current player is allowed to interact with the board or not

        Returns:
            bool: True if the player can, False otherwise
        """
        return (
            gameplay.current_player_ID == 0 and mode in [gamemode.AI, gamemode.ONLINE]
        ) or mode == gamemode.LOCAL

    board_elements, fillers = update_board()
    end_update_counter: int = 0
    animation_frame_counter: int = 0
    end_flag = 0
    # Game loop
    while True:
        animation_frame_counter += 1
        can_interact: bool = player_can_interact()
        # Update the relevant elements only once the game has started
        if started:
            score: list[int] = gameplay.get_score()
            board_elements, fillers = update_board()
            if can_interact:
                labels["timer"] = get_stopwatch_label(start_time_in_seconds, game_font)
            else:
                text = game_font.get_font(75).render(
                    "Waiting for opponent"
                    + "." * (animation_frame_counter % 3 + 1)
                    + " " * (3 - animation_frame_counter % 3 + 1),
                    True,
                    "#EEEEEE",
                )
                rect = text.get_rect(center=(640, 45))
                labels["timer"] = (text, rect)
            labels["player1_score"] = get_score_label(score[0], game_font, True)
            labels["player2_score"] = get_score_label(score[1], game_font, False)
            if (
                can_interact
                and "timer" in config
                and config["timer"] > 0
                and (time.time() - start_time_in_seconds > config["timer"])
                and (end_update_counter == 0)
            ):
                end_update_counter = 1
                end_flag = 1
        # Display the FPS counter in console
        print(int(clock.get_fps()), end=" FPS    \r")
        # Display the background to the screen first /!\
        screen.blit(background, (0, 0))
        # Update and display all text
        for surface, rect in labels.values():
            screen.blit(surface, rect)

        for event in pygame.event.get():
            # Send all events to the UI elements
            if can_interact:
                for element in board_elements:
                    element.update(event)
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    # Start the game on first click
                    if not started:
                        started = True
                        start_time_in_seconds = time.time()
                    # Clear FPS counter from console
                    print("            ", end="\r")
        # Display each filler
        for filler in fillers:
            pygame.draw.rect(screen, "#EEEEEE", filler)
        # Display each UI element
        for element in board_elements:
            element.update_render()
        # Update the display
        pygame.display.update()
        # Tick the clock used to calculate FPS
        clock.tick()
        if started:
            # If the game is over, wait 10 frames before displaying the end popup
            if end_update_counter > 0 or gameplay.game_over():
                end_update_counter += 1
            if end_update_counter == 10:
                score: list[int] = gameplay.get_score()
                # Obtain the text for each of the player's scores
                player1_score_label: pygame.surface.Surface = game_font.get_font(
                    75
                ).render(f"{score[0]:03d}", True, PLAYER1_COLOR)
                player2_score_label: pygame.surface.Surface = game_font.get_font(
                    75
                ).render(f"{score[1]:03d}", True, PLAYER2_COLOR)
                player1_score_rect: pygame.rect.Rect = player1_score_label.get_rect(
                    center=(
                        end_popup.surface.get_size()[0] // 2 * 0.5,
                        end_popup.surface.get_size()[1] // 2 * 1.3,
                    )
                )
                player2_score_rect: pygame.rect.Rect = player1_score_label.get_rect(
                    center=(
                        end_popup.surface.get_size()[0] // 2 * 1.5,
                        end_popup.surface.get_size()[1] // 2 * 1.3,
                    )
                )
                winner_str: str = "default_winner_str"
                match end_flag:
                    case 1:  # Time out
                        # If a player has more score than the other, he wins, otherwise it's a draw
                        winner_str = f"{players[gameplay.current_player_ID]} timed out"
                        # Create the winner text
                        winner_label: pygame.surface.Surface = game_font.get_font(
                            75
                        ).render(winner_str, True, "white")
                        winner_rect: pygame.rect.Rect = winner_label.get_rect(
                            center=(
                                end_popup.surface.get_size()[0] // 2,
                                end_popup.surface.get_size()[1] // 2 * 0.8,
                            )
                        )
                        end_popup.add_rect(winner_label, winner_rect)
                    case _:  # The game is over
                        winner_str = "Draw!"
                        # If a player has more score than the other, he wins, otherwise it's a draw
                        if score[0] > score[1]:
                            winner_str = f"{players[0]} wins!"
                        elif score[1] > score[0]:
                            winner_str = f"{players[1]} wins!"
                        # Create the winner text
                        winner_label: pygame.surface.Surface = game_font.get_font(
                            75
                        ).render(winner_str, True, "white")
                        winner_rect: pygame.rect.Rect = winner_label.get_rect(
                            center=(
                                end_popup.surface.get_size()[0] // 2,
                                end_popup.surface.get_size()[1] // 2 * 0.8,
                            )
                        )
                        end_popup.add_rect(winner_label, winner_rect)
                # Add all the previously created texts and display the popup
                end_popup.add_rect(player1_score_label, player1_score_rect)
                end_popup.add_rect(player2_score_label, player2_score_rect)
                end_popup.run()
                # Exit game loop
                EXECUTOR.shutdown(wait=True)
                return
