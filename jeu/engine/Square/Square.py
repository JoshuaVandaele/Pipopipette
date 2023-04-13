# <========== import ==========>

from __future__ import annotations
from typing import Final
from jeu.engine.Square.Segment import Segment

# <========== class ==========>


class Square:
    # <----- init ----->

    def __init__(self: Square, id=0) -> None:
        self.__left: Segment = Segment()
        self.__right: Segment = Segment()
        self.__top: Segment = Segment()
        self.__down: Segment = Segment()
        self.__square_owner: int = -1
        self.__ID: Final[int] = id

    # <----- getter ----->

    @property
    def left(self: Square) -> Segment:
        return self.__left

    @property
    def right(self: Square) -> Segment:
        return self.__right

    @property
    def top(self: Square) -> Segment:
        return self.__top

    @property
    def down(self: Square) -> Segment:
        return self.__down

    @property
    def square_owner(self: Square) -> int:
        return self.__square_owner

    @property
    def ID(self: Square) -> int:
        return self.__ID

    # <----- setter ----->

    @left.setter
    def left(self: Square, owner_ID: int) -> bool | None:
        self.__left.owner_ID = owner_ID
        if (
            self.__right.owner_ID != -1
            and self.__top.owner_ID != -1
            and self.__down.owner_ID != -1
        ):
            self.__square_owner = owner_ID

    @right.setter
    def right(self: Square, owner_ID: int) -> bool | None:
        self.__right.owner_ID = owner_ID
        if (
            self.__left.owner_ID != -1
            and self.__top.owner_ID != -1
            and self.__down.owner_ID != -1
        ):
            self.__square_owner = owner_ID

    @top.setter
    def top(self: Square, owner_ID: int) -> bool | None:
        self.__top.owner_ID = owner_ID
        if (
            self.__right.owner_ID != -1
            and self.__left.owner_ID != -1
            and self.__down.owner_ID != -1
        ):
            self.__square_owner = owner_ID

    @down.setter
    def down(self: Square, owner_ID: int) -> bool | None:
        self.__down.owner_ID = owner_ID
        if (
            self.__right.owner_ID != -1
            and self.__top.owner_ID != -1
            and self.__left.owner_ID != -1
        ):
            self.__square_owner = owner_ID

    @square_owner.setter
    def square_owner(self: Square, owner_ID: int) -> None:
        self.__square_owner = owner_ID

    # <----- str ----->

    def __str__(self: Square) -> str:
        return f"[id:{self.__ID}(l:{self.__left.owner_ID},r:{self.__right.owner_ID},t{self.__top.owner_ID},d{self.__down.owner_ID}), owner:{self.__square_owner}]"

    def copy(self: Square) -> Square:
        """Returns a deep copy of this Square instance.

        Returns:
            Square: Copied instance
        """
        new_square = Square(id=self.ID)
        new_square.left.owner_ID = self.left.owner_ID
        new_square.right.owner_ID = self.right.owner_ID
        new_square.top.owner_ID = self.top.owner_ID
        new_square.down.owner_ID = self.down.owner_ID
        new_square.square_owner = self.square_owner
        return new_square
