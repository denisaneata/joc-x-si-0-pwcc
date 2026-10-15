# Jocul X și 0 (Tic-Tac-Toe) în Python

O implementare consolă completă, modernă și interactivă a clasicului joc **X și 0** (Tic-Tac-Toe), realizată în Python 3 fără dependențe externe.

---

## 🎮 Caracteristici

- **Moduri de joc**:
  - **2 Jucători (Local PvP)**: Joacă pe rând de la aceeași tastatură, cu nume personalizate.
  - **Jucător vs Calculator (AI)**:
    - **Ușor (Easy)**: Calculatorul alege mutări aleatorii.
    - **Mediu (Medium)**: Calculatorul urmărește oportunități de victorie și blochează mutările tale cheie.
    - **Imbatabil (Hard - Minimax)**: Algoritm complet de Minimax – imposibil de învins (fie câștigă, fie remiză).
- **Afișaj intuitiv**: Fiecare celulă liberă afișează numărul corespunzător (1–9) pentru o alegere rapidă.
- **Tabelă de scor persistentă pe parcursul sesiunii** (Victorii Jucător 1, Victorii Jucător 2 / AI, Remize).
- **Validare robustă**: Previne mutările pe celule deja ocupate sau valori nevalide.
- **Suport ANSI**: Culori pentru simboluri (albastru pentru X, roșu pentru O, linii subtile pentru grilă).

---

## 🚀 Rulare

Pentru a porni jocul:

```bash
python3 main.py
```

### Controale în joc:
- Tastează o cifră de la **`1`** la **`9`** pentru a plasa simbolul în căsuța dorită:
  ```text
    1 │ 2 │ 3
   ───┼───┼───
    4 │ 5 │ 6
   ───┼───┼───
    7 │ 8 │ 9
  ```
- În orice moment al jocului, poți tasta **`q`** pentru a te întoarce la meniul principal.

---

## 🧪 Rulare Teste Unitare

Proiectul include o suită completă de teste unitare care validează stările tablei, condițiile de victorie și invulnerabilitatea inteligenței artificiale Minimax:

```bash
python3 -m unittest discover -v
```

---

## 📁 Structura Proiectului

```text
joc_x_si_0/
├── game/
│   ├── __init__.py
│   ├── board.py            # Logica tablei de 3x3, verificare victorie, randare
│   ├── ai.py               # Algoritmi AI (Ușor, Mediu, Minimax)
│   └── game_controller.py  # Controlerul partidei, scorul și interacțiunea
├── tests/
│   ├── __init__.py
│   ├── test_board.py       # Teste pentru mecanică și verificări de victorie
│   └── test_ai.py          # Teste pentru strategiile AI și Minimax
├── main.py                 # Meniul principal consolă
└── README.md               # Documentație
```
