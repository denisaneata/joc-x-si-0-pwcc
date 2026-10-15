"""Teste unitare pentru logica AI."""

import random
import unittest
from game.board import Board
from game.ai import get_easy_move, get_medium_move, get_hard_move


class TestAI(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_easy_move(self) -> None:
        self.board.make_move(0, 'X')
        move = get_easy_move(self.board)
        self.assertIn(move, self.board.available_moves())
        self.assertNotEqual(move, 0)

    def test_medium_winning_move(self) -> None:
        # AI has 0 and 1, should pick 2 to win
        self.board.make_move(0, 'O')
        self.board.make_move(1, 'O')
        self.board.make_move(3, 'X')
        self.board.make_move(4, 'X')
        move = get_medium_move(self.board, ai_symbol='O', human_symbol='X')
        self.assertEqual(move, 2)

    def test_medium_blocking_move(self) -> None:
        # Human has 0 and 1, AI should block at 2
        self.board.make_move(0, 'X')
        self.board.make_move(1, 'X')
        self.board.make_move(4, 'O')
        move = get_medium_move(self.board, ai_symbol='O', human_symbol='X')
        self.assertEqual(move, 2)

    def test_hard_ai_takes_immediate_win(self) -> None:
        # AI is 'X', positions 0 and 1 occupied, should take 2
        self.board.make_move(0, 'X')
        self.board.make_move(1, 'X')
        self.board.make_move(3, 'O')
        self.board.make_move(4, 'O')
        move = get_hard_move(self.board, ai_symbol='X', human_symbol='O')
        self.assertEqual(move, 2)

    def test_hard_ai_blocks_opponent_win(self) -> None:
        # Opponent is 'O' with 3 and 4, AI must block at 5
        self.board.make_move(3, 'O')
        self.board.make_move(4, 'O')
        self.board.make_move(0, 'X')
        move = get_hard_move(self.board, ai_symbol='X', human_symbol='O')
        self.assertEqual(move, 5)

    def test_hard_ai_never_loses_against_random(self) -> None:
        """Simulam 20 de partide in care AI-ul joaca impotriva unui oponent aleator."""
        for _ in range(20):
            board = Board()
            # Randomly decide who starts
            ai_symbol = random.choice(['X', 'O'])
            human_symbol = 'O' if ai_symbol == 'X' else 'X'
            current_turn = 'X'

            while not board.is_game_over():
                if current_turn == ai_symbol:
                    move = get_hard_move(board, ai_symbol, human_symbol)
                else:
                    move = random.choice(board.available_moves())
                board.make_move(move, current_turn)
                current_turn = 'O' if current_turn == 'X' else 'X'

            winner = board.check_winner()
            # Hard AI should NEVER lose
            self.assertNotEqual(winner, human_symbol, f"Hard AI a pierdut impotriva oponentului random!")


if __name__ == '__main__':
    unittest.main()
