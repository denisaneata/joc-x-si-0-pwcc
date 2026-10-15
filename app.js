/**
 * Jocul X și 0 (Tic-Tac-Toe) - Logica Web Client
 */

(function () {
    'use strict';

    // --- Constante și Combinații Câștigătoare ---
    const WINNING_COMBINATIONS = [
        [0, 1, 2], // Linia 1
        [3, 4, 5], // Linia 2
        [6, 7, 8], // Linia 3
        [0, 3, 6], // Coloana 1
        [1, 4, 7], // Coloana 2
        [2, 5, 8], // Coloana 3
        [0, 4, 8], // Diagonala principală
        [2, 4, 6]  // Diagonala secundară
    ];

    // --- Stare Joc ---
    const state = {
        board: Array(9).fill(null),
        currentPlayer: 'X',
        gameActive: true,
        mode: 'ai', // 'ai' | 'pvp'
        difficulty: 'hard', // 'easy' | 'medium' | 'hard'
        humanSymbol: 'X',
        aiSymbol: 'O',
        scores: {
            x: 0,
            o: 0,
            ties: 0
        },
        soundEnabled: true,
        aiThinking: false
    };

    // --- Elemente DOM ---
    const DOM = {
        board: document.getElementById('board'),
        cells: document.querySelectorAll('.cell'),
        statusBanner: document.getElementById('status-banner'),
        statusText: document.getElementById('status-text'),
        cardX: document.getElementById('card-x'),
        cardO: document.getElementById('card-o'),
        cardTies: document.getElementById('card-ties'),
        scoreX: document.getElementById('score-x'),
        scoreO: document.getElementById('score-o'),
        scoreTies: document.getElementById('score-ties'),
        labelX: document.getElementById('label-x'),
        labelO: document.getElementById('label-o'),
        modeAiBtn: document.getElementById('mode-ai'),
        modePvpBtn: document.getElementById('mode-pvp'),
        aiSettings: document.getElementById('ai-settings'),
        diffButtons: document.querySelectorAll('.diff-btn'),
        symbolButtons: document.querySelectorAll('.symbol-btn'),
        btnRestart: document.getElementById('btn-restart'),
        btnResetScore: document.getElementById('btn-reset-score'),
        soundToggle: document.getElementById('sound-toggle'),
        soundIcon: document.getElementById('sound-icon'),
        winningSvg: document.getElementById('winning-line-svg'),
        winningLine: document.getElementById('winning-line'),
        confettiCanvas: document.getElementById('confetti-canvas')
    };

    // --- Generator Sunete (Web Audio API) ---
    class SoundEngine {
        constructor() {
            this.ctx = null;
        }

        init() {
            if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                this.ctx = new AudioCtx();
            }
            if (this.ctx && this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
        }

        playTone(freq, type = 'sine', duration = 0.12, gainVal = 0.15) {
            if (!state.soundEnabled) return;
            try {
                this.init();
                if (!this.ctx) return;

                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = type;
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

                gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start();
                osc.stop(this.ctx.currentTime + duration);
            } catch (e) {
                // AudioContext nu este permis sau a eșuat
            }
        }

        playMoveX() {
            this.playTone(520, 'sine', 0.1, 0.2);
            setTimeout(() => this.playTone(660, 'triangle', 0.12, 0.15), 40);
        }

        playMoveO() {
            this.playTone(440, 'sine', 0.1, 0.2);
            setTimeout(() => this.playTone(330, 'sine', 0.14, 0.15), 40);
        }

        playWin() {
            if (!state.soundEnabled) return;
            const notes = [440, 554, 659, 880]; // Cântec de victorie (A4 major chord)
            notes.forEach((freq, idx) => {
                setTimeout(() => {
                    this.playTone(freq, 'triangle', 0.25, 0.2);
                }, idx * 100);
            });
        }

        playDraw() {
            if (!state.soundEnabled) return;
            const notes = [380, 320, 260];
            notes.forEach((freq, idx) => {
                setTimeout(() => {
                    this.playTone(freq, 'sine', 0.2, 0.15);
                }, idx * 120);
            });
        }

        playClick() {
            this.playTone(800, 'sine', 0.05, 0.08);
        }
    }

    const sound = new SoundEngine();

    // --- Efect Confetti ---
    class ConfettiManager {
        constructor(canvas) {
            this.canvas = canvas;
            this.ctx = canvas.getContext('2d');
            this.particles = [];
            this.animationId = null;
            this.resize();
            window.addEventListener('resize', () => this.resize());
        }

        resize() {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        }

        fire() {
            this.particles = [];
            const colors = ['#38bdf8', '#fb7185', '#facc15', '#a855f7', '#34d399', '#ffffff'];
            for (let i = 0; i < 90; i++) {
                this.particles.push({
                    x: this.canvas.width / 2 + (Math.random() - 0.5) * 200,
                    y: this.canvas.height / 2 - 50,
                    vx: (Math.random() - 0.5) * 12,
                    vy: (Math.random() - 0.8) * 14,
                    size: Math.random() * 8 + 4,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    rotation: Math.random() * 360,
                    vRot: (Math.random() - 0.5) * 10,
                    life: 1
                });
            }

            if (!this.animationId) {
                this.render();
            }
        }

        render() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            let activeCount = 0;

            for (let p of this.particles) {
                if (p.life > 0) {
                    activeCount++;
                    p.x += p.vx;
                    p.y += p.vy;
                    p.vy += 0.35; // gravitație
                    p.vx *= 0.98;
                    p.rotation += p.vRot;
                    p.life -= 0.012;

                    this.ctx.save();
                    this.ctx.translate(p.x, p.y);
                    this.ctx.rotate((p.rotation * Math.PI) / 180);
                    this.ctx.fillStyle = p.color;
                    this.ctx.globalAlpha = Math.max(0, p.life);
                    this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
                    this.ctx.restore();
                }
            }

            if (activeCount > 0) {
                this.animationId = requestAnimationFrame(() => this.render());
            } else {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.animationId = null;
            }
        }
    }

    const confetti = new ConfettiManager(DOM.confettiCanvas);

    // --- Persistență Scoruri și Preferințe ---
    function loadSavedState() {
        try {
            const savedScores = localStorage.getItem('tictactoe_scores');
            if (savedScores) {
                const parsed = JSON.parse(savedScores);
                state.scores.x = parsed.x || 0;
                state.scores.o = parsed.o || 0;
                state.scores.ties = parsed.ties || 0;
            }

            const savedSound = localStorage.getItem('tictactoe_sound');
            if (savedSound !== null) {
                state.soundEnabled = savedSound === 'true';
            }
        } catch (e) {
            console.warn('Nu s-au putut încărca setările locale:', e);
        }
        updateScoreboard();
        updateSoundButton();
    }

    function saveState() {
        try {
            localStorage.setItem('tictactoe_scores', JSON.stringify(state.scores));
            localStorage.setItem('tictactoe_sound', String(state.soundEnabled));
        } catch (e) {
            // Nu blocăm jocul
        }
    }

    // --- Interfață și Actualizări DOM ---
    function updateScoreboard() {
        DOM.scoreX.textContent = state.scores.x;
        DOM.scoreO.textContent = state.scores.o;
        DOM.scoreTies.textContent = state.scores.ties;
    }

    function updateSoundButton() {
        DOM.soundIcon.textContent = state.soundEnabled ? '🔊' : '🔇';
    }

    function updateLabels() {
        if (state.mode === 'ai') {
            if (state.humanSymbol === 'X') {
                DOM.labelX.textContent = 'Tu (X)';
                DOM.labelO.textContent = 'Calculator (O)';
            } else {
                DOM.labelX.textContent = 'Calculator (X)';
                DOM.labelO.textContent = 'Tu (O)';
            }
        } else {
            DOM.labelX.textContent = 'Jucător 1 (X)';
            DOM.labelO.textContent = 'Jucător 2 (O)';
        }
    }

    function updateTurnIndicators() {
        DOM.cardX.classList.remove('active-turn');
        DOM.cardO.classList.remove('active-turn');

        if (!state.gameActive) return;

        if (state.currentPlayer === 'X') {
            DOM.cardX.classList.add('active-turn');
        } else {
            DOM.cardO.classList.add('active-turn');
        }
    }

    function updateStatusMessage(customText = null, type = 'normal') {
        DOM.statusBanner.className = 'status-banner';

        if (customText) {
            DOM.statusText.innerHTML = customText;
            if (type === 'win-x') DOM.statusBanner.classList.add('win-x');
            if (type === 'win-o') DOM.statusBanner.classList.add('win-o');
            if (type === 'draw') DOM.statusBanner.classList.add('draw');
            return;
        }

        if (state.mode === 'ai' && state.currentPlayer === state.aiSymbol) {
            DOM.statusText.innerHTML = `Calculatorul <strong>(${state.aiSymbol})</strong> gândește... 🤖`;
        } else {
            const playerLabel = (state.mode === 'ai')
                ? `Rândul tău (<strong>${state.humanSymbol}</strong>)`
                : `Rândul jucătorului <strong>${state.currentPlayer}</strong>`;
            DOM.statusText.innerHTML = playerLabel;
        }
    }

    function drawWinningLine(combination) {
        if (!combination) return;

        const cellA = DOM.cells[combination[0]].getBoundingClientRect();
        const cellC = DOM.cells[combination[2]].getBoundingClientRect();
        const boardRect = DOM.board.getBoundingClientRect();

        const x1 = cellA.left + cellA.width / 2 - boardRect.left;
        const y1 = cellA.top + cellA.height / 2 - boardRect.top;
        const x2 = cellC.left + cellC.width / 2 - boardRect.left;
        const y2 = cellC.top + cellC.height / 2 - boardRect.top;

        DOM.winningLine.setAttribute('x1', x1);
        DOM.winningLine.setAttribute('y1', y1);
        DOM.winningLine.setAttribute('x2', x2);
        DOM.winningLine.setAttribute('y2', y2);

        const winner = state.board[combination[0]];
        DOM.winningSvg.className = `winning-line-svg active ${winner.toLowerCase()}`;
    }

    function clearWinningLine() {
        DOM.winningSvg.className = 'winning-line-svg';
    }

    // --- Verificări Victorie / Remiză ---
    function checkWinner(board) {
        for (const [a, b, c] of WINNING_COMBINATIONS) {
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return { winner: board[a], combination: [a, b, c] };
            }
        }
        return null;
    }

    function isBoardFull(board) {
        return board.every(cell => cell !== null);
    }

    function getAvailableMoves(board) {
        const moves = [];
        for (let i = 0; i < 9; i++) {
            if (board[i] === null) moves.push(i);
        }
        return moves;
    }

    // --- Algoritmi AI (Ușor, Mediu, Imbatabil Minimax) ---
    function getEasyMove(board) {
        const available = getAvailableMoves(board);
        return available[Math.floor(Math.random() * available.length)];
    }

    function getMediumMove(board, aiSymbol, humanSymbol) {
        const available = getAvailableMoves(board);

        // 1. Verifică dacă AI poate câștiga dintr-o singură mutare
        for (const move of available) {
            board[move] = aiSymbol;
            if (checkWinner(board)?.winner === aiSymbol) {
                board[move] = null;
                return move;
            }
            board[move] = null;
        }

        // 2. Blochează o mutare câștigătoare a adversarului
        for (const move of available) {
            board[move] = humanSymbol;
            if (checkWinner(board)?.winner === humanSymbol) {
                board[move] = null;
                return move;
            }
            board[move] = null;
        }

        // 3. Preia centrul dacă este liber
        if (available.includes(4)) return 4;

        // 4. Preia un colț dacă este disponibil
        const corners = [0, 2, 6, 8].filter(c => available.includes(c));
        if (corners.length > 0) {
            return corners[Math.floor(Math.random() * corners.length)];
        }

        // 5. Orice poziție rămasă
        return available[Math.floor(Math.random() * available.length)];
    }

    function minimax(board, depth, isMaximizing, aiSymbol, humanSymbol) {
        const winResult = checkWinner(board);
        if (winResult) {
            return winResult.winner === aiSymbol ? 10 - depth : depth - 10;
        }
        if (isBoardFull(board)) return 0;

        const available = getAvailableMoves(board);

        if (isMaximizing) {
            let maxEval = -1000;
            for (const move of available) {
                board[move] = aiSymbol;
                const score = minimax(board, depth + 1, false, aiSymbol, humanSymbol);
                board[move] = null;
                if (score > maxEval) maxEval = score;
            }
            return maxEval;
        } else {
            let minEval = 1000;
            for (const move of available) {
                board[move] = humanSymbol;
                const score = minimax(board, depth + 1, true, aiSymbol, humanSymbol);
                board[move] = null;
                if (score < minEval) minEval = score;
            }
            return minEval;
        }
    }

    function getHardMove(board, aiSymbol, humanSymbol) {
        const available = getAvailableMoves(board);

        // Dacă tabla este goală, alegem centrul sau un colț direct pentru viteză
        if (available.length === 9) {
            const starters = [0, 2, 4, 6, 8];
            return starters[Math.floor(Math.random() * starters.length)];
        }

        let bestScore = -1000;
        let bestMoves = [];

        for (const move of available) {
            board[move] = aiSymbol;
            const score = minimax(board, 0, false, aiSymbol, humanSymbol);
            board[move] = null;

            if (score > bestScore) {
                bestScore = score;
                bestMoves = [move];
            } else if (score === bestScore) {
                bestMoves.push(move);
            }
        }

        return bestMoves[Math.floor(Math.random() * bestMoves.length)];
    }

    function computeAIMove() {
        if (!state.gameActive || state.currentPlayer !== state.aiSymbol) return;

        state.aiThinking = true;
        updateStatusMessage();

        // Mică pauză realistă pentru a simula gândirea
        setTimeout(() => {
            if (!state.gameActive) {
                state.aiThinking = false;
                return;
            }

            let move;
            if (state.difficulty === 'easy') {
                move = getEasyMove(state.board);
            } else if (state.difficulty === 'medium') {
                move = getMediumMove(state.board, state.aiSymbol, state.humanSymbol);
            } else {
                move = getHardMove(state.board, state.aiSymbol, state.humanSymbol);
            }

            state.aiThinking = false;
            if (typeof move === 'number' && state.board[move] === null) {
                handleCellClick(move);
            }
        }, 400);
    }

    // --- Execuție Mutare ---
    function handleCellClick(index) {
        if (!state.gameActive || state.board[index] !== null) return;
        if (state.mode === 'ai' && state.currentPlayer === state.aiSymbol && !state.aiThinking) return;

        const symbol = state.currentPlayer;
        state.board[index] = symbol;

        // Actualizare vizuală celulă
        const cell = DOM.cells[index];
        cell.textContent = symbol;
        cell.classList.add(symbol.toLowerCase(), 'filled');
        cell.disabled = true;

        // Sunet
        if (symbol === 'X') sound.playMoveX();
        else sound.playMoveO();

        // Verifică victorie
        const winData = checkWinner(state.board);
        if (winData) {
            handleGameWin(winData.winner, winData.combination);
            return;
        }

        // Verifică remiză
        if (isBoardFull(state.board)) {
            handleGameDraw();
            return;
        }

        // Schimbă tura
        state.currentPlayer = state.currentPlayer === 'X' ? 'O' : 'X';
        updateTurnIndicators();
        updateStatusMessage();

        // Dacă e rândul AI-ului, declanșăm mutarea acestuia
        if (state.mode === 'ai' && state.currentPlayer === state.aiSymbol) {
            computeAIMove();
        }
    }

    function handleGameWin(winner, combination) {
        state.gameActive = false;
        updateTurnIndicators();

        // Marcăm căsuțele câștigătoare
        combination.forEach(idx => {
            DOM.cells[idx].classList.add('winning-cell', winner.toLowerCase());
        });
        drawWinningLine(combination);

        // Actualizăm scorul
        if (winner === 'X') state.scores.x++;
        else state.scores.o++;
        saveState();
        updateScoreboard();

        // Mesaje și sunete
        let message;
        if (state.mode === 'ai') {
            if (winner === state.humanSymbol) {
                message = `🎉 Felicitări! Ai câștigat!`;
                confetti.fire();
                sound.playWin();
            } else {
                message = `🤖 Calculatorul a câștigat runda!`;
                sound.playDraw();
            }
        } else {
            message = `🎉 Jucătorul <strong>${winner}</strong> a câștigat!`;
            confetti.fire();
            sound.playWin();
        }

        updateStatusMessage(message, `win-${winner.toLowerCase()}`);
    }

    function handleGameDraw() {
        state.gameActive = false;
        updateTurnIndicators();
        state.scores.ties++;
        saveState();
        updateScoreboard();

        sound.playDraw();
        updateStatusMessage('🤝 Partidă terminată la egalitate!', 'draw');
    }

    // --- Resetare Rând / Scor ---
    function restartGame() {
        state.board = Array(9).fill(null);
        state.gameActive = true;
        state.aiThinking = false;
        state.currentPlayer = 'X'; // X întotdeauna începe la X și 0

        clearWinningLine();

        DOM.cells.forEach(cell => {
            cell.textContent = '';
            cell.className = 'cell';
            cell.disabled = false;
        });

        updateLabels();
        updateTurnIndicators();
        updateStatusMessage();

        // Dacă e mod AI și omul a ales 'O', AI-ul este 'X' și trebuie să mute primul!
        if (state.mode === 'ai' && state.aiSymbol === 'X') {
            computeAIMove();
        }
    }

    function resetScore() {
        sound.playClick();
        state.scores.x = 0;
        state.scores.o = 0;
        state.scores.ties = 0;
        saveState();
        updateScoreboard();
        restartGame();
    }

    // --- Gestionare Evenimente Utilizator ---
    function setupEventListeners() {
        // Clic pe celule
        DOM.cells.forEach(cell => {
            cell.addEventListener('click', (e) => {
                if (state.aiThinking) return;
                const index = parseInt(cell.dataset.index, 10);
                handleCellClick(index);
            });
        });

        // Schimbare Mod de Joc (AI vs PvP)
        DOM.modeAiBtn.addEventListener('click', () => {
            if (state.mode === 'ai') return;
            sound.playClick();
            state.mode = 'ai';
            DOM.modeAiBtn.classList.add('active');
            DOM.modePvpBtn.classList.remove('active');
            DOM.aiSettings.style.display = 'flex';
            restartGame();
        });

        DOM.modePvpBtn.addEventListener('click', () => {
            if (state.mode === 'pvp') return;
            sound.playClick();
            state.mode = 'pvp';
            DOM.modePvpBtn.classList.add('active');
            DOM.modeAiBtn.classList.remove('active');
            DOM.aiSettings.style.display = 'none';
            restartGame();
        });

        // Dificultate AI
        DOM.diffButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                sound.playClick();
                DOM.diffButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.difficulty = btn.dataset.diff;
                restartGame();
            });
        });

        // Simbol Jucător (X sau O)
        DOM.symbolButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                sound.playClick();
                DOM.symbolButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.humanSymbol = btn.dataset.symbol;
                state.aiSymbol = state.humanSymbol === 'X' ? 'O' : 'X';
                restartGame();
            });
        });

        // Buton Runda Nouă
        DOM.btnRestart.addEventListener('click', () => {
            sound.playClick();
            restartGame();
        });

        // Buton Reset Scor
        DOM.btnResetScore.addEventListener('click', () => {
            if (confirm('Ești sigur că vrei să resetezi scorul la 0 - 0?')) {
                resetScore();
            }
        });

        // Sunet On/Off
        DOM.soundToggle.addEventListener('click', () => {
            state.soundEnabled = !state.soundEnabled;
            saveState();
            updateSoundButton();
            if (state.soundEnabled) sound.playClick();
        });

        // Suport Tastatură (1-9 pentru celule, R pentru restart)
        window.addEventListener('keydown', (e) => {
            // Nu captura când e deschis un input sau modal
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            const key = e.key;
            if (key >= '1' && key <= '9') {
                const index = parseInt(key, 10) - 1;
                if (!state.aiThinking && state.board[index] === null) {
                    handleCellClick(index);
                }
            } else if (key === 'r' || key === 'R') {
                restartGame();
            }
        });

        // Re-calibrare linie SVG la redimensionare ecran
        window.addEventListener('resize', () => {
            const winData = checkWinner(state.board);
            if (winData) {
                drawWinningLine(winData.combination);
            }
        });
    }

    // --- Pornire Aplicație ---
    function init() {
        loadSavedState();
        setupEventListeners();
        restartGame();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
