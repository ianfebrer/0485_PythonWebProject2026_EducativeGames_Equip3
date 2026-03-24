document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("start-mouse-game");
    const statusBox = document.getElementById("mouse-game-status");
    const targetFigure = document.getElementById("target-figure");
    const scoreValue = document.getElementById("score-value");
    const timerValue = document.getElementById("timer-value");
    const figures = document.querySelectorAll(".mouse-figure");

    const GAME_DURATION = 30;

    let roundActive = false;
    let score = 0;
    let currentTarget = null;
    let gameStarted = false;
    let timeLeft = GAME_DURATION;
    let timerId = null;

    function showStatus(message, type = "info") {
        statusBox.style.display = "block";
        statusBox.textContent = message;
        statusBox.style.borderLeft = "";
        statusBox.style.background = "";

        if (type === "success") {
            statusBox.style.borderLeft = "4px solid #14b8a6";
            statusBox.style.background = "rgba(20, 184, 166, 0.15)";
        } else if (type === "error") {
            statusBox.style.borderLeft = "4px solid #ec4899";
            statusBox.style.background = "rgba(236, 72, 153, 0.15)";
        } else {
            statusBox.style.borderLeft = "4px solid #6366f1";
            statusBox.style.background = "rgba(99, 102, 241, 0.15)";
        }
    }

    function updateScore() {
        scoreValue.textContent = `${score} punts`;
    }

    function updateTimer() {
        timerValue.textContent = `${timeLeft} s`;
    }

    function resetFigures() {
        figures.forEach((figure) => {
            figure.style.outline = "none";
            figure.style.transform = "";
            figure.style.opacity = "1";
        });
    }

    function pickRandomTarget() {
        const randomIndex = Math.floor(Math.random() * figures.length);
        currentTarget = figures[randomIndex];
        targetFigure.textContent = currentTarget.dataset.label;
    }

    function stopGame() {
        roundActive = false;
        gameStarted = false;
        currentTarget = null;
        if (timerId) {
            window.clearInterval(timerId);
            timerId = null;
        }
        startButton.textContent = "Tornar a jugar";
        resetFigures();
        targetFigure.textContent = "Cap figura";
        showStatus(`Temps esgotat. Puntuacio final: ${score} punts.`, "info");
    }

    function startRound() {
        if (!gameStarted || timeLeft <= 0) {
            return;
        }

        roundActive = true;
        resetFigures();
        pickRandomTarget();
        showStatus("Ronda activa. Fes clic sobre la figura correcta.", "info");
    }

    function startTimer() {
        if (timerId) {
            window.clearInterval(timerId);
        }

        timerId = window.setInterval(() => {
            timeLeft -= 1;
            updateTimer();

            if (timeLeft <= 0) {
                stopGame();
            }
        }, 1000);
    }

    function startGame() {
        score = 0;
        timeLeft = GAME_DURATION;
        gameStarted = true;
        updateScore();
        updateTimer();
        startButton.textContent = "Reiniciar partida";
        startTimer();
        startRound();
    }

    startButton.addEventListener("click", () => {
        startGame();
    });

    figures.forEach((figure) => {
        figure.addEventListener("mouseover", () => {
            if (!roundActive) {
                return;
            }

            resetFigures();
            figure.style.transform = "translateY(-6px) scale(1.03)";
            figure.style.outline = "2px solid rgba(255, 255, 255, 0.22)";
        });

        figure.addEventListener("mouseout", () => {
            if (!roundActive) {
                return;
            }

            resetFigures();
        });

        figure.addEventListener("click", () => {
            if (!gameStarted) {
                showStatus("Primer has de premer 'Comencar ronda'.", "error");
                return;
            }

            if (!roundActive || timeLeft <= 0) {
                return;
            }

            const isCorrect = figure === currentTarget;

            resetFigures();
            figure.style.transform = "scale(1.03)";
            figure.style.outline = isCorrect
                ? "3px solid rgba(20, 184, 166, 0.85)"
                : "3px solid rgba(236, 72, 153, 0.85)";

            if (isCorrect) {
                score += 10;
                updateScore();
                showStatus(`Correcte! Has trobat ${figure.dataset.label}.`, "success");
            } else {
                showStatus(
                    `Incorrecte. Has passat per ${figure.dataset.label}. La correcta era ${currentTarget.dataset.label}.`,
                    "error"
                );
            }

            roundActive = false;

            window.setTimeout(() => {
                startRound();
            }, 900);
        });
    });

    updateScore();
    updateTimer();
});
