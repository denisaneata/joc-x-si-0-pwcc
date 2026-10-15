#!/usr/bin/env python3
"""Punctul de intrare principal pentru Jocul X și 0 (Tic-Tac-Toe)."""

import sys
from game.game_controller import GameController


def show_instructions() -> None:
    """Afiseaza instructiunile de joc."""
    print("""
============================================================
              📖 CUM SE JOACĂ X ȘI 0
============================================================
1. Tabla are 9 căsuțe numerotate de la 1 la 9:
      1 │ 2 │ 3
     ───┼───┼───
      4 │ 5 │ 6
     ───┼───┼───
      7 │ 8 │ 9

2. Fiecare jucător alege pe rând o poziție disponibilă tastând
   numărul căsuței corespunzătoare.
3. Primul jucător care reușește să așeze 3 simboluri identice
   pe o linie, o coloană sau o diagonală CÂȘTIGĂ runda!
4. Dacă toate cele 9 căsuțe se ocupă fără un câștigător, partida
   se termină la EGALITATE (REMIZĂ).
5. În timpul jocului poți tasta 'q' pentru a reveni la meniu.
============================================================
""")
    input("Apasă Enter pentru a reveni la meniul principal...")


def main_menu() -> None:
    """Afișează meniul principal și gestionează selecția utilizatorului."""
    controller = GameController()

    while True:
        print("""
╔══════════════════════════════════════════╗
║              JOCUL X ȘI 0                ║
║           (Console Tic-Tac-Toe)          ║
╚══════════════════════════════════════════╝
  [1]  2 Jucători (Local PvP)
  [2]  Tu vs Calculator - Ușor (Casual)
  [3]  Tu vs Calculator - Mediu (Inteligent)
  [4]  Tu vs Calculator - Imbatabil (Minimax AI)
  [5]  Instrucțiuni de joc
  [6]  🌐 Pornește Serverul Web (Interfață Grafică)
  [0]  Ieșire (Exit)
""")
        choice = input("Selectează o opțiune [0-6]: ").strip()

        if choice == '1':
            controller.play_pvp()
        elif choice == '2':
            controller.play_vs_ai(difficulty="easy")
        elif choice == '3':
            controller.play_vs_ai(difficulty="medium")
        elif choice == '4':
            controller.play_vs_ai(difficulty="hard")
        elif choice == '5':
            show_instructions()
        elif choice == '6':
            from server import start_server
            start_server()
        elif choice in ['0', 'q', 'exit', 'quit']:
            print("\nMulțumim pentru joc! La revedere! 👋\n")
            sys.exit(0)
        else:
            print("⚠️ Opțiune invalidă! Alege o cifră între 0 și 6.")



if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nJoc întrerupt. La revedere! 👋")
        sys.exit(0)
