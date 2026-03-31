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
    let savingScore = false;

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

    function loadTargetFromBackend() {
        fetch("/api/mouse-objectiu")
            .then((response) => response.json())
            .then((data) => {
                currentTarget = data.objectiu;
                targetFigure.textContent = currentTarget;
            })
            .catch(() => {
                currentTarget = null;
                targetFigure.textContent = "Error";
                showStatus("No he pogut carregar la ronda.", "error");
            });
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
        saveScore();
    }

    function startRound() {
        if (!gameStarted || timeLeft <= 0) {
            return;
        }

        roundActive = true;
        resetFigures();
        loadTargetFromBackend();
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
        savingScore = false;
        timeLeft = GAME_DURATION;
        gameStarted = true;
        updateScore();
        updateTimer();
        startButton.textContent = "Reiniciar partida";
        startTimer();
        startRound();
    }

    function saveScore() {
        if (savingScore) {
            return;
        }

        savingScore = true;

        fetch("/api/guardar-resultat-rato", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                punts: score
            })
        })
            .then((response) => response.json())
            .then((data) => {
                showStatus(data.missatge, "info");
            })
            .catch(() => {
                showStatus(`Temps esgotat. Puntuacio final: ${score} punts.`, "info");
            });
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

            roundActive = false;

            fetch("/api/mouse-validar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    objectiu: currentTarget,
                    seleccionada: figure.dataset.label
                })
            })
                .then((response) => response.json())
                .then((data) => {
                    resetFigures();
                    figure.style.transform = "scale(1.03)";
                    figure.style.outline = data.correcte
                        ? "3px solid rgba(20, 184, 166, 0.85)"
                        : "3px solid rgba(236, 72, 153, 0.85)";

                    if (data.correcte) {
                        score += data.punts;
                        updateScore();
                        showStatus(`Correcte! Has trobat ${figure.dataset.label}.`, "success");
                    } else {
                        showStatus(
                            `Incorrecte. Has clicat ${figure.dataset.label}. La correcta era ${currentTarget}.`,
                            "error"
                        );
                    }

                    window.setTimeout(() => {
                        startRound();
                    }, 900);
                })
                .catch(() => {
                    showStatus("No he pogut validar la figura.", "error");
                    window.setTimeout(() => {
                        startRound();
                    }, 900);
                });
        });
    });

    updateScore();
    updateTimer();
});
