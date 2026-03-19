document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("start-mouse-game");
    const statusBox = document.getElementById("mouse-game-status");
    const targetFigure = document.getElementById("target-figure");
    const figures = document.querySelectorAll(".mouse-figure");

    let roundActive = false;
    let score = 0;
    let correctShape = "estrella";
    let correctColor = "roig";

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
        const scoreText = document.querySelector("#start-mouse-game")
            .closest(".auth-box")
            .querySelector("p[style*='font-size: 1.6rem']");
        
        if (scoreText) {
            score.textContent = `${score} punts`;
        }
    }

    function resetFigures() {
        figures.forEach((figure) => {
            figure.style.outline = "none";
            figure.style.transform = "";
        });
    }

    startButton.addEventListener("click", () => {
        roundActive = true;
        resetFigures();
        targetFigure.textContent = "estrella roja";
        showStatus("Ronda activa. Busca la figura correcta.", "info");
    });

    figures.forEach((figure) => {
        figure.addEventListener("mouseover", () => {
            if (!roundActive) {
                showStatus("Primer has de prémer 'Començar ronda'.", "error");
                return;
            }

            const shape = figure.dataset.shape;
            const color = figure.dataset.color;

            resetFigures();
            figure.style.transform = "scale(1.03)";
            figure.style.outline = "3px solid rgba(255,255,255,0.35)";

            if (shape === correctShape && color === correctColor) {
                score += 10;
                updateScore();
                showStatus("Correcte! Has trobat la figura bona.", "success");
                roundActive = false;
            } else {
                showStatus(`Incorrecte. Has passat per ${shape} ${color}.`, "error");
                roundActive = false;
            }
        });
    });
});