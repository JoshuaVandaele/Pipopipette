# <========== Import ==========>

from __future__ import annotations
from random import shuffle
from typing import Final
from jeu.engine.Square.Square import Square
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jeu.engine.Square.Segment import Segment

# <========== Class ==========>

class Pipopipette():
    """
    The class that will manage the playground.
    """
    
    # <----- init ----->
    
    def __init__(self: Pipopipette, width: int = 5, height: int = 5) -> None:
        """

        Args:
            width: The width of the game
            height: The height of the game
        """
        self.__WIDTH: Final[int] = width
        self.__HEIGHT: Final[int] = height
        self.__list_square: list[Square] = [Square(i) for i in range(width * height)]
        shuffle(self.__list_square)
    
    # <----- getter ----->
    
    @property
    def WIDTH(self: Pipopipette) -> int: return self.__WIDTH
    
    @property
    def HEIGHT(self: Pipopipette) -> int: return self.__HEIGHT
    
    @property
    def list_square(self: Pipopipette) -> list[Square]: return self.__list_square
    
    # <----- setter ----->

    @list_square.setter
    def list_square(self: Pipopipette, newlist_square: list[Square]) -> None: self.__list_square = newlist_square.copy()

    # <----- str ----->

    def __str__(self: Pipopipette) -> str:
        return_str = ""
        for square in self.__list_square: return_str += square.__str__() + " "
        return return_str
    
     # <----- get_square_by_ID ----->
    
    def get_square_by_ID(self: Pipopipette, id: int) -> Square | None:
        """Used to get a Square by his ID
        
        Args:
            id: A Square's id

        Returns:
            The found square, or None
        """
        for square in self.__list_square:
            if square.ID == id: return square
        return None
    
    # <----- set_side ----->
    
    def set_side(self: Pipopipette, square_ID: int, side: str, owner_ID: int) ->  None:
        """Define the owner of a side.
        
        Args:
            square_ID (int): ID of the Squre to edit.
            side (str): 'l'; 'r', 't', or 'd'. Side to edit.
            owner_ID (int): ID of the player who placed this side

        """
        if (square := self.get_square_by_ID(square_ID)) != None:
            match side:
                case 'l':
                    square.left = owner_ID
                    if ((neighbor := self.get_square_by_ID(square_ID-1)) != None and square_ID%self.__WIDTH):
                        neighbor.right = owner_ID
                case 'r':
                    square.right = owner_ID
                    if ((neighbor := self.get_square_by_ID(square_ID+1)) != None and neighbor.ID%(self.__WIDTH)):
                        neighbor.left = owner_ID
                case 't':
                    square.top = owner_ID
                    if (neighbor := self.get_square_by_ID(square_ID-self.__WIDTH)) != None:
                        neighbor.down = owner_ID
                case 'd':
                    square.down = owner_ID
                    if (neighbor := self.get_square_by_ID(square_ID+self.__WIDTH)) != None:
                        neighbor.top = owner_ID

    def get_side(self: Pipopipette, square_ID: int, side: str) ->  Segment|None:
        """Gets the owner of a side.
        
        Args:
            square_ID (int): ID of the Squre to edit.
            side (str): 'l'; 'r', 't', or 'd'. Side to edit.

        """
        if (square := self.get_square_by_ID(square_ID)) != None:
            match side:
                case 'l':
                    return square.left
                case 'r':
                    return square.right
                case 't':
                    return square.top
                case 'd':
                    return square.down

    # <----- valide_target ----->
    
    def valid_target(self: Pipopipette, square_ID: int, side: str) -> bool:
        """Weither or not a player can place a Segment here.
        
        Args:
            Square_ID (int): ID of the square to verify.
            side (str): 'l', 'r', 't', or 'd'. Side to verify.

        Returns:
            bool: True if a player can place a Segment here, False otherwise.

        """
        if (square := self.get_square_by_ID(square_ID)) != None:
            match side:
                case 'l':
                    return square.left.owner_ID == -1
                case 'r':
                    return square.right.owner_ID == -1
                case 't':
                    return square.top.owner_ID == -1
                case 'd':
                    return square.down.owner_ID == -1
        return False

    def copy(self):
        copied_instance = Pipopipette(self.__WIDTH, self.__HEIGHT)
        copied_instance.list_square = [square.copy() for square in self.list_square]
        return copied_instance