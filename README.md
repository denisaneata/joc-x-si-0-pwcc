# Jocul X și 0 (Tic-Tac-Toe)

O implementare completă, modernă și interactivă a clasicului joc **X și 0** (Tic-Tac-Toe), disponibilă atât ca **Aplicație Web cu Interfață Grafică**, cât și ca **Joc în Consolă**, realizată fără dependențe externe în Python 3 și JavaScript nativ.

---

## 🎮 Caracteristici

- **Interfață Web Modernă & Responsivă** (`index.html`, `style.css`, `app.js`):
  - Design elegant (dark theme cu accente neon cyan pentru X și coral/roz pentru O).
  - Efecte sonore dinamice generate prin **Web Audio API** (fără fișiere audio externe necesare).
  - Linie animată SVG peste combinația câștigătoare și explozie festivă de confetti.
  - Tabela de scoruri salvată local (localStorage).
  - Suport complet tastatură (tastele **1–9** pentru celule, tasta **R** pentru restart).
- **Moduri de joc**:
  - **2 Jucători (Local PvP)**: Joc pe rând pe același dispozitiv.
  - **Jucător vs Calculator (AI)**:
    - **Ușor (Easy)**: Calculatorul alege mutări aleatorii.
    - **Mediu (Medium)**: Urmărește oportunități directe de victorie și blochează mutările adversarului.
    - **Imbatabil (Hard - Minimax)**: Algoritm complet de Minimax – imposibil de învins (fie câștigă, fie remiză).
- **Versiune Consolă** (`main.py`):
  - Complet colorată cu coduri ANSI, tabelă de scor pe sesiune și meniu interactiv.

---

## 🚀 Rulare Server Web Local

Pentru a porni serverul web local și a juca în browser:

```bash
python3 server.py
```

Apoi deschide în orice browser web adresa:
👉 **`http://localhost:8000`** (sau `http://127.0.0.1:8000`)

---

## 💻 Rulare Joc în Consolă

Pentru a juca versiunea clasică direct în terminal:

```bash
python3 main.py
```

De asemenea, din meniul din consolă poți selecta opțiunea `[6]` pentru a porni direct serverul web!

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
├── index.html              # Interfața Web HTML5 a jocului
├── style.css               # Stiluri CSS responsive, temă neon modernă, animații
├── app.js                  # Logica jocului în browser (AI Minimax, Web Audio, Confetti)
├── server.py               # Server web HTTP local în Python (fără dependențe externe)
├── main.py                 # Meniul principal în consolă
├── game/
│   ├── __init__.py
│   ├── board.py            # Logica tablei de 3x3 în Python
│   ├── ai.py               # Algoritmi AI în Python (Ușor, Mediu, Minimax)
│   └── game_controller.py  # Controler partidă consolă
├── tests/
│   ├── __init__.py
│   ├── test_board.py       # Teste pentru mecanică și verificări de victorie
│   └── test_ai.py          # Teste pentru strategiile AI și Minimax
└── README.md               # Documentație completă
```
