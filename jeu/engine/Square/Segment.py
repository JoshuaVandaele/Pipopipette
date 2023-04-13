# <========== import ==========>

from __future__ import annotations

# <========== class ==========>


class Segment:
    """
    Used to represent a segment, placed by a player.
    """

    # <----- init ----->

    def __init__(self: Segment, owner_ID: int = -1) -> None:
        """
        Create a new Segment
        Args:
            ownerID (int): The ID of the user who placed this. Default to -1 for no owner
        """
        self.__owner_ID: int = owner_ID

    # <----- getter ----->

    @property
    def owner_ID(self: Segment) -> int:
        return self.__owner_ID

    # <----- setter ----->

    @owner_ID.setter
    def owner_ID(self: Segment, owner_ID: int) -> None:
        self.__owner_ID = owner_ID
