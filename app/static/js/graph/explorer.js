/**
 * Moduł interaktywnego eksploratora wykresów funkcji
 * Pozwala badać funkcje liniowe, kwadratowe i dowolne wpisane przez użytkownika,
 * wyznaczając dynamicznie miejsca zerowe, punkty przecięcia z osią OY oraz wierzchołek paraboli.
 */
(function (global) {
    'use strict';

    function escapeHtml(value) {
        return String(value ?? '').replace(/[&<>"']/g, (ch) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[ch]));
    }

    function formatNum(val) {
        if (typeof val !== 'number' || !Number.isFinite(val)) return 'NaN';
        const rounded = Math.round(val * 100) / 100;
        const clean = Math.abs(rounded) < 1e-9 ? 0 : rounded;
        return Number.isInteger(clean) ? String(clean) : clean.toFixed(2).replace(/\.?0+$/, '');
    }

    function addKeyPoint(points, x, y, label, color) {
        if (typeof x !== 'number' || typeof y !== 'number' || !Number.isFinite(x) || !Number.isFinite(y)) return;
        const existing = points.find(p => Math.abs(p.x - x) < 1e-4 && Math.abs(p.y - y) < 1e-4);
        if (existing) {
            if (label && existing.label && existing.label !== label) {
                existing.label = `${existing.label}, ${label}`;
            } else if (label && !existing.label) {
                existing.label = label;
            }
        } else {
            points.push({ x, y, label: label || null, color });
        }
    }

    function buildFamilyFormula(mode, params) {
        if (mode === 'linear') {
            const { a, b } = params.linear;
            return `${a}*x ${b >= 0 ? `+ ${b}` : `- ${Math.abs(b)}`}`;
        }
        if (mode === 'quadratic') {
            const { a, b, c } = params.quadratic;
            return `${a}*x^2 ${b >= 0 ? `+ ${b}` : `- ${Math.abs(b)}`}*x ${c >= 0 ? `+ ${c}` : `- ${Math.abs(c)}`}`;
        }
        return null;
    }

    function initExplorer(containerId = 'explorerGraphContainer') {
        const graphEl = document.getElementById(containerId);
        if (!graphEl) return;
        let engine = null;
        const state = {
            currentMode: 'custom',
            formula: 'x^2 - 4',
            params: { linear: { a: 2, b: -1 }, quadratic: { a: 1, b: 0, c: -4 } }
        };
        const formulaInput = document.getElementById('singleFormulaInput');
        const legendBox = document.getElementById('graphActiveLegend');
        const pillsBox = document.getElementById('mathAnalysisPills');
        const modeBtns = {
            custom: document.getElementById('modeBtn_custom'),
            linear: document.getElementById('modeBtn_linear'),
            quadratic: document.getElementById('modeBtn_quadratic')
        };
        const slidersPanel = document.getElementById('slidersPanel');
        const linearControls = document.getElementById('controls_linear');
        const quadraticControls = document.getElementById('controls_quadratic');

        const pill = (text, cls = 'bg-primary text-primary') =>
            `<span class="badge ${cls} bg-opacity-10 px-3 py-2 rounded-pill fs-6">${text}</span>`;

        const updateAnalysis = (compiled, range) => {
            const points = [];
            let pillsHtml = '';

            if (legendBox) {
                legendBox.innerHTML = `<span class="badge rounded-pill fw-semibold border shadow-xs px-3 py-1 text-primary bg-primary bg-opacity-10">f(x) = ${escapeHtml(state.formula || '...')}</span>`;
            }

            if (state.currentMode === 'linear') {
                const { a, b } = state.params.linear;
                const isAZero = Math.abs(a) < 1e-9;
                const isBZero = Math.abs(b) < 1e-9;

                addKeyPoint(points, 0, b, `f(0)=${formatNum(b)}`, '#2563eb');

                if (isAZero) {
                    if (isBZero) {
                        pillsHtml = `${pill('Kierunkowy a = 0 (funkcja stała)')}` +
                            `<span class="badge bg-warning bg-opacity-15 text-dark border border-warning px-3 py-2 rounded-pill fs-6">Funkcja tożsamościowo równa zero (f(x) = 0)</span>` +
                            `<span class="badge bg-info bg-opacity-10 text-primary border border-info border-opacity-25 px-3 py-2 rounded-pill fs-6 fw-semibold">Nieskończenie wiele miejsc zerowych (x ∈ ℝ)</span>` +
                            `${pill('OY: (0, 0)', 'bg-success text-success')}`;
                    } else {
                        pillsHtml = `${pill('Kierunkowy a = 0 (funkcja stała)')}` +
                            `<span class="badge bg-secondary bg-opacity-10 text-secondary px-3 py-2 rounded-pill fs-6">Brak miejsc zerowych</span>` +
                            `${pill(`OY: (0, ${formatNum(b)})`, 'bg-success text-success')}`;
                    }
                } else {
                    const x0 = -b / a;
                    addKeyPoint(points, x0, 0, `x₀=${formatNum(x0)}`, '#059669');

                    pillsHtml = `${pill(`Kierunkowy a = ${formatNum(a)}`)}` +
                        `${pill(`Miejsce zerowe: x₀ = ${formatNum(x0)}`, 'bg-success text-success')}` +
                        `${pill(`OY: (0, ${formatNum(b)})`, 'bg-success text-success')}`;
                }
            } else if (state.currentMode === 'quadratic') {
                const { a, b, c } = state.params.quadratic;
                const isAZero = Math.abs(a) < 1e-9;
                const isBZero = Math.abs(b) < 1e-9;
                const isCZero = Math.abs(c) < 1e-9;

                addKeyPoint(points, 0, c, `f(0)=${formatNum(c)}`, '#2563eb');

                if (isAZero) {
                    if (isBZero && isCZero) {
                        pillsHtml = `<span class="badge bg-warning bg-opacity-15 text-dark border border-warning px-3 py-2 rounded-pill fs-6">Dla a = 0 funkcja staje się liniowa (f(x) = 0) – brak paraboli i wierzchołka</span>` +
                            `<span class="badge bg-info bg-opacity-10 text-primary border border-info border-opacity-25 px-3 py-2 rounded-pill fs-6 fw-semibold">Nieskończenie wiele miejsc zerowych (x ∈ ℝ)</span>` +
                            `${pill('OY: (0, 0)', 'bg-success text-success')}`;
                    } else if (isBZero) {
                        pillsHtml = `<span class="badge bg-warning bg-opacity-15 text-dark border border-warning px-3 py-2 rounded-pill fs-6">Dla a = 0 funkcja staje się stała (f(x) = ${formatNum(c)}) – brak paraboli i wierzchołka</span>` +
                            `<span class="badge bg-secondary bg-opacity-10 text-secondary px-3 py-2 rounded-pill fs-6">Brak miejsc zerowych</span>` +
                            `${pill(`OY: (0, ${formatNum(c)})`, 'bg-success text-success')}`;
                    } else {
                        const x0 = -c / b;
                        addKeyPoint(points, x0, 0, `x₀=${formatNum(x0)}`, '#059669');

                        const bSign = b >= 0 ? `${formatNum(b)}x` : `-${formatNum(Math.abs(b))}x`;
                        const cSign = c >= 0 ? ` + ${formatNum(c)}` : ` - ${formatNum(Math.abs(c))}`;
                        pillsHtml = `<span class="badge bg-warning bg-opacity-15 text-dark border border-warning px-3 py-2 rounded-pill fs-6">Dla a = 0 funkcja staje się liniowa (f(x) = ${bSign}${cSign}) – brak paraboli i wierzchołka</span>` +
                            `${pill(`Miejsce zerowe: x₀ = ${formatNum(x0)}`, 'bg-success text-success')}` +
                            `${pill(`OY: (0, ${formatNum(c)})`, 'bg-success text-success')}`;
                    }
                } else {
                    const delta = b * b - 4 * a * c;
                    const p = -b / (2 * a);
                    const q = -delta / (4 * a);

                    addKeyPoint(points, p, q, `W(${formatNum(p)}, ${formatNum(q)})`, '#7c3aed');

                    const deltaHtml = pill(`Δ = ${formatNum(delta)}`);
                    const vertexHtml = `<span class="badge bg-purple bg-opacity-10 px-3 py-2 rounded-pill fs-6" style="color:#7c3aed;background:rgba(124,58,237,0.1);">Wierzchołek: W(${formatNum(p)}, ${formatNum(q)})</span>`;
                    let rootsHtml = '';

                    if (delta > 1e-9) {
                        const sqrtDelta = Math.sqrt(delta);
                        const r1 = (-b - sqrtDelta) / (2 * a);
                        const r2 = (-b + sqrtDelta) / (2 * a);
                        const xMin = Math.min(r1, r2);
                        const xMax = Math.max(r1, r2);

                        addKeyPoint(points, xMin, 0, `x₁=${formatNum(xMin)}`, '#059669');
                        addKeyPoint(points, xMax, 0, `x₂=${formatNum(xMax)}`, '#059669');

                        rootsHtml = pill(`Miejsca zerowe: x₁ = ${formatNum(xMin)}, x₂ = ${formatNum(xMax)}`, 'bg-success text-success');
                    } else if (Math.abs(delta) <= 1e-9) {
                        const x0 = p;
                        addKeyPoint(points, x0, 0, `x₀=${formatNum(x0)}`, '#059669');
                        rootsHtml = pill(`Jedno podwójne miejsce zerowe: x₀ = ${formatNum(x0)}`, 'bg-success text-success');
                    } else {
                        rootsHtml = `<span class="badge bg-secondary bg-opacity-10 text-secondary px-3 py-2 rounded-pill fs-6">Brak miejsc zerowych (Δ &lt; 0)</span>`;
                    }

                    pillsHtml = `${deltaHtml}${vertexHtml}${rootsHtml}${pill(`OY: (0, ${formatNum(c)})`, 'bg-success text-success')}`;
                }
            } else {
                // Tryb własnego wzoru
                try {
                    const y0 = compiled(0);
                    if (Number.isFinite(y0)) {
                        addKeyPoint(points, 0, y0, `f(0)=${formatNum(y0)}`, '#2563eb');
                        pillsHtml += pill(`OY: (0, ${formatNum(y0)})`, 'bg-success text-success');
                    }
                } catch (e) {}

                if (global.GraphSolvers?.findFunctionZeros) {
                    const zeros = global.GraphSolvers.findFunctionZeros(compiled, range.minX, range.maxX);
                    if (zeros.isIdenticallyZero) {
                        pillsHtml += `<span class="badge bg-info bg-opacity-10 text-primary border border-info border-opacity-25 px-3 py-2 rounded-pill fs-6 fw-semibold">Nieskończenie wiele miejsc zerowych (x ∈ ℝ)</span>`;
                    } else if (zeros.length > 0) {
                        const MAX_POINTS_WITH_LABELS = 8;
                        const MAX_PILL_ITEMS = 6;

                        zeros.forEach((z, idx) => {
                            const showLabel = zeros.length <= MAX_POINTS_WITH_LABELS || idx < MAX_PILL_ITEMS;
                            addKeyPoint(points, z, 0, showLabel ? `x₀=${formatNum(z)}` : null, '#059669');
                        });

                        if (zeros.length <= MAX_PILL_ITEMS) {
                            pillsHtml += pill(`Miejsca zerowe: ${zeros.map(z => formatNum(z)).join(', ')}`, 'bg-success text-success');
                        } else {
                            const displayedZeros = zeros.slice(0, MAX_PILL_ITEMS).map(z => formatNum(z)).join(', ');
                            pillsHtml += pill(`Miejsca zerowe (${zeros.length}): ${displayedZeros}, …`, 'bg-success text-success');
                        }
                    } else {
                        pillsHtml += pill('Brak widocznych miejsc zerowych', 'bg-secondary text-secondary');
                    }
                }
            }

            if (pillsBox) pillsBox.innerHTML = pillsHtml;
            return points;
        };

        const redraw = () => {
            const expr = (state.formula || '').trim();
            const compiled = global.MathParser.compile(expr);
            const range = { minX: engine?.options?.xRange?.[0] ?? -6, maxX: engine?.options?.xRange?.[1] ?? 6 };
            const points = updateAnalysis(compiled, range);
            const fnDefs = expr ? [{ fn: compiled, color: '#2563eb', strokeWidth: 3 }] : [];
            if (!engine) {
                engine = new global.MathGraph.Engine(graphEl, { width: 720, height: 440, functions: fnDefs, points });
            } else {
                engine.update({ functions: fnDefs, points });
            }
        };

        const switchMode = (mode) => {
            state.currentMode = mode;
            Object.entries(modeBtns).forEach(([k, btn]) => {
                btn?.classList.toggle('btn-primary', k === mode);
                btn?.classList.toggle('btn-outline-primary', k !== mode);
            });
            slidersPanel?.classList.toggle('d-none', mode === 'custom');
            linearControls?.classList.toggle('d-none', mode !== 'linear');
            quadraticControls?.classList.toggle('d-none', mode !== 'quadratic');
            const fam = buildFamilyFormula(mode, state.params);
            if (fam) { state.formula = fam; if (formulaInput) formulaInput.value = fam; }
            redraw();
        };

        const applyFormula = () => {
            if (!formulaInput) return;
            state.formula = formulaInput.value.trim();
            state.currentMode = 'custom';
            switchMode('custom');
        };

        document.getElementById('applyFormulaBtn')?.addEventListener('click', applyFormula);
        formulaInput?.addEventListener('keydown', (e) => { if (e.key === 'Enter') applyFormula(); });
        document.querySelectorAll('.preset-pill').forEach(pillBtn => {
            pillBtn.addEventListener('click', () => {
                const fnExpr = pillBtn.getAttribute('data-fn');
                if (fnExpr && formulaInput) { formulaInput.value = fnExpr; applyFormula(); }
            });
        });
        Object.entries(modeBtns).forEach(([m, btn]) => btn?.addEventListener('click', () => switchMode(m)));

        [
            { s: 'slider_lin_a', v: 'val_lin_a', m: 'linear', k: 'a' },
            { s: 'slider_lin_b', v: 'val_lin_b', m: 'linear', k: 'b' },
            { s: 'slider_quad_a', v: 'val_quad_a', m: 'quadratic', k: 'a' },
            { s: 'slider_quad_b', v: 'val_quad_b', m: 'quadratic', k: 'b' },
            { s: 'slider_quad_c', v: 'val_quad_c', m: 'quadratic', k: 'c' }
        ].forEach(({ s, v, m, k }) => {
            const slider = document.getElementById(s), valEl = document.getElementById(v);
            if (!slider) return;
            state.params[m][k] = parseFloat(slider.value) || 0;
            if (valEl) valEl.textContent = slider.value;
            slider.addEventListener('input', (e) => {
                state.params[m][k] = parseFloat(e.target.value);
                if (valEl) valEl.textContent = e.target.value;
                const fam = buildFamilyFormula(m, state.params);
                if (fam) { state.formula = fam; if (formulaInput) formulaInput.value = fam; }
                redraw();
            });
        });

        document.getElementById('zoomInBtn')?.addEventListener('click', () => { engine?.zoom(0.8); redraw(); });
        document.getElementById('zoomOutBtn')?.addEventListener('click', () => { engine?.zoom(1.25); redraw(); });
        document.getElementById('resetViewBtn')?.addEventListener('click', () => { engine?.resetView(); redraw(); });

        const fam = new URLSearchParams(window.location.search).get('family');
        if (fam === 'linear' || fam === 'quadratic') switchMode(fam);
        else { if (formulaInput) formulaInput.value = state.formula; redraw(); }
    }

    if (global.MathGraph) global.MathGraph.initExplorer = initExplorer;
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('explorerGraphContainer') && global.MathGraph?.initExplorer) {
            global.MathGraph.initExplorer('explorerGraphContainer');
        }
    });
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this));
