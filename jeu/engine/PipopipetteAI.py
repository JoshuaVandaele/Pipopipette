import time
from random import choice, shuffle
from typing import Generator

from jeu.engine.PipopipetteGameplay import PipopipetteGameplay


class PipopipetteAI:
    """Class which will be used to control the AI's logic.
    """

    @staticmethod
    def __list_moves(gameplay: PipopipetteGameplay) -> Generator[tuple[int, str], None, None]:
        """Iterator to go through the valid moves the player can go through

        Args:
            gameplay (PipopipetteGameplay): Game to check for

        Yields:
            Generator[tuple[int, str], None, None]: Generator
        """
        for square in gameplay.pipopipette.list_square:
            if square.square_owner == -1:
                if square.left.owner_ID == -1:
                    yield square.ID, 'l'
                if square.top.owner_ID == -1:
                    yield square.ID, 't'
                if square.right.owner_ID == -1:
                    yield square.ID, 'r'
                if square.down.owner_ID == -1:
                    yield square.ID, 'd'

    @staticmethod
    def move_random(gameplay: PipopipetteGameplay) -> tuple[None, None] | tuple[int, str]:
        """Pick a random move for the AI to play

        Args:
            gameplay (PipopipetteGameplay): Game to play on

        Returns:
            tuple[None, None]|tuple[int, str]: Resulting square and side
        """
        moves = [move for move in PipopipetteAI.__list_moves(gameplay)]
        if moves:
            return choice(moves)
        else:
            return (None, None)

    @staticmethod
    def move_minmax(gameplay: PipopipetteGameplay, depth: int = 2, time_limit: float = 5.0) -> tuple[None, None] | tuple[int, str]:
        """Pick a move for the AI to play by simulating the next moves

        Args:
            gameplay (PipopipetteGameplay): Game to play on
            depth (int): Maximum depth to search
            time_limit (float): Maximum time limit for search, in seconds

        Returns:
            tuple[None, None]|tuple[int, str]: Resulting square and side
        """
        def max_value(gameplay: PipopipetteGameplay, depth: int, alpha: float, beta: float) -> float:
            if depth == 0 or gameplay.game_over():
                return PipopipetteAI.evaluate(gameplay)

            value = float('-inf')
            for move in PipopipetteAI.__list_moves(gameplay):
                next_state = PipopipetteAI.get_next_state(gameplay, *move)
                value = max(value, min_value(
                    next_state, depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        def min_value(gameplay: PipopipetteGameplay, depth: int, alpha: float, beta: float) -> float:
            if depth == 0 or gameplay.game_over():
                return PipopipetteAI.evaluate(gameplay)

            value = float('inf')
            for move in PipopipetteAI.__list_moves(gameplay):
                next_state = PipopipetteAI.get_next_state(gameplay, *move)
                value = min(value, max_value(next_state, depth - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

        start_time = time.monotonic()
        best_move = (None, None)
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in PipopipetteAI.__list_moves(gameplay):
            next_state = PipopipetteAI.get_next_state(gameplay, *move)
            value = min_value(next_state, depth - 1, alpha, beta)
            if best_value == float('-inf') or value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)

            elapsed_time = time.monotonic() - start_time
            if elapsed_time >= time_limit:
                break
        return best_move

    @staticmethod
    def evaluate(gameplay: PipopipetteGameplay) -> float:
        """Evaluate the game state from the perspective of the AI

        Args:
            gameplay (PipopipetteGameplay): Game to evaluate

        Returns:
            float: Evaluation score
        """
        opponent_score, ai_score = gameplay.get_score()
        potential_squares = len(PipopipetteAI.get_potential_squares(gameplay))

        # Compute the evaluation score based on the above factors
        score = (ai_score*2) - opponent_score + potential_squares

        return score

    @staticmethod
    def get_potential_squares(gameplay: PipopipetteGameplay) -> list[int]:
        """Get the IDs of the squares that could potentially be completed
        by filling a side of the specified square.

        Args:
            gameplay (PipopipetteGameplay): Game to use

        Returns:
            list[int]: IDs of the potential squares that could be completed
        """
        potential_squares = []

        for square in gameplay.pipopipette.list_square:
            if square.square_owner == -1:
                # One side is open
                if [square.left.owner_ID, square.right.owner_ID, square.top.owner_ID, square.down.owner_ID].count(-1) == 1:
                    potential_squares.append(0)
        return potential_squares

    @staticmethod
    def get_next_state(gameplay: PipopipetteGameplay, square_id: int, side: str) -> 'PipopipetteGameplay':
        """Return the next game state after applying a move

        Args:
            square_id (int): ID of the square to play on
            side (str): Side of the square to play on ('l', 't', 'r', or 'd')

        Returns:
            PipopipetteGameplay: New game state
        """
        # Create a copy of the game board
        new_gameplay = gameplay.copy()

        new_gameplay.pipopipette.set_side(square_id, side, new_gameplay.current_player_ID)
        new_gameplay.next_player()

        # Create a new game state object and switch the player
        new_state = new_gameplay
        return new_state