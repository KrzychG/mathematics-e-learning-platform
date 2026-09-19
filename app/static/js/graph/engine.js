/**
 * silnik do rysowania wykresów funkcji matematycznych
 * w kartezjańskim układzie współrzędnych.
 * 
 * Funkcjonalności:
 * - Dynamiczna siatka z etykietami osi X i Y
 * - Przeliczanie współrzędnych matematycznych na współrzędne ekranowe 
 * - Rysowanie krzywych funkcji na podstawie próbkowania punktów
 * - Przerywanie linii przy punktach nieciągłości
 * - Zaznaczanie punktów kluczowych
 */
(function (global) {
    'use strict';

    const SVG_NS = 'http://www.w3.org/2000/svg';
    const PADDING = 35; // Margines wokół wykresu na etykiety i strzałki osi
    let clipCounter = 0;

    /**
     * Sprawdza, czy między kolejnymi próbkami występuje nieciągłość
     * aby nie rysować pionowej linii łączącej gałęzie
     */
    function isDiscontinuity(fn, prevX, prevY, curX, curY, ySpan) {
        const dy = Math.abs(curY - prevY);
        // Gwałtowny skok wartości na osi Y
        if (dy > ySpan * 0.8) return true;
        // Zmiana znaku przy dużym skoku
        if (prevY * curY < 0 && dy > ySpan * 0.3) {
            try {
                const midY = fn((prevX + curX) / 2);
                if (!Number.isFinite(midY)) return true;
                if (midY < Math.min(prevY, curY) || midY > Math.max(prevY, curY)) return true;
            } catch (e) {
                return true;
            }
        }
        return false;
    }

    /**
     * Pomocnicza funkcja do tworzenia elementów SVG z atrybutami.
     */
    function createSvg(tag, attrs = {}) {
        const el = document.createElementNS(SVG_NS, tag);
        Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, String(v)));
        return el;
    }

    /**
     * Kompiluje definicję funkcji ze stringa lub zwraca istniejącą funkcję JS.
     */
    function compileFn(fDef) {
        if (typeof fDef.fn === 'function') return fDef.fn;
        if (global.MathParser && typeof global.MathParser.compile === 'function') {
            return global.MathParser.compile(fDef.fn || 'x');
        }
        return () => NaN;
    }

    class MathGraphEngine {
        constructor(container, options = {}) {
            this.container = typeof container === 'string' ? document.getElementById(container) : container;
            if (!this.container) return;

            // Domyślne ustawienia wykresu
            this.options = Object.assign({
                width: 720,
                height: 440,
                xRange: [-6, 6],
                yRange: [-6, 6],
                theme: document.documentElement.getAttribute('data-bs-theme') || 'light',
                functions: [],
                points: []
            }, options);

            this.plotClipId = `math-graph-clip-${++clipCounter}`;
            this.initDOM();
            this.render();
        }

        /**
         * Dobiera paletę barw w zależności od motywu (jasny / ciemny).
         */
        getColors() {
            const isDark = (document.documentElement.getAttribute('data-bs-theme') || this.options.theme) === 'dark';
            return {
                bg: isDark ? '#1e293b' : '#ffffff',
                axis: isDark ? '#94a3b8' : '#475569',
                grid: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)',
                gridMajor: isDark ? 'rgba(255, 255, 255, 0.16)' : 'rgba(0, 0, 0, 0.12)',
                text: isDark ? '#cbd5e1' : '#475569',
                primaryFn: isDark ? '#38bdf8' : '#2563eb',
                secondaryFn: isDark ? '#f43f5e' : '#e11d48'
            };
        }

        /**
         * Przygotowanie kontenera i głównego elementu <svg>.
         */
        initDOM() {
            this.container.innerHTML = '';
            this.wrapper = document.createElement('div');
            this.wrapper.className = 'math-graph-wrapper position-relative w-100';
            this.wrapper.style.maxWidth = `${this.options.width}px`;

            this.svg = createSvg('svg', {
                viewBox: `0 0 ${this.options.width} ${this.options.height}`,
                class: 'w-100 h-auto rounded-4 shadow-xs'
            });
            Object.assign(this.svg.style, { display: 'block', border: '1px solid var(--app-border, rgba(0,0,0,0.08))' });

            this.wrapper.appendChild(this.svg);
            this.container.appendChild(this.wrapper);
        }

        // Przeliczanie matematycznego x na współrzędną pikselową w SVG
        toSvgX(x) {
            const [min, max] = this.options.xRange;
            return PADDING + ((x - min) / (max - min)) * (this.options.width - PADDING * 2);
        }

        // Przeliczanie matematycznego y na piksel w SVG
        toSvgY(y) {
            const [min, max] = this.options.yRange;
            return this.options.height - PADDING - ((y - min) / (max - min)) * (this.options.height - PADDING * 2);
        }

        // Wyznaczenie kroku podziałki (np. co 1, co 5) w zależności od zakresu osi
        computeStep() {
            const span = this.options.xRange[1] - this.options.xRange[0];
            return span > 50 ? 5 : (span < 5 ? 0.5 : 1);
        }

        /**
         * Główna funkcja renderująca układ współrzędnych i wykresy.
         */
        render() {
            const colors = this.getColors();
            this.svg.innerHTML = '';

            // Definicje: groty strzałek osi oraz prostokąt przycinający clipPath
            const defs = createSvg('defs');
            ['arrowX', 'arrowY'].forEach(id => {
                const marker = createSvg('marker', {
                    id, viewBox: '0 0 10 10', refX: 5, refY: 5,
                    markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse'
                });
                marker.appendChild(createSvg('path', { d: 'M 0 1.5 L 10 5 L 0 8.5 z', fill: colors.axis }));
                defs.appendChild(marker);
            });

            // Obszar przycinania - zapobiega wychodzeniu wykresu poza układ osi
            const clip = createSvg('clipPath', { id: this.plotClipId });
            clip.appendChild(createSvg('rect', {
                x: PADDING,
                y: PADDING,
                width: Math.max(0, this.options.width - PADDING * 2),
                height: Math.max(0, this.options.height - PADDING * 2)
            }));
            defs.appendChild(clip);
            this.svg.appendChild(defs);

            // Tło wykresu
            this.svg.appendChild(createSvg('rect', { width: '100%', height: '100%', fill: colors.bg, rx: '16' }));

            const step = this.computeStep();
            this.renderGrid(colors, step);
            this.renderAxes(colors, step);
            this.renderFunctions(colors);
            this.renderPoints(colors);
        }

        /**
         * Rysowanie siatki pomocniczej.
         */
        renderGrid(colors, step) {
            const [minX, maxX] = this.options.xRange;
            const [minY, maxY] = this.options.yRange;
            const g = createSvg('g', { class: 'grid-lines' });

            // Pionowe linie siatki
            for (let x = Math.floor(minX / step) * step; x <= maxX; x += step) {
                const sx = this.toSvgX(x);
                if (sx < 30 || sx > this.options.width - 30) continue;
                const isMaj = Math.abs(x % (step * 5)) < 1e-4;
                g.appendChild(createSvg('line', {
                    x1: sx, y1: PADDING, x2: sx, y2: this.options.height - PADDING,
                    stroke: isMaj ? colors.gridMajor : colors.grid,
                    'stroke-width': isMaj ? '1.5' : '1'
                }));
            }

            // Poziome linie siatki
            for (let y = Math.floor(minY / step) * step; y <= maxY; y += step) {
                const sy = this.toSvgY(y);
                if (sy < 30 || sy > this.options.height - 30) continue;
                const isMaj = Math.abs(y % (step * 5)) < 1e-4;
                g.appendChild(createSvg('line', {
                    x1: PADDING, y1: sy, x2: this.options.width - PADDING, y2: sy,
                    stroke: isMaj ? colors.gridMajor : colors.grid,
                    'stroke-width': isMaj ? '1.5' : '1'
                }));
            }
            this.svg.appendChild(g);
        }

        /**
         * Rysowanie osi OX i OY z podziałkami liczbowymi i strzałkami.
         */
        renderAxes(colors, step) {
            const [minX, maxX] = this.options.xRange;
            const [minY, maxY] = this.options.yRange;
            const g = createSvg('g');

            const zx = Math.max(PADDING, Math.min(this.options.width - PADDING, this.toSvgX(0)));
            const zy = Math.max(PADDING, Math.min(this.options.height - PADDING, this.toSvgY(0)));

            // Oś OX
            g.appendChild(createSvg('line', {
                x1: 20, y1: zy, x2: this.options.width - 15, y2: zy,
                stroke: colors.axis, 'stroke-width': '2', 'marker-end': 'url(#arrowX)'
            }));
            const lx = createSvg('text', {
                x: this.options.width - 25, y: zy - 10,
                fill: colors.text, 'font-size': '13', 'font-weight': 'bold'
            });
            lx.textContent = 'x';
            g.appendChild(lx);

            // Oś OY
            g.appendChild(createSvg('line', {
                x1: zx, y1: this.options.height - 20, x2: zx, y2: 15,
                stroke: colors.axis, 'stroke-width': '2', 'marker-end': 'url(#arrowY)'
            }));
            const ly = createSvg('text', {
                x: zx + 10, y: 25,
                fill: colors.text, 'font-size': '13', 'font-weight': 'bold'
            });
            ly.textContent = 'y';
            g.appendChild(ly);

            // Etykiety liczb na osi OX
            for (let x = Math.floor(minX / step) * step; x <= maxX; x += step) {
                if (Math.abs(x) < 1e-4) continue;
                const pos = this.toSvgX(x);
                if (pos < 45 || pos > this.options.width - 45) continue;
                const txt = createSvg('text', {
                    x: pos, y: zy + 16,
                    fill: colors.text, 'font-size': '10', 'text-anchor': 'middle'
                });
                txt.textContent = Number(x.toFixed(2)).toString();
                g.appendChild(txt);
            }

            // Etykiety liczb na osi OY
            for (let y = Math.floor(minY / step) * step; y <= maxY; y += step) {
                if (Math.abs(y) < 1e-4) continue;
                const pos = this.toSvgY(y);
                if (pos < 45 || pos > this.options.height - 45) continue;
                const txt = createSvg('text', {
                    x: zx - 8, y: pos + 4,
                    fill: colors.text, 'font-size': '10', 'text-anchor': 'end'
                });
                txt.textContent = Number(y.toFixed(2)).toString();
                g.appendChild(txt);
            }
            this.svg.appendChild(g);
        }

        /**
         * Rysowanie krzywych funkcji matematycznych przez próbkowanie 400 punktów.
         */
        renderFunctions(colors) {
            const [minX, maxX] = this.options.xRange;
            const [minY, maxY] = this.options.yRange;
            const ySpan = Math.max(1e-6, maxY - minY);
            const yMargin = ySpan * 2;
            const samples = 400; // liczba punktów próbkowania
            const step = (maxX - minX) / samples;
            const g = createSvg('g', { 'clip-path': `url(#${this.plotClipId})` });

            this.options.functions.forEach((fDef, idx) => {
                if (fDef.visible === false) return;
                const color = fDef.color || (idx === 0 ? colors.primaryFn : colors.secondaryFn);
                const fn = compileFn(fDef);

                const segments = [];
                let cur = [];
                let prevX = null;
                let prevY = null;

                for (let i = 0; i <= samples; i++) {
                    const mx = minX + i * step;
                    let my;
                    try { my = fn(mx); } catch (e) { my = NaN; }

                    if (Number.isFinite(my) && my >= minY - yMargin && my <= maxY + yMargin) {
                        // Jeśli nastąpił skok (nieciągłość), kończymy obecny segment i zaczynamy nowy
                        if (cur.length > 0 && isDiscontinuity(fn, prevX, prevY, mx, my, ySpan)) {
                            segments.push(cur);
                            cur = [];
                        }
                        cur.push(`${this.toSvgX(mx).toFixed(1)},${this.toSvgY(my).toFixed(1)}`);
                        prevX = mx;
                        prevY = my;
                    } else if (cur.length > 0) {
                        segments.push(cur);
                        cur = [];
                        prevX = null;
                        prevY = null;
                    }
                }
                if (cur.length > 0) segments.push(cur);

                // Rysujemy każdy ciągły segment jako ścieżkę SVG <path>
                segments.forEach(seg => {
                    if (seg.length > 1) {
                        g.appendChild(createSvg('path', {
                            d: `M ${seg.join(' L ')}`,
                            stroke: color,
                            'stroke-width': fDef.strokeWidth || 3,
                            fill: 'none',
                            'stroke-linecap': 'round',
                            'stroke-linejoin': 'round'
                        }));
                    }
                });
            });
            this.svg.appendChild(g);
        }

        /**
         * Zaznaczanie punktów kluczowych na wykresie (np. miejsca zerowe, wierzchołek).
         */
        renderPoints(colors) {
            if (!this.options.points || !this.options.points.length) return;
            const g = createSvg('g');

            this.options.points.forEach(pt => {
                const sx = this.toSvgX(pt.x);
                const sy = this.toSvgY(pt.y);
                if (sx < 20 || sx > this.options.width - 20 || sy < 20 || sy > this.options.height - 20) return;

                // Kropka punktu
                g.appendChild(createSvg('circle', {
                    cx: sx, cy: sy, r: pt.r || '6',
                    fill: pt.color || colors.primaryFn,
                    stroke: '#ffffff', 'stroke-width': '2'
                }));

                // Podpis punktu (np. "W(2, 4)")
                if (pt.label) {
                    const txt = createSvg('text', {
                        x: sx + 8, y: sy - 8,
                        fill: pt.color || colors.text,
                        'font-size': '11', 'font-weight': 'bold'
                    });
                    txt.textContent = pt.label;
                    g.appendChild(txt);
                }
            });
            this.svg.appendChild(g);
        }

        update(newOptions) {
            Object.assign(this.options, newOptions);
            this.render();
        }

        zoom(factor) {
            const [minX, maxX] = this.options.xRange;
            const [minY, maxY] = this.options.yRange;
            const cx = (minX + maxX) / 2;
            const cy = (minY + maxY) / 2;
            this.options.xRange = [cx - (cx - minX) * factor, cx + (maxX - cx) * factor];
            this.options.yRange = [cy - (cy - minY) * factor, cy + (maxY - cy) * factor];
            this.render();
        }

        resetView() {
            this.options.xRange = [-6, 6];
            this.options.yRange = [-6, 6];
            this.render();
        }
    }

    /**
     * Obiekt pomocniczy MathGraph z metodami montowania wykresu w szablonach zadań.
     */
    const MathGraph = {
        Engine: MathGraphEngine,

        parseGraphSpec(raw) {
            let s = raw;
            for (let i = 0; i < 2 && typeof s === 'string'; i++) {
                if (!s.trim()) return null;
                try { s = JSON.parse(s.trim()); } catch (e) { return null; }
            }
            return s && typeof s === 'object' ? s : null;
        },

        renderTaskGraph(container, spec) {
            const el = typeof container === 'string' ? document.getElementById(container) : container;
            if (!el || !spec) return null;
            const fnDefs = (spec.formula || spec.fn)
                ? [{ fn: spec.formula || spec.fn, color: spec.color || '#2563eb', strokeWidth: 3 }]
                : [];
            return new MathGraphEngine(el, {
                width: 580,
                height: 380,
                xRange: spec.xRange || [-6, 6],
                yRange: spec.yRange || [-6, 6],
                functions: fnDefs,
                points: spec.points || []
            });
        },

        mountTaskGraph(container, rawSpec, { wrapper = null, force = true } = {}) {
            const el = typeof container === 'string' ? document.getElementById(container) : container;
            if (!el) return null;
            const w = typeof wrapper === 'string' ? document.getElementById(wrapper) : wrapper;
            const spec = this.parseGraphSpec(rawSpec);
            if (!spec) {
                if (w) w.classList.add('d-none');
                el.innerHTML = '';
                return null;
            }
            if (w) w.classList.remove('d-none');
            if (!force && el.querySelector('svg')) return null;
            el.innerHTML = '';
            return this.renderTaskGraph(el, spec);
        },

        mountTaskGraphFromScript(specEl, container, options = {}) {
            if (!specEl) return null;
            return this.mountTaskGraph(container, specEl.textContent, options);
        }
    };

    global.MathGraph = MathGraph;
})(typeof window !== 'undefined' ? window : this);
