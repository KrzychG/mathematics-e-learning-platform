document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('practicePageRoot');
    if (!root) return;
    let isLoading = root.dataset.isLoading === 'true';
    const isForceNewInitial = root.dataset.forceNew === 'true';
    const isRandomMode = root.dataset.randomMode === 'true';
    const baseGetTaskUrl = root.dataset.fetchUrl || '';
    const defaultCategory = root.dataset.defaultCategory || 'Bez kategorii';
    const loadingCard = document.getElementById('loadingCard');
    const taskCard = document.getElementById('taskCard');
    const errorCard = document.getElementById('errorCard');
    const errorMessage = document.getElementById('errorMessage');
    const retryBtn = document.getElementById('retryFetchBtn');
    const randomTopicMeta = document.getElementById('randomTopicMeta');
    const randomCategoryName = document.getElementById('randomCategoryName');
    const randomTopicName = document.getElementById('randomTopicName');
    const randomTopicTheoryLink = document.getElementById('randomTopicTheoryLink');
    const taskQuestionBox = document.getElementById('taskQuestionBox');
    const taskIdInput = document.getElementById('taskIdInput');
    const difficultyBadge = document.getElementById('difficultyBadge');
    const optionsContainer = document.getElementById('optionsContainer');
    const optionsGrid = document.getElementById('optionsGrid');
    const answerForm = document.getElementById('answerForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const taskGraphWrapper = document.getElementById('taskGraphWrapper');
    const taskGraphContainer = document.getElementById('taskGraphContainer');
    const attachOptionCardListeners = () => {
        const optionCards = document.querySelectorAll('.option-card');
        const optionRadios = document.querySelectorAll('.option-radio');
        const updateSelectedStyles = () => {
            optionCards.forEach(card => {
                const radio = card.querySelector('.option-radio');
                if (radio && radio.checked) {
                    card.classList.add('selected');
                } else {
                    card.classList.remove('selected');
                }
            });
        };
        optionRadios.forEach(radio => {
            radio.addEventListener('change', updateSelectedStyles);
        });
        optionCards.forEach(card => {
            card.addEventListener('click', () => {
                const radio = card.querySelector('.option-radio');
                if (radio) {
                    radio.checked = true;
                    updateSelectedStyles();
                }
            });
        });
        updateSelectedStyles();
    };
    attachOptionCardListeners();
    const setSubmitState = (isSubmitting) => {
        if (!submitBtn || !btnText || !btnSpinner) return;
        btnText.textContent = isSubmitting ? 'Weryfikacja odpowiedzi...' : 'Zatwierdź odpowiedź';
        btnSpinner.classList.toggle('d-none', !isSubmitting);
        submitBtn.disabled = isSubmitting;
    };
    if (answerForm) {
        answerForm.addEventListener('submit', () => setSubmitState(true));
    }
    const renderTaskGraphIfNeeded = (rawSpec) => {
        if (!taskGraphWrapper || !taskGraphContainer) return;
        window.MathGraph?.mountTaskGraph(taskGraphContainer, rawSpec, { wrapper: taskGraphWrapper });
    };
    // Asynchroniczne pobieranie lub generowanie zadania
    const fetchTask = async (forceNew = false) => {
        if (!isLoading && !forceNew) {
            const specEl = document.getElementById('initialTaskGraphSpec');
            if (specEl && taskGraphWrapper && taskGraphContainer) {
                window.MathGraph?.mountTaskGraphFromScript(specEl, taskGraphContainer, { wrapper: taskGraphWrapper });
            }
            window.renderMathInElement?.([taskQuestionBox, optionsGrid]);
            return;
        }
        isLoading = true;
        loadingCard.classList.remove('d-none');
        taskCard.classList.add('d-none');
        errorCard.classList.add('d-none');
        if (isRandomMode && randomTopicMeta && forceNew) {
            randomTopicMeta.classList.add('d-none');
        }
        setSubmitState(false);
        try {
            const requestUrl = baseGetTaskUrl + ((forceNew || isForceNewInitial) ? '?force_new=1' : '');
            const data = await window.apiFetchJson(requestUrl, {
                errorMessage: 'Nie udało się pobrać zadania z serwera.'
            });
            if (!data.success) {
                throw new Error(data.error || 'Nie udało się pobrać zadania z serwera.');
            }
            taskIdInput.value = data.task_id;
            taskQuestionBox.textContent = data.formatted_question ?? data.question ?? '';
            renderTaskGraphIfNeeded(data.graph_spec);
            if (data.difficulty && difficultyBadge) {
                difficultyBadge.textContent = `Poziom trudności: ${data.difficulty} / 5`;
            }
            if (isRandomMode && randomTopicMeta && data.topic_name) {
                if (randomCategoryName) {
                    randomCategoryName.textContent = data.category_name || defaultCategory;
                }
                if (randomTopicName) {
                    randomTopicName.textContent = data.topic_name;
                }
                if (randomTopicTheoryLink && (data.theory_url || data.topic_id)) {
                    randomTopicTheoryLink.setAttribute('href', data.theory_url || `/learning/${encodeURIComponent(data.topic_id)}`);
                }
                randomTopicMeta.classList.remove('d-none');
            }
            if (data.options && Object.keys(data.options).length > 0) {
                optionsContainer.classList.remove('d-none');
                const optionCardTemplate = document.getElementById('optionCardTemplate');
                optionsGrid.replaceChildren();
                const letters = ['A', 'B', 'C', 'D'];
                letters.forEach(letter => {
                    if (data.options[letter] !== undefined && optionCardTemplate) {
                        const formattedOption = data.formatted_options?.[letter] ?? data.options[letter];
                        const fragment = optionCardTemplate.content.cloneNode(true);
                        const label = fragment.querySelector('.option-card');
                        const radio = fragment.querySelector('.option-radio');
                        const badge = fragment.querySelector('.option-letter-badge');
                        const textEl = fragment.querySelector('.option-text');
                        if (label) label.setAttribute('for', `option_${letter}`);
                        if (radio) {
                            radio.id = `option_${letter}`;
                            radio.value = letter;
                        }
                        if (badge) badge.textContent = letter;
                        if (textEl) textEl.textContent = formattedOption;
                        optionsGrid.appendChild(fragment);
                    }
                });
                attachOptionCardListeners();
            }
            loadingCard.classList.add('d-none');
            taskCard.classList.remove('d-none');
            window.renderMathInElement?.([taskQuestionBox, optionsGrid]);
        } catch (err) {
            console.error(err);
            loadingCard.classList.add('d-none');
            taskCard.classList.add('d-none');
            errorCard.classList.remove('d-none');
            errorMessage.textContent = err.message || 'Wystąpił nieoczekiwany błąd podczas generowania zadania.';
        }
    };
    if (retryBtn) {
        retryBtn.addEventListener('click', () => fetchTask(true));
    }
    const nextTaskBtn = document.getElementById('nextTaskBtn');
    if (nextTaskBtn) {
        nextTaskBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fetchTask(true);
        });
    }
    fetchTask(isForceNewInitial);
});
