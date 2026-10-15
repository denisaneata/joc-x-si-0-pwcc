"""Modul pentru tabla jocului X și 0."""

from typing import List, Optional, Tuple


class Board:
    """Reprezintă tabla de joc 3x3 pentru X și 0."""

    WINNING_COMBINATIONS = [
        (0, 1, 2),  # Linia 1
        (3, 4, 5),  # Linia 2
        (6, 7, 8),  # Linia 3
        (0, 3, 6),  # Coloana 1
        (1, 4, 7),  # Coloana 2
        (2, 5, 8),  # Coloana 3
        (0, 4, 8),  # Diagonala principala
        (2, 4, 6),  # Diagonala secundara
    ]

    # Coduri ANSI pentru colorare placuta in consola
    COLOR_RESET = "\033[0m"
    COLOR_BOLD = "\033[1m"
    COLOR_X = "\033[94m"      # Albastru deschis pentru X
    COLOR_O = "\033[91m"      # Rosu/Coral pentru O
    COLOR_GRID = "\033[90m"   # Gri pentru linii
    COLOR_HINT = "\033[37m"   # Gri deschis pentru numerele pozitiilor libere

    def __init__(self) -> None:
        self.cells: List[Optional[str]] = [None] * 9

    def reset(self) -> None:
        """Reseteaza tabla de joc."""
        self.cells = [None] * 9

    def make_move(self, position: int, symbol: str) -> bool:
        """
        Plaseaza simbolul pe pozitia specificata (0-8).
        Returneaza True daca mutarea a fost valida, False altfel.
        """
        if 0 <= position < 9 and self.cells[position] is None:
            self.cells[position] = symbol.upper()
            return True
        return False

    def undo_move(self, position: int) -> None:
        """Anuleaza mutarea de pe pozitia specificata (util pentru Minimax)."""
        if 0 <= position < 9:
            self.cells[position] = None

    def available_moves(self) -> List[int]:
        """Returneaza o lista cu indecsii pozitiilor libere (0-8)."""
        return [i for i, cell in enumerate(self.cells) if cell is None]

    def is_full(self) -> bool:
        """Verifica daca tabla este plina."""
        return all(cell is not None for cell in self.cells)

    def check_winner(self) -> Optional[str]:
        """
        Returneaza 'X' sau 'O' daca exista un castigator, altfel None.
        """
        for a, b, c in self.WINNING_COMBINATIONS:
            if self.cells[a] is not None and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def get_winning_line(self) -> Optional[Tuple[int, int, int]]:
        """Returneaza tuplul celor 3 pozitii castigatoare, sau None."""
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            if self.cells[a] is not None and self.cells[a] == self.cells[b] == self.cells[c]:
                return combo
        return None

    def is_game_over(self) -> bool:
        """Returneaza True daca jocul s-a incheiat (victorie sau remiza)."""
        return self.check_winner() is not None or self.is_full()

    def render(self, colored: bool = True) -> str:
        """
        Genereaza o reprezentare grafica a tablei.
        Pozitiile necompletate afiseaza cifra corespunzatoare (1-9) ca ghidaj.
        """
        formatted_cells = []
        for i in range(9):
            val = self.cells[i]
            if val == 'X':
                if colored:
                    formatted_cells.append(f"{self.COLOR_BOLD}{self.COLOR_X}X{self.COLOR_RESET}")
                else:
                    formatted_cells.append("X")
            elif val == 'O':
                if colored:
                    formatted_cells.append(f"{self.COLOR_BOLD}{self.COLOR_O}O{self.COLOR_RESET}")
                else:
                    formatted_cells.append("O")
            else:
                pos_str = str(i + 1)
                if colored:
                    formatted_cells.append(f"{self.COLOR_HINT}{pos_str}{self.COLOR_RESET}")
                else:
                    formatted_cells.append(pos_str)

        grid_line = f"{self.COLOR_GRID}───┼───┼───{self.COLOR_RESET}" if colored else "───┼───┼───"
        sep = f"{self.COLOR_GRID}│{self.COLOR_RESET}" if colored else "│"

        c = formatted_cells
        board_str = (
            f"\n"
            f"  {c[0]} {sep} {c[1]} {sep} {c[2]}\n"
            f" {grid_line}\n"
            f"  {c[3]} {sep} {c[4]} {sep} {c[5]}\n"
            f" {grid_line}\n"
            f"  {c[6]} {sep} {c[7]} {sep} {c[8]}\n"
        )
        return board_str
