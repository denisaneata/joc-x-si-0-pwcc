"""Controlerul principal pentru fluxul jocului X și 0."""

import time
from typing import Dict, Optional
from game.board import Board
from game.ai import get_easy_move, get_medium_move, get_hard_move


class GameController:
    """Gestioneaza logica rundelor, scorul si interactiunea cu utilizatorii."""

    def __init__(self) -> None:
        self.board = Board()
        self.scores: Dict[str, int] = {
            "player1": 0,
            "player2_or_ai": 0,
            "draws": 0,
        }

    def reset_scores(self) -> None:
        """Reseteaza tabela de scor."""
        self.scores = {"player1": 0, "player2_or_ai": 0, "draws": 0}

    def display_score(self, p1_name: str, p2_name: str) -> None:
        """Afiseaza scorul curent."""
        print("\n" + "=" * 40)
        print(f"📊 SCOR: {p1_name}: {self.scores['player1']}  |  {p2_name}: {self.scores['player2_or_ai']}  |  Remize: {self.scores['draws']}")
        print("=" * 40 + "\n")

    def get_player_move(self, player_name: str, symbol: str) -> Optional[int]:
        """
        Cere jucatorului sa aleaga o pozitie (1-9).
        Permite 'q' pentru a reveni la meniu.
        Returneaza indexul intern (0-8) sau None pentru iesire.
        """
        while True:
            try:
                user_input = input(f"👉 {player_name} ({symbol}), alege pozitia (1-9) sau 'q' pentru meniu: ").strip()
                if user_input.lower() in ['q', 'quit', 'exit']:
                    return None

                pos = int(user_input) - 1
                if pos < 0 or pos > 8:
                    print("⚠️  Pozitie invalida! Alege un numar intre 1 si 9.")
                    continue

                if self.board.cells[pos] is not None:
                    print("⚠️  Pozitia este deja ocupata! Alege o casuta libera.")
                    continue

                return pos
            except ValueError:
                print("⚠️  Te rugam sa introduci o cifra valida intre 1 si 9.")

    def play_pvp(self) -> None:
        """Modul: 2 Jucatori (Local)."""
        print("\n--- Modul 2 Jucatori (PvP) ---")
        p1_name = input("Numele Jucatorului 1 (X) [implicit Jucator 1]: ").strip() or "Jucator 1"
        p2_name = input("Numele Jucatorului 2 (O) [implicit Jucator 2]: ").strip() or "Jucator 2"
        self.reset_scores()

        while True:
            self.board.reset()
            current_turn = 'X'
            current_player = p1_name

            print(f"\n🚀 Incepe o noua partida intre {p1_name} (X) si {p2_name} (O)!")

            while not self.board.is_game_over():
                print(self.board.render())
                pos = self.get_player_move(current_player, current_turn)
                if pos is None:
                    print("\nPartida a fost intrerupta. Revenire la meniu...")
                    return

                self.board.make_move(pos, current_turn)

                # Schimba randul
                if current_turn == 'X':
                    current_turn = 'O'
                    current_player = p2_name
                else:
                    current_turn = 'X'
                    current_player = p1_name

            # Sfarsitul partidei
            print(self.board.render())
            winner = self.board.check_winner()
            if winner == 'X':
                print(f"🎉 Felicitari! {p1_name} (X) a castigat runda!")
                self.scores["player1"] += 1
            elif winner == 'O':
                print(f"🎉 Felicitari! {p2_name} (O) a castigat runda!")
                self.scores["player2_or_ai"] += 1
            else:
                print("🤝 Remiza! Niciun castigator.")
                self.scores["draws"] += 1

            self.display_score(p1_name, p2_name)

            replay = input("Vreti sa jucati din nou? (d/n) [implicit d]: ").strip().lower()
            if replay in ['n', 'nu', 'no']:
                break

    def play_vs_ai(self, difficulty: str) -> None:
        """Modul: Jucator vs Calculator (AI)."""
        diff_names = {
            "easy": "Usor",
            "medium": "Mediu",
            "hard": "Imbatabil (Minimax)",
        }
        diff_label = diff_names.get(difficulty, "Normal")
        print(f"\n--- Modul: Tu vs AI ({diff_label}) ---")

        p_name = input("Numele tau [implicit Jucator]: ").strip() or "Jucator"
        ai_name = f"Calculator ({diff_label})"

        # Alegere simbol
        symbol_choice = ""
        while symbol_choice not in ['x', 'o']:
            symbol_choice = input(f"{p_name}, vrei sa joci cu X sau cu O? (X incepe primul): ").strip().lower()
            if not symbol_choice:
                symbol_choice = 'x'

        human_symbol = symbol_choice.upper()
        ai_symbol = 'O' if human_symbol == 'X' else 'X'

        self.reset_scores()

        while True:
            self.board.reset()
            current_turn = 'X'

            print(f"\n🚀 Incepe runda! {p_name} ({human_symbol}) vs {ai_name} ({ai_symbol})")

            while not self.board.is_game_over():
                print(self.board.render())

                if current_turn == human_symbol:
                    pos = self.get_player_move(p_name, human_symbol)
                    if pos is None:
                        print("\nPartida a fost intrerupta. Revenire la meniu...")
                        return
                    self.board.make_move(pos, human_symbol)
                else:
                    print(f"🤖 {ai_name} se gandeste...")
                    time.sleep(0.4)  # Mic efect vizual pentru realism

                    if difficulty == "easy":
                        ai_move = get_easy_move(self.board)
                    elif difficulty == "medium":
                        ai_move = get_medium_move(self.board, ai_symbol, human_symbol)
                    else:
                        ai_move = get_hard_move(self.board, ai_symbol, human_symbol)

                    self.board.make_move(ai_move, ai_symbol)
                    print(f"🤖 Calculatorul a ales pozitia {ai_move + 1}.")

                current_turn = 'O' if current_turn == 'X' else 'X'

            # Sfarsit runda
            print(self.board.render())
            winner = self.board.check_winner()
            if winner == human_symbol:
                print(f"🎉 Bravo, {p_name}! Ai castigat!")
                self.scores["player1"] += 1
            elif winner == ai_symbol:
                print(f"🤖 {ai_name} a castigat aceasta runda!")
                self.scores["player2_or_ai"] += 1
            else:
                print("🤝 Egalitate! A fost o partida stransa.")
                self.scores["draws"] += 1

            self.display_score(p_name, ai_name)

            replay = input("Vrei sa joci inca o partida? (d/n) [implicit d]: ").strip().lower()
            if replay in ['n', 'nu', 'no']:
                break
