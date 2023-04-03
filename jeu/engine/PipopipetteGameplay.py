# <========== Import ==========>

from __future__ import annotations
from typing import Final
from jeu.engine.Pipopipette import Pipopipette
from jeu.engine.Player.Player import Player

# <========== Class ==========>

class PipopipetteGameplay():
    """
    Class used to manage the players, their score, ect...
    """
    
    # <----- init ----->
    
    def __init__(self: PipopipetteGameplay, list_player_name: list[str], pipopipette: Pipopipette = Pipopipette()) -> None:
        """
        Args:
            listPlayer: A list of players. Should contain a least two Players
            pipopipette: The playground.
        """
        self.__LIST_PLAYER: Final[list[Player]] = [Player(list_player_name[i],i) for i in range(len(list_player_name))]
        self.__pipopipette: Pipopipette = pipopipette
        self.__current_player_ID: int = self.__LIST_PLAYER[0].ID if len(self.__LIST_PLAYER) > 0 else 0
            
    # <----- getter ----->
    
    @property
    def LIST_PLAYER(self: PipopipetteGameplay) -> list[Player]: return self.__LIST_PLAYER
    
    @property
    def pipopipette(self: PipopipetteGameplay) -> Pipopipette: return self.__pipopipette
    
    @property
    def current_player_ID(self: PipopipetteGameplay) -> int: return self.__current_player_ID
    
    # <----- setter ----->
    
    @pipopipette.setter
    def pipopipette(self: PipopipetteGameplay, pipopipette: Pipopipette) -> None: self.__pipopipette = pipopipette
    
    @current_player_ID.setter
    def current_player_ID(self: PipopipetteGameplay, current_player_ID) -> None: self.__current_player_ID = current_player_ID
            
    # <----- nextPlayer ----->
    
    def next_player(self: PipopipetteGameplay) -> None:
        """
        Will switch to another player.
        """
        self.__current_player_ID += 1
        if self.__current_player_ID % len(self.__LIST_PLAYER) == 0: self.__current_player_ID = 0
        
        
    # <----- setPlayerTarget ----->
    
    def set_player_target(self: PipopipetteGameplay, square_ID: int, side: str) -> None:
        """
        Used to take a Segment of a square
        Args:
            squareID: The Square to edit
            side: Wich side to manage ? 'l'; 'r', 't', or 'd'.
        """
        if self.__pipopipette.valid_target(square_ID, side):
            self.__pipopipette.set_side(square_ID, side, self.current_player_ID)
    
    def get_score(self: PipopipetteGameplay) -> list[int]:
        result: list[int] = [0]*len(self.__LIST_PLAYER)
        for square in self.__pipopipette.list_square:
            if square.square_owner >= 0:
                result[square.square_owner] += 1
        return result

    # <----- gameOver ----->
    
    def game_over(self: PipopipetteGameplay) -> bool:
        """
        Check if there is a Square without an owner to check if the game ended or not.
        Returns:
            Boolean - True if game finished, False of not

        """
        total_score: int = sum(self.get_score())

        return total_score >= self.pipopipette.HEIGHT * self.pipopipette.WIDTH

    def game_state_string(self) -> str:
        return ''.join(str(square.square_owner) for square in self.pipopipette.list_square)
    
    def copy(self):
        """
        Returns a deep copy of this PipopipetteGameplay instance.
        """
        new_gameplay = PipopipetteGameplay([], pipopipette=self.__pipopipette.copy())
        new_gameplay.__current_player_ID = self.__current_player_ID

        # Make a deep copy of each player object in the list
        new_gameplay.__LIST_PLAYER = [] # type: ignore
        for player in self.__LIST_PLAYER:
            new_player = Player(player.NAME, player.ID, player.score.value)
            new_gameplay.__LIST_PLAYER.append(new_player)

        return new_gameplay