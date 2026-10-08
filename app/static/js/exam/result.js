document.addEventListener('DOMContentLoaded', () => {
    window.renderMathInElement?.(document.body);
    if (!window.MathGraph?.mountTaskGraphFromScript) return;
    document.querySelectorAll('.exam-result-graph-spec').forEach(specEl => {
        window.MathGraph.mountTaskGraphFromScript(specEl, specEl.dataset.target);
    });
});
