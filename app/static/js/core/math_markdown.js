window.renderMathInElement = function(container, { clearFirst = false } = {}) {
    const rawList = Array.isArray(container) ? container : [container || document.body];
    const targets = rawList.filter(Boolean);
    if (targets.length === 0) return;
    const typesetArgs = (targets.length === 1 && targets[0] === document.body) ? undefined : targets;
    const runTypeset = () => {
        if (!window.MathJax) return;
        if (clearFirst && typeof window.MathJax.typesetClear === 'function' && typesetArgs) {
            window.MathJax.typesetClear(typesetArgs);
        }
        if (typeof window.MathJax.typesetPromise === 'function') {
            window.MathJax.typesetPromise(typesetArgs).catch((err) => console.warn('MathJax typeset warning:', err));
        }
    };
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        window.MathJax.startup.promise.then(runTypeset);
    } else {
        runTypeset();
    }
};

window.renderSafeMarkdownWithMath = function(targetEl, rawText) {
    if (!targetEl) return;
    const raw = (rawText || '').replace(/\r\n/g, '\n').trim();
    if (!raw) {
        targetEl.textContent = '';
        return;
    }
    const displayBlocks = [];
    const maskedText = raw.replace(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\])/g, (match) => {
        const token = `@@MATHBLOCK_${displayBlocks.length}@@`;
        displayBlocks.push(match);
        return token;
    });
    const MATH_OR_BLOCK_RE = /(@@MATHBLOCK_\d+@@|\\\([\s\S]*?\\\)|\$[^$\n]+\$)/g;
    const INLINE_MD_RE = /(\*\*[^*\n]+?\*\*|`[^`\n]+?`|\*[^*\s][^*\n]*?\*|\*[^*\s]\*)/g;
    const appendInlineMarkdown = (parent, segment) => {
        let lastIndex = 0;
        INLINE_MD_RE.lastIndex = 0;
        let match;
        while ((match = INLINE_MD_RE.exec(segment)) !== null) {
            if (match.index > lastIndex) {
                parent.appendChild(document.createTextNode(segment.slice(lastIndex, match.index)));
            }
            const token = match[0];
            if (token.startsWith('**') && token.endsWith('**')) {
                const strong = document.createElement('strong');
                strong.textContent = token.slice(2, -2);
                parent.appendChild(strong);
            } else if (token.startsWith('`') && token.endsWith('`')) {
                const code = document.createElement('code');
                code.className = 'px-1 rounded bg-secondary bg-opacity-10';
                code.textContent = token.slice(1, -1);
                parent.appendChild(code);
            } else if (token.startsWith('*') && token.endsWith('*')) {
                const em = document.createElement('em');
                em.textContent = token.slice(1, -1);
                parent.appendChild(em);
            }
            lastIndex = INLINE_MD_RE.lastIndex;
        }
        if (lastIndex < segment.length) {
            parent.appendChild(document.createTextNode(segment.slice(lastIndex)));
        }
    };
    const appendLineWithMathAndMarkdown = (parent, lineText) => {
        const parts = lineText.split(MATH_OR_BLOCK_RE);
        parts.forEach((part, idx) => {
            if (!part) return;
            if (idx % 2 === 1) {
                const blockMatch = part.match(/^@@MATHBLOCK_(\d+)@@$/);
                const mathStr = blockMatch ? displayBlocks[Number(blockMatch[1])] : part;
                parent.appendChild(document.createTextNode(mathStr));
            } else {
                appendInlineMarkdown(parent, part);
            }
        });
    };
    const fragment = document.createDocumentFragment();
    const lines = maskedText.split('\n');
    let currentList = null;
    let currentListTag = null;
    let paragraphLines = [];
    const flushParagraph = () => {
        if (paragraphLines.length === 0) return;
        const p = document.createElement('p');
        p.className = 'mb-2';
        paragraphLines.forEach((ln, i) => {
            if (i > 0) p.appendChild(document.createElement('br'));
            appendLineWithMathAndMarkdown(p, ln.trim());
        });
        fragment.appendChild(p);
        paragraphLines = [];
    };
    const flushList = () => {
        if (currentList) {
            fragment.appendChild(currentList);
            currentList = null;
            currentListTag = null;
        }
    };
    lines.forEach((rawLine) => {
        const trimmed = rawLine.trim();
        if (!trimmed) {
            flushParagraph();
            flushList();
            return;
        }
        const ulMatch = trimmed.match(/^[-*•]\s+(.*)$/);
        const olMatch = trimmed.match(/^(\d+)[.)]\s+(.*)$/);
        if (ulMatch || olMatch) {
            flushParagraph();
            const desiredTag = ulMatch ? 'ul' : 'ol';
            const itemText = ulMatch ? ulMatch[1] : olMatch[2];
            if (!currentList || currentListTag !== desiredTag) {
                flushList();
                currentList = document.createElement(desiredTag);
                currentList.className = 'mb-2 ps-3';
                currentListTag = desiredTag;
            }
            const li = document.createElement('li');
            li.className = 'mb-1';
            appendLineWithMathAndMarkdown(li, itemText);
            currentList.appendChild(li);
            return;
        }
        flushList();
        paragraphLines.push(trimmed);
    });
    flushParagraph();
    flushList();
    if (fragment.lastElementChild) {
        fragment.lastElementChild.classList.remove('mb-2');
    }
    targetEl.replaceChildren(fragment);
    window.renderMathInElement(targetEl, { clearFirst: true });
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-math-typeset="true"]').forEach((el) => {
        window.renderMathInElement(el);
    });
});
