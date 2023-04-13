# <========== Import ==========>

from __future__ import annotations
from typing import Final
from jeu.engine.Player.Score import Score

# <========== Class ==========>


class Player:
    """
    Represent the player. This class holds all the methods that allow the player to interact with the game.
    """

    # <----- init ----->

    def __init__(self: Player, name: str, id: int, score_value: int = 0) -> None:
        """
        Create a new player.
        Args:
            name (str): The name of this user.
            id (int): An unique identifier for this user.
        """
        self.__NAME: Final[str] = name
        self.__ID: Final[int] = id
        self.__score: Score = Score(score_value)

    # <----- getter ----->

    @property
    def NAME(self: Player) -> str:
        """
        Define the name of this player
        """
        return self.__NAME

    @property
    def ID(self: Player) -> int:
        return self.__ID

    @property
    def score(self: Player) -> Score:
        return self.__score

    # <----- setter ----->

    @score.setter
    def score(self: Player, new_score: Score) -> None:
        self.__score = new_score

    # <----- str ----->

    def __str__(self: Player) -> str:
        return f"{self.__NAME} {self.__score}"
