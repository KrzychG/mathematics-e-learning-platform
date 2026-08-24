window.initAiHintModal = function initAiHintModal(modalId = 'aiHintModal') {
    const modalEl = document.getElementById(modalId);
    if (!modalEl || modalEl.dataset.hintModalBound === '1') return;
    modalEl.dataset.hintModalBound = '1';
    document.addEventListener('click', (event) => {
        const btn = event.target.closest('.btn-show-hint');
        if (!btn) return;
        const target = btn.getAttribute('data-bs-target') || '';
        if (target && target !== `#${modalId}`) return;
        const hintEl = document.getElementById(btn.dataset.hintId || '');
        const taskEl = document.getElementById(btn.dataset.taskId || '');
        const rawHint = hintEl ? hintEl.textContent : '';
        const rawTask = taskEl ? taskEl.textContent : '';
        const categoryEl = document.getElementById(`${modalId}Category`);
        const topicEl = document.getElementById(`${modalId}Topic`);
        const questionEl = document.getElementById(`${modalId}Question`);
        const userAnsEl = document.getElementById(`${modalId}UserAnswer`);
        const correctAnsEl = document.getElementById(`${modalId}CorrectAnswer`);
        const badgeEl = document.getElementById(`${modalId}ResultBadge`);
        const bodyEl = document.getElementById(`${modalId}Body`);
        if (categoryEl) categoryEl.textContent = btn.dataset.category || modalEl.dataset.defaultCategory || 'Bez kategorii';
        if (topicEl) topicEl.textContent = btn.dataset.topic || '';
        if (userAnsEl) userAnsEl.textContent = btn.dataset.userAnswer || '-';
        if (correctAnsEl) correctAnsEl.textContent = btn.dataset.correctAnswer || '-';
        if (badgeEl) {
            badgeEl.textContent = '';
            const badge = document.createElement('span');
            if (btn.dataset.isCorrect === '1') {
                badge.className = 'badge bg-success-subtle text-success border border-success-subtle';
                badge.textContent = 'Poprawna';
            } else {
                badge.className = 'badge bg-danger-subtle text-danger border border-danger-subtle';
                badge.textContent = 'Błędna';
            }
            badgeEl.appendChild(badge);
        }
        if (questionEl) {
            questionEl.textContent = rawTask;
            window.renderMathInElement?.(questionEl, { clearFirst: true });
        }
        if (bodyEl) {
            if (typeof window.renderSafeMarkdownWithMath === 'function') {
                window.renderSafeMarkdownWithMath(bodyEl, rawHint);
            } else {
                bodyEl.textContent = rawHint;
            }
        }
    });
};

window.showConfirmModal = function showConfirmModal(options = {}) {
    const modalEl = document.getElementById(options.modalId || 'appConfirmModal');
    if (!modalEl || !window.bootstrap || !window.bootstrap.Modal) return false;
    const modalId = modalEl.id;
    const allowedVariants = new Set(['primary', 'danger', 'warning', 'info', 'success', 'secondary']);
    const variant = allowedVariants.has(options.variant) ? options.variant : 'primary';
    const rawIcon = typeof options.icon === 'string' ? options.icon.trim() : '';
    const iconClass = /^bi-[a-z0-9-]+$/i.test(rawIcon) ? rawIcon : 'bi-exclamation-triangle-fill';
    const titleEl = document.getElementById(`${modalId}Title`);
    const iconWrapEl = document.getElementById(`${modalId}IconWrap`);
    const iconEl = document.getElementById(`${modalId}Icon`);
    const msgEl = document.getElementById(`${modalId}Message`);
    const noteEl = document.getElementById(`${modalId}Note`);
    const warnEl = document.getElementById(`${modalId}Warning`);
    const warnTextEl = document.getElementById(`${modalId}WarningText`);
    const submitBtn = document.getElementById(`${modalId}Submit`);
    if (titleEl) {
        titleEl.textContent = options.title || 'Potwierdź akcję';
        titleEl.className = variant === 'danger' ? 'text-danger' : '';
    }
    if (iconWrapEl) {
        iconWrapEl.className = `d-inline-flex align-items-center justify-content-center rounded-circle flex-shrink-0 bg-${variant} bg-opacity-10 text-${variant}`;
    }
    if (iconEl) {
        iconEl.className = `bi ${iconClass}`;
    }
    if (msgEl) {
        msgEl.textContent = options.message || 'Czy na pewno chcesz wykonać tę operację?';
    }
    if (noteEl) {
        if (options.note) {
            noteEl.textContent = options.note;
            noteEl.classList.remove('d-none');
        } else {
            noteEl.textContent = '';
            noteEl.classList.add('d-none');
        }
    }
    if (warnEl && warnTextEl) {
        if (options.warning) {
            warnTextEl.textContent = options.warning;
            warnEl.classList.remove('d-none');
        } else {
            warnTextEl.textContent = '';
            warnEl.classList.add('d-none');
        }
    }
    if (submitBtn) {
        submitBtn.className = `btn btn-${variant} rounded-pill px-4 fw-semibold`;
        submitBtn.textContent = options.confirmLabel || 'Potwierdź';
    }
    modalEl._pendingConfirmCallback = typeof options.onConfirm === 'function' ? options.onConfirm : null;
    window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
    return true;
};

window.initConfirmModal = function initConfirmModal(modalId = 'appConfirmModal') {
    const modalEl = document.getElementById(modalId);
    if (!modalEl || modalEl.dataset.confirmModalBound === '1') return;
    modalEl.dataset.confirmModalBound = '1';
    const submitBtn = document.getElementById(`${modalId}Submit`);
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            const cb = modalEl._pendingConfirmCallback;
            modalEl._pendingConfirmCallback = null;
            if (window.bootstrap && window.bootstrap.Modal) {
                const instance = window.bootstrap.Modal.getInstance(modalEl);
                if (instance) instance.hide();
            }
            if (typeof cb === 'function') cb();
        });
    }
    modalEl.addEventListener('hidden.bs.modal', () => {
        modalEl._pendingConfirmCallback = null;
    });
    document.addEventListener('submit', (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        const message = form.dataset.confirmMessage;
        if (!message) return;
        event.preventDefault();
        window.showConfirmModal({
            modalId,
            title: form.dataset.confirmTitle,
            message,
            note: form.dataset.confirmNote,
            warning: form.dataset.confirmWarning,
            confirmLabel: form.dataset.confirmLabel,
            variant: form.dataset.confirmVariant,
            icon: form.dataset.confirmIcon,
            onConfirm: () => HTMLFormElement.prototype.submit.call(form)
        });
    });
};
