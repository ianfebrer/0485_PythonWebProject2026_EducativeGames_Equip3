document.addEventListener('DOMContentLoaded', () => {
    // 1. Agafem tots els elements de l'HTML que necessitem
    const btnStart = document.getElementById('btn-start');
    const fraseDisplay = document.getElementById('frase-display');
    const typingInput = document.getElementById('typing-input');
    const errorsDisplay = document.getElementById('errors-display');
    const progressDisplay = document.getElementById('progress-display');
    const resultMessage = document.getElementById('result-message');

    // Variables per controlar la partida
    let fraseActual = "";
    let errorsTotals = 0;
    let lletresCorrectes = 0;

    // 2. Quan fem clic al botó "Començar Partida"
    btnStart.addEventListener('click', () => {
        // Reiniciem els marcadors
        errorsTotals = 0;
        errorsDisplay.innerText = "0";
        resultMessage.innerText = "";
        typingInput.value = "";
        
        // Demanem una frase aleatòria al nostre Python (Flask)
        fetch('/api/get-frase')
            .then(response => response.json())
            .then(data => {
                fraseActual = data.frase;
                
                // Buidem la caixa i posem cada lletra dins d'un <span> per poder pintar-les individualment
                fraseDisplay.innerHTML = '';
                fraseActual.split('').forEach(lletra => {
                    let span = document.createElement('span');
                    span.innerText = lletra;
                    fraseDisplay.appendChild(span);
                });

                progressDisplay.innerText = `0/${fraseActual.length}`;
                
                // Activem l'input perquè l'usuari pugui començar a escriure
                typingInput.disabled = false;
                typingInput.focus();
                btnStart.disabled = true;
                btnStart.innerText = "Jugant...";
            });
    });

    // 3. Cada vegada que l'usuari prem una tecla a l'input
    typingInput.addEventListener('input', (event) => {
        const arraySpans = fraseDisplay.querySelectorAll('span');
        const lletresEscrites = typingInput.value.split('');
        
        lletresCorrectes = 0;

        // Comparem el que ha escrit amb la frase original, lletra a lletra
        arraySpans.forEach((span, index) => {
            const caracterEscrit = lletresEscrites[index];

            if (caracterEscrit == null) {
                // Encara no ha arribat a aquesta lletra (li traiem els colors)
                span.className = '';
            } else if (caracterEscrit === span.innerText) {
                // Lletra correcta! (Aplica la classe CSS verda/teal)
                span.className = 'lletra-correcta';
                lletresCorrectes++;
            } else {
                // Lletra incorrecta! (Aplica la classe CSS vermella)
                span.className = 'lletra-incorrecta';
            }
        });

        // Si l'usuari acaba d'afegir una lletra nova i està malament, sumem un error
        if (event.inputType === 'insertText') {
            let ultimaPosicio = lletresEscrites.length - 1;
            if (lletresEscrites[ultimaPosicio] !== arraySpans[ultimaPosicio].innerText) {
                errorsTotals++;
                errorsDisplay.innerText = errorsTotals;
            }
        }

        // Actualitzem el comptador de lletres (Exemple: 15/40)
        progressDisplay.innerText = `${lletresEscrites.length}/${fraseActual.length}`;

        // 4. Comprovem si ha acabat d'escriure tota la frase
        if (lletresEscrites.length === fraseActual.length) {
            // Només deixem acabar si no hi ha cap lletra en vermell (ha de corregir-ho)
            const hiHaErrors = document.querySelectorAll('.lletra-incorrecta').length > 0;
            
            if (!hiHaErrors) {
                acabarJoc();
            }
        }
    });

    // 5. Funció que s'executa quan s'ha completat la frase correctament
    function acabarJoc() {
        typingInput.disabled = true; // Bloquegem l'input
        btnStart.disabled = false;
        btnStart.innerText = "Tornar a jugar";

        // Enviem les dades al Python perquè calculi la puntuació i guardi la partida
        fetch('/api/guardar-resultat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correctes: lletresCorrectes,
                incorrectes: errorsTotals
            })
        })
        .then(response => response.json())
        .then(data => {
            // Mostrem el missatge que ens retorna el Python (Ex: "Has aconseguit 250 punts!")
            resultMessage.innerText = data.missatge;
        })
        .catch(error => console.error("Error guardant resultat:", error));
    }
});