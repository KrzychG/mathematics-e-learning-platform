document.addEventListener('DOMContentLoaded', () => {
    let config = {};
    const configEl = document.getElementById('examConfigData');
    if (configEl && configEl.textContent) {
        try {
            config = JSON.parse(configEl.textContent) || {};
        } catch (err) {
            console.warn('Nie udało się odczytać konfiguracji egzaminu:', err);
        }
    }
    const totalTasks = config.totalTasks || 20;
    let currentTaskIndex = 1;
    const saveUrl = config.saveUrl || '';
    const csrfToken = config.csrfToken || '';
    const graphSpecs = config.graphSpecs || {};
    const btnPrev = document.getElementById('btnPrevTask');
    const btnNext = document.getElementById('btnNextTask');
    const answeredCounter = document.getElementById('answeredCounter');
    const pills = document.querySelectorAll('.exam-pill-btn');
    const taskCards = document.querySelectorAll('.exam-task-card');
    const optionInputs = document.querySelectorAll('.exam-option-input');
    const btnOpenSubmitModal = document.getElementById('btnOpenSubmitModal');
    const modalUnansweredAlert = document.getElementById('modalUnansweredAlert');
    const modalUnansweredCount = document.getElementById('modalUnansweredCount');
    // Przełączanie widoku zadania na arkuszu egzaminu
    // Pokazuje wybraną kartę, aktualizuje kafelki nawigacji, odpala renderowanie KaTeX
    // oraz montuje wykres funkcyjny.
    function goToTask(index) {
        if (index < 1 || index > totalTasks) return;
        currentTaskIndex = index;
        taskCards.forEach(card => card.style.display = 'none');
        const activeCard = document.getElementById(`taskCard_${index}`);
        if (activeCard) {
            activeCard.style.display = 'block';
            window.renderMathInElement?.(activeCard);
        }
        pills.forEach(pill => {
            const pillIdx = parseInt(pill.getAttribute('data-task-index'), 10);
            pill.classList.toggle('active', pillIdx === index);
        });
        if (btnPrev) btnPrev.disabled = (index === 1);
        if (btnNext) btnNext.disabled = (index === totalTasks);
        if (activeCard) {
            const taskId = activeCard.getAttribute('data-task-id');
            window.MathGraph?.mountTaskGraph(`examGraphContainer_${taskId}`, graphSpecs[taskId], { force: false });
        }
    }
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            const idx = parseInt(pill.getAttribute('data-task-index'), 10);
            goToTask(idx);
        });
    });
    if (btnPrev) {
        btnPrev.addEventListener('click', () => goToTask(currentTaskIndex - 1));
    }
    if (btnNext) {
        btnNext.addEventListener('click', () => goToTask(currentTaskIndex + 1));
    }
    optionInputs.forEach(input => {
        input.addEventListener('change', () => {
            const taskId = input.getAttribute('data-task-id');
            const taskIndex = input.getAttribute('data-task-index');
            const selectedOption = input.value;
            const currentPill = document.getElementById(`pillTask_${taskIndex}`);
            if (currentPill) {
                currentPill.classList.add('answered');
            }
            updateAnsweredCount();
            // Autozapis wyboru w tle uczeń nie traci postępu przy zerwaniu sieci czy odświeżeniu
            if (saveUrl && csrfToken && window.apiFetchJson) {
                window.apiFetchJson(saveUrl, {
                    method: 'POST',
                    csrfToken,
                    body: {
                        task_id: taskId,
                        selected_option: selectedOption
                    }
                }).catch(err => {
                    console.warn('Błąd podczas autozapisu odpowiedzi:', err);
                });
            }
        });
    });
    function updateAnsweredCount() {
        const answeredTasks = new Set();
        document.querySelectorAll('.exam-option-input:checked').forEach(inp => {
            answeredTasks.add(inp.getAttribute('data-task-id'));
        });
        if (answeredCounter) {
            answeredCounter.textContent = answeredTasks.size;
        }
        return answeredTasks.size;
    }
    if (btnOpenSubmitModal) {
        btnOpenSubmitModal.addEventListener('click', () => {
            const answeredCount = updateAnsweredCount();
            const unanswered = totalTasks - answeredCount;
            if (modalUnansweredAlert) {
                modalUnansweredAlert.classList.toggle('d-none', unanswered <= 0);
            }
            if (modalUnansweredCount && unanswered > 0) {
                modalUnansweredCount.textContent = unanswered;
            }
        });
    }
    document.addEventListener('keydown', (e) => {
        const tag = (e.target.tagName || '').toLowerCase();
        if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
        const modal = document.getElementById('confirmSubmitModal');
        if (modal && modal.classList.contains('show')) return;
        if (e.key === 'ArrowLeft') {
            goToTask(currentTaskIndex - 1);
        } else if (e.key === 'ArrowRight') {
            goToTask(currentTaskIndex + 1);
        } else if (['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'].includes(e.key)) {
            const letter = e.key.toUpperCase();
            const activeCard = document.getElementById(`taskCard_${currentTaskIndex}`);
            if (activeCard) {
                const radio = activeCard.querySelector(`.exam-option-input[value="${letter}"]`);
                if (radio) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event('change'));
                }
            }
        }
    });
    goToTask(1);
    updateAnsweredCount();
});
