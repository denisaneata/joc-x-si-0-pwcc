"""Teste unitare pentru clasa Board."""

import unittest
from game.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_initial_board(self) -> None:
        self.assertEqual(len(self.board.available_moves()), 9)
        self.assertFalse(self.board.is_full())
        self.assertIsNone(self.board.check_winner())
        self.assertFalse(self.board.is_game_over())

    def test_make_move(self) -> None:
        self.assertTrue(self.board.make_move(0, 'X'))
        self.assertEqual(self.board.cells[0], 'X')
        self.assertEqual(len(self.board.available_moves()), 8)
        # Cannot move on the same cell
        self.assertFalse(self.board.make_move(0, 'O'))
        # Cannot move out of bounds
        self.assertFalse(self.board.make_move(-1, 'X'))
        self.assertFalse(self.board.make_move(9, 'X'))

    def test_undo_move(self) -> None:
        self.board.make_move(4, 'O')
        self.assertEqual(self.board.cells[4], 'O')
        self.board.undo_move(4)
        self.assertIsNone(self.board.cells[4])
        self.assertIn(4, self.board.available_moves())

    def test_row_wins(self) -> None:
        for row in [(0, 1, 2), (3, 4, 5), (6, 7, 8)]:
            b = Board()
            for pos in row:
                b.make_move(pos, 'X')
            self.assertEqual(b.check_winner(), 'X')
            self.assertTrue(b.is_game_over())

    def test_column_wins(self) -> None:
        for col in [(0, 3, 6), (1, 4, 7), (2, 5, 8)]:
            b = Board()
            for pos in col:
                b.make_move(pos, 'O')
            self.assertEqual(b.check_winner(), 'O')
            self.assertTrue(b.is_game_over())

    def test_diagonal_wins(self) -> None:
        for diag in [(0, 4, 8), (2, 4, 6)]:
            b = Board()
            for pos in diag:
                b.make_move(pos, 'X')
            self.assertEqual(b.check_winner(), 'X')
            self.assertTrue(b.is_game_over())

    def test_draw(self) -> None:
        # X O X
        # X O O
        # O X X
        moves = [
            (0, 'X'), (1, 'O'), (2, 'X'),
            (3, 'X'), (4, 'O'), (5, 'O'),
            (6, 'O'), (7, 'X'), (8, 'X')
        ]
        for pos, sym in moves:
            self.board.make_move(pos, sym)

        self.assertTrue(self.board.is_full())
        self.assertIsNone(self.board.check_winner())
        self.assertTrue(self.board.is_game_over())

    def test_render_contains_symbols(self) -> None:
        self.board.make_move(0, 'X')
        self.board.make_move(4, 'O')
        rendered = self.board.render(colored=False)
        self.assertIn('X', rendered)
        self.assertIn('O', rendered)
        self.assertIn('2', rendered)  # Empty cell displays its number


if __name__ == '__main__':
    unittest.main()
