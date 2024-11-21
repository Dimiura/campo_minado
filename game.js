const difficulties = {
    easy: { size: 8, mines: 10, name: 'Fácil' },
    medium: { size: 12, mines: 30, name: 'Médio' },
    hard: { size: 16, mines: 60, name: 'Difícil' }
};

let board = [];
let gameStarted = false;
let startTime;
let timer;
let currentDifficulty;
let highScores = loadHighScores();

function loadHighScores() {
    const scores = localStorage.getItem('minesweeperScores');
    return scores ? JSON.parse(scores) : {
        easy: Infinity,
        medium: Infinity,
        hard: Infinity
    };
}

function saveHighScores() {
    localStorage.setItem('minesweeperScores', JSON.stringify(highScores));
    updateHighScoresDisplay();
}

function updateHighScoresDisplay() {
    const scoresDiv = document.getElementById('high-scores');
    scoresDiv.innerHTML = Object.entries(difficulties).map(([key, diff]) => {
        const score = highScores[key];
        const scoreText = score === Infinity ? 'Sem recorde' : score.toFixed(1) + 's';
        return `<p>🏆 ${diff.name}: ${scoreText}</p>`;
    }).join('');
}

function startGame(difficulty) {
    currentDifficulty = difficulty;
    const { size, mines } = difficulties[difficulty];
    
    document.getElementById('menu').classList.remove('active');
    document.getElementById('menu').classList.add('hidden');
    document.getElementById('game-board').classList.remove('hidden');
    document.getElementById('game-board').classList.add('active');
    
    createBoard(size, mines);
    gameStarted = false;
    if (timer) clearInterval(timer);
    document.getElementById('timer').textContent = '⏱️ Tempo: 0.0s';
}

function createBoard(size, mines) {
    const boardDiv = document.getElementById('board');
    boardDiv.style.gridTemplateColumns = `repeat(${size}, 30px)`;
    boardDiv.innerHTML = '';
    
    board = Array(size).fill().map(() => Array(size).fill(0));
    
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.addEventListener('click', () => handleClick(i, j));
            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                handleRightClick(i, j);
            });
            boardDiv.appendChild(cell);
        }
    }
}

function placeMines(size, mines, firstRow, firstCol) {
    const positions = [];
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (i !== firstRow || j !== firstCol) {
                positions.push([i, j]);
            }
        }
    }
    
    for (let i = 0; i < mines; i++) {
        const index = Math.floor(Math.random() * positions.length);
        const [row, col] = positions.splice(index, 1)[0];
        board[row][col] = 'X';
    }
    
    calculateNumbers(size);
}

function calculateNumbers(size) {
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (board[i][j] !== 'X') {
                let count = 0;
                for (let di = -1; di <= 1; di++) {
                    for (let dj = -1; dj <= 1; dj++) {
                        const ni = i + di;
                        const nj = j + dj;
                        if (ni >= 0 && ni < size && nj >= 0 && nj < size && board[ni][nj] === 'X') {
                            count++;
                        }
                    }
                }
                board[i][j] = count;
            }
        }
    }
}

function handleClick(row, col) {
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains('revealed') || cell.classList.contains('flag')) {
        return;
    }

    if (!gameStarted) {
        gameStarted = true;
        startTime = Date.now();
        timer = setInterval(updateTimer, 100);
        const { size, mines } = difficulties[currentDifficulty];
        placeMines(size, mines, row, col);
    }
    
    if (board[row][col] === 'X') {
        gameOver();
        return;
    }
    
    reveal(row, col);
    
    if (checkWin()) {
        winGame();
    }
}

function reveal(row, col) {
    const { size } = difficulties[currentDifficulty];
    if (row < 0 || row >= size || col < 0 || col >= size) {
        return;
    }
    
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains('revealed')) {
        return;
    }
    
    cell.classList.add('revealed');
    
    if (board[row][col] === 0) {
        cell.textContent = '';
        for (let di = -1; di <= 1; di++) {
            for (let dj = -1; dj <= 1; dj++) {
                reveal(row + di, col + dj);
            }
        }
    } else {
        cell.textContent = board[row][col];
        cell.classList.add(`number-${board[row][col]}`);
    }
}

function handleRightClick(row, col) {
    if (!gameStarted) return;
    
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains('revealed')) {
        return;
    }
    
    if (cell.classList.contains('flag')) {
        cell.classList.remove('flag');
        cell.textContent = '';
    } else {
        cell.classList.add('flag');
        cell.textContent = '🚩';
    }
}

function gameOver() {
    clearInterval(timer);
    const { size } = difficulties[currentDifficulty];
    
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (board[i][j] === 'X') {
                const cell = document.querySelector(`[data-row="${i}"][data-col="${j}"]`);
                cell.classList.add('mine');
                cell.textContent = '💣';
            }
        }
    }
    
    setTimeout(() => {
        alert('Game Over!');
        returnToMenu();
    }, 100);
}

function winGame() {
    clearInterval(timer);
    const elapsed = (Date.now() - startTime) / 1000;
    
    if (elapsed < highScores[currentDifficulty]) {
        highScores[currentDifficulty] = elapsed;
        saveHighScores();
    }
    
    setTimeout(() => {
        alert(`Parabéns! Você venceu!\nTempo: ${elapsed.toFixed(1)} segundos`);
        returnToMenu();
    }, 100);
}

function checkWin() {
    const { size } = difficulties[currentDifficulty];
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const cell = document.querySelector(`[data-row="${i}"][data-col="${j}"]`);
            if (board[i][j] !== 'X' && !cell.classList.contains('revealed')) {
                return false;
            }
        }
    }
    return true;
}

function updateTimer() {
    const elapsed = (Date.now() - startTime) / 1000;
    document.getElementById('timer').textContent = `⏱️ Tempo: ${elapsed.toFixed(1)}s`;
}

function returnToMenu() {
    if (timer) clearInterval(timer);
    document.getElementById('game-board').classList.remove('active');
    document.getElementById('game-board').classList.add('hidden');
    document.getElementById('menu').classList.remove('hidden');
    document.getElementById('menu').classList.add('active');
    updateHighScoresDisplay();
}

// Initialize high scores display
updateHighScoresDisplay();