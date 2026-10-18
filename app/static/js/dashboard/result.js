document.addEventListener('DOMContentLoaded', () => {
    const specEl = document.getElementById('resultGraphSpecData');
    window.MathGraph?.mountTaskGraphFromScript(specEl, 'resultGraphContainer');
    const explanationBox = document.getElementById('resultExplanationBox');
    if (explanationBox && typeof window.renderSafeMarkdownWithMath === 'function') {
        window.renderSafeMarkdownWithMath(explanationBox, explanationBox.textContent);
    }
    const cardBody = document.querySelector('.card-body');
    window.renderMathInElement?.(cardBody || document.body);
});
