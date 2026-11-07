document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('theory');
    if (!textarea) return;

    const editorStats = document.getElementById('editorStats');
    const previewContent = document.getElementById('previewContent');
    const tabPreview = document.getElementById('tabPreview');

    function updateStats() {
        if (!editorStats) return;
        const text = textarea.value.trim();
        const chars = text.length;
        const words = text ? text.split(/\s+/).filter(Boolean).length : 0;
        editorStats.textContent = `${chars} znaków | ${words} słów`;
    }

    textarea.addEventListener('input', updateStats);
    updateStats();

    function insertSnippet(before, after = '', placeholder = '') {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selected = textarea.value.substring(start, end) || placeholder;
        const replacement = before + selected + after;

        textarea.setRangeText(replacement, start, end, 'select');
        textarea.focus();
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        updateStats();
    }

    if (typeof window.initMathFormulaModal === 'function') {
        window.initMathFormulaModal(({ value, isBlock }) => {
            if (isBlock) {
                insertSnippet('\n$$\n', '\n$$\n', value);
            } else {
                insertSnippet('$', '$', value);
            }
        });
    }

    if (tabPreview && previewContent) {
        tabPreview.addEventListener('shown.bs.tab', async () => {
            const rawMarkdown = textarea.value.trim();
            if (!rawMarkdown) {
                previewContent.innerHTML = '';
                return;
            }

            previewContent.innerHTML = '<div class="text-center py-5 text-muted"><div class="spinner-border spinner-border-sm text-primary me-2"></div>Generowanie podglądu lekcji...</div>';

            try {
                const response = await window.apiFetchJson('/admin/topic/preview', {
                    method: 'POST',
                    body: { markdown: rawMarkdown },
                    errorMessage: 'Nie udało się wygenerować podglądu lekcji.',
                });
                previewContent.innerHTML = response.html || '<p class="text-muted fst-italic">Pusta treść.</p>';
                window.renderMathInElement?.(previewContent, { clearFirst: true });
            } catch (err) {
                previewContent.replaceChildren();
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger mb-0';
                const icon = document.createElement('i');
                icon.className = 'bi bi-exclamation-triangle me-2';
                alertDiv.appendChild(icon);
                alertDiv.appendChild(document.createTextNode(`Błąd generowania podglądu: ${err.message}`));
                previewContent.appendChild(alertDiv);
            }
        });
    }

    if (typeof window.initUnsavedChangesGuard === 'function') {
        window.initUnsavedChangesGuard({
            form: document.getElementById('editTopicForm'),
            trackedInputs: [
                document.getElementById('name'),
                document.getElementById('category_id'),
                document.getElementById('description'),
                textarea,
            ],
            badge: document.getElementById('unsavedChangesBadge'),
        });
    }
});
