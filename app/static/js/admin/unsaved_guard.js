window.initUnsavedChangesGuard = function(options) {
    const {
        form,
        trackedInputs = [],
        badge = null,
        getExtraState = () => ({}),
        onMainSubmit = null,
    } = options || {};
    if (!form) return null;
    let initialStateSnapshot = '';
    let allowUnload = false;
    function getFormStateSnapshot() {
        const inputValues = {};
        trackedInputs.forEach(el => {
            if (el) inputValues[el.id || el.name] = el.value;
        });
        return JSON.stringify({ ...inputValues, ...getExtraState() });
    }
    function hasUnsavedChanges() {
        return !allowUnload && initialStateSnapshot !== '' && getFormStateSnapshot() !== initialStateSnapshot;
    }
    function updateDirtyState() {
        if (badge) badge.classList.toggle('d-none', !hasUnsavedChanges());
    }
    function confirmLeaveWithUnsavedChanges(onProceed) {
        if (!hasUnsavedChanges()) return onProceed();
        const proceed = () => {
            allowUnload = true;
            onProceed();
        };
        if (typeof window.showConfirmModal === 'function') {
            const shown = window.showConfirmModal({
                title: 'Niezapisane zmiany',
                message: 'Masz niezapisane zmiany w edytowanym temacie. Czy na pewno chcesz opuścić tę stronę?',
                warning: 'Wprowadzone modyfikacje treści lub danych tematu zostaną utracone bez zapisu.',
                confirmLabel: 'Opuść bez zapisywania',
                variant: 'warning',
                icon: 'bi-exclamation-triangle-fill',
                onConfirm: proceed,
            });
            if (shown) return;
        }
        proceed();
    }
    trackedInputs.forEach(el => {
        if (!el) return;
        const evName = el.tagName === 'SELECT' ? 'change' : 'input';
        el.addEventListener(evName, updateDirtyState);
    });
    form.addEventListener('submit', (e) => {
        if (onMainSubmit) onMainSubmit(e);
        if (!e.defaultPrevented) allowUnload = true;
    });
    document.addEventListener('click', (e) => {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || !hasUnsavedChanges()) return;
        const targetEl = e.target?.nodeType === Node.TEXT_NODE ? e.target.parentElement : e.target;
        const link = targetEl?.closest?.('a[href]');
        if (!link || link.hasAttribute('download') || link.hasAttribute('data-bs-toggle')) return;
        const targetAttr = (link.getAttribute('target') || '').trim().toLowerCase();
        const rawHref = (link.getAttribute('href') || '').trim();
        if ((targetAttr && targetAttr !== '_self') || !rawHref || rawHref.startsWith('#') || rawHref.toLowerCase().startsWith('javascript:')) return;
        try {
            const destUrl = new URL(link.href, window.location.href);
            if (destUrl.href === window.location.href) return;
            e.preventDefault();
            confirmLeaveWithUnsavedChanges(() => { window.location.href = destUrl.href; });
        } catch {
            // Ignoruj niepoprawny URL
        }
    });
    document.addEventListener('submit', (e) => {
        const submittedForm = e.target;
        if (e.defaultPrevented || !submittedForm || submittedForm === form || submittedForm.dataset?.confirmMessage || !hasUnsavedChanges()) return;
        const formTarget = (submittedForm.getAttribute('target') || '').trim().toLowerCase();
        if (formTarget && formTarget !== '_self') return;
        e.preventDefault();
        confirmLeaveWithUnsavedChanges(() => HTMLFormElement.prototype.submit.call(submittedForm));
    });
    window.addEventListener('beforeunload', (e) => {
        if (hasUnsavedChanges()) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
    window.addEventListener('pageshow', (e) => {
        if (e.persisted) {
            allowUnload = false;
            updateDirtyState();
        }
    });
    initialStateSnapshot = getFormStateSnapshot();
    updateDirtyState();
    return { updateDirtyState };
};
