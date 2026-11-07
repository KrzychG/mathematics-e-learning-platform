window.initMathFormulaModal = function(onInsert) {
    const modalEl = document.getElementById('mathFormulaModal');
    if (!modalEl || typeof bootstrap === 'undefined') return null;
    const modal = new bootstrap.Modal(modalEl);
    const input = document.getElementById('mathFormulaInput');
    const preview = document.getElementById('mathFormulaModalPreview');
    const blockRadio = document.getElementById('formulaTypeBlock');
    let pendingSlotTarget = null;
    function updatePreview() {
        if (!preview || !input) return;
        const val = input.value.trim();
        if (!val) {
            window.MathJax?.typesetClear?.([preview]);
            const hint = document.createElement('span');
            hint.className = 'text-muted small';
            hint.textContent = 'Wpisz wzór lub kliknij symbol powyżej...';
            preview.replaceChildren(hint);
            return;
        }
        preview.textContent = blockRadio?.checked ? `$$${val}$$` : `$${val}$`;
        window.renderMathInElement?.(preview, { clearFirst: true });
    }
    function open(slotTarget = null, forceBlock = false) {
        pendingSlotTarget = slotTarget;
        if (forceBlock && blockRadio) {
            blockRadio.checked = true;
            updatePreview();
        }
        modal.show();
        setTimeout(() => input?.focus(), 300);
    }
    document.getElementById('btnOpenMathModal')?.addEventListener('click', () => open());
    modalEl.addEventListener('hidden.bs.modal', () => { pendingSlotTarget = null; });
    input?.addEventListener('input', updatePreview);
    document.querySelectorAll('input[name="formulaTypeRadio"]').forEach(r => r.addEventListener('change', updatePreview));
    document.querySelectorAll('.math-symbol-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (!input) return;
            input.value += btn.getAttribute('data-latex') || '';
            input.focus();
            updatePreview();
        });
    });
    document.getElementById('btnInsertFormulaToEditor')?.addEventListener('click', () => {
        const val = input?.value.trim();
        if (!val) return;
        const slotTarget = pendingSlotTarget;
        pendingSlotTarget = null;
        onInsert({ value: val, isBlock: Boolean(blockRadio?.checked), slotTarget });
        input.value = '';
        updatePreview();
        modal.hide();
    });
    return { open };
};
