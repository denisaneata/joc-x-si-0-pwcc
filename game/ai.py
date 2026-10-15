"""Modul pentru logica inteligentei artificiale (AI) la X și 0."""

import random
from typing import Optional
from game.board import Board


def get_easy_move(board: Board) -> int:
    """Alege o pozitie libera la intamplare."""
    moves = board.available_moves()
    if not moves:
        raise ValueError("Nu exista mutari disponibile.")
    return random.choice(moves)


def get_medium_move(board: Board, ai_symbol: str, human_symbol: str) -> int:
    """
    Nivel mediu de dificultate:
    1. Verifica daca AI-ul poate castiga imediat.
    2. Blocheaza mutarea castigatoare a adversarului.
    3. Ocupa centrul daca e liber.
    4. Ocupa un colt la intamplare.
    5. Alege orice alta pozitie libera.
    """
    available = board.available_moves()
    if not available:
        raise ValueError("Nu exista mutari disponibile.")

    # 1. Verifica daca AI-ul poate castiga imediat
    for move in available:
        board.make_move(move, ai_symbol)
        if board.check_winner() == ai_symbol:
            board.undo_move(move)
            return move
        board.undo_move(move)

    # 2. Blocheaza victoria adversarului
    for move in available:
        board.make_move(move, human_symbol)
        if board.check_winner() == human_symbol:
            board.undo_move(move)
            return move
        board.undo_move(move)

    # 3. Preia centrul daca e disponibil
    if 4 in available:
        return 4

    # 4. Preia un colt disponibil
    corners = [m for m in [0, 2, 6, 8] if m in available]
    if corners:
        return random.choice(corners)

    # 5. Oricare alta mutare
    return random.choice(available)


def _minimax(board: Board, depth: int, is_maximizing: bool, ai_symbol: str, human_symbol: str) -> int:
    """Functie recursiva Minimax pentru evaluarea starilor de joc."""
    winner = board.check_winner()
    if winner == ai_symbol:
        return 10 - depth
    elif winner == human_symbol:
        return depth - 10
    elif board.is_full():
        return 0

    if is_maximizing:
        best_score = -999
        for move in board.available_moves():
            board.make_move(move, ai_symbol)
            score = _minimax(board, depth + 1, False, ai_symbol, human_symbol)
            board.undo_move(move)
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = 999
        for move in board.available_moves():
            board.make_move(move, human_symbol)
            score = _minimax(board, depth + 1, True, ai_symbol, human_symbol)
            board.undo_move(move)
            if score < best_score:
                best_score = score
        return best_score


def get_hard_move(board: Board, ai_symbol: str, human_symbol: str) -> int:
    """
    Nivel imbatabil (Minimax):
    Exploreaza toate miscarile posibile si alege mutarea optima.
    """
    available = board.available_moves()
    if not available:
        raise ValueError("Nu exista mutari disponibile.")

    # Daca tabla este complet goala, luam direct centrul sau un colt pentru viteza
    if len(available) == 9:
        return random.choice([0, 2, 4, 6, 8])

    best_score = -999
    best_moves = []

    for move in available:
        board.make_move(move, ai_symbol)
        score = _minimax(board, depth=0, is_maximizing=False, ai_symbol=ai_symbol, human_symbol=human_symbol)
        board.undo_move(move)

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
