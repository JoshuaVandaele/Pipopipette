from random import choice
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
        # List of checked sides: dict[side, list[square_id]]
        checked_sides: dict[str, list[int]] = {'l': [], 'r': [], 't': [], 'd': []}
        width: int = gameplay.pipopipette.WIDTH
        
        for square in gameplay.pipopipette.list_square:
            if square.square_owner == -1:
                if square.left.owner_ID == -1 and (square.ID not in checked_sides["l"]):
                    checked_sides["r"].append(square.ID-1)
                    yield square.ID, 'l'
                if square.top.owner_ID == -1 and (square.ID not in checked_sides["t"]):
                    checked_sides["d"].append(square.ID-width)
                    yield square.ID, 't'
                if square.right.owner_ID == -1 and (square.ID not in checked_sides["r"]):
                    checked_sides["l"].append(square.ID+1)
                    yield square.ID, 'r'
                if square.down.owner_ID == -1 and (square.ID not in checked_sides["d"]):
                    checked_sides["t"].append(square.ID+width)
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
    def move_minmax(gameplay: PipopipetteGameplay, depth: int = 2) -> tuple[None, None] | tuple[int, str]:
        """Pick a move for the AI to play by simulating the next moves

        Args:
            gameplay (PipopipetteGameplay): Game to play on
            depth (int): Maximum depth to search

        Returns:
            tuple[None, None]|tuple[int, str]: Resulting square and side
        """
        memo = {}

        def max_value(gameplay: PipopipetteGameplay, depth: int, alpha: float, beta: float) -> float:
            key = (gameplay.pipopipette, depth, "max")
            if key in memo:
                return memo[key]

            if depth == 0 or gameplay.game_over():
                memo[key] = PipopipetteAI.evaluate(gameplay)
                return memo[key]

            value = float('-inf')
            for move in PipopipetteAI.__list_moves(gameplay):
                next_state = PipopipetteAI.get_next_state(gameplay, *move)
                value = max(value, min_value(next_state, depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            memo[key] = value
            return value

        def min_value(gameplay: PipopipetteGameplay, depth: int, alpha: float, beta: float) -> float:
            key = (gameplay.pipopipette, depth, "min")
            if key in memo:
                return memo[key]

            if depth == 0 or gameplay.game_over():
                memo[key] = PipopipetteAI.evaluate(gameplay)
                return memo[key]

            value = float('inf')
            for move in PipopipetteAI.__list_moves(gameplay):
                next_state = PipopipetteAI.get_next_state(gameplay, *move)
                value = min(value, max_value(next_state, depth - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            memo[key] = value
            return value

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

        # Compute the evaluation score based on the above factors
        score = (ai_score*2) - opponent_score

        return score

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