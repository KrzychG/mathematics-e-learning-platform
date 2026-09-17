/**
 * Interaktywny brudnopis do szybkich obliczeń i notatek matematycznych.
 * Obsługuje rysowanie ołówkiem/gumką, cofanie
 */
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('scratchpadCanvas');
    const drawer = document.getElementById('scratchpadDrawer');
    const edgeTab = document.getElementById('scratchpadEdgeTab');
    const defaultDot = document.getElementById('scratchpadDefaultColorDot');
    if (!canvas || !drawer) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Stan rysowania
    let isDrawing = false;
    let currentTool = 'pen';
    let isDefaultColor = true;
    let currentColor = '#1e293b';
    let currentSize = 4;
    let lastX = 0;
    let lastY = 0;

    // Historia do cofania
    const undoStack = [];

    const getIsDark = () => document.documentElement.getAttribute('data-bs-theme') === 'dark';
    let currentTheme = getIsDark() ? 'dark' : 'light';

    const updateDefaultDot = () => {
        if (!defaultDot) return;
        const isDark = getIsDark();
        defaultDot.title = isDark ? 'Biały / Kreda' : 'Czarny / Grafit';
    };

    const getEffectiveColor = () => {
        if (isDefaultColor) {
            return getIsDark() ? '#f8fafc' : '#1e293b';
        }
        return currentColor;
    };

    // Skalowanie płótna
    const resize = () => {
        if (drawer.classList.contains('is-collapsed') || !canvas.parentElement) return;
        const rect = canvas.parentElement.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return;
        const dpr = window.devicePixelRatio || 1;
        const tw = Math.round(rect.width * dpr), th = Math.round(rect.height * dpr);
        if (canvas.width === tw && canvas.height === th) return;
        const temp = document.createElement('canvas');
        temp.width = canvas.width; temp.height = canvas.height;
        const tc = temp.getContext('2d');
        if (tc && canvas.width > 0) tc.drawImage(canvas, 0, 0);
        canvas.width = tw; canvas.height = th;
        canvas.style.width = `${rect.width}px`; canvas.style.height = `${rect.height}px`;
        ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        if (temp.width > 0) ctx.drawImage(temp, 0, 0, tw, th);
    };

    // Przeliczenie współrzędnych kursora myszy / dotyku na współrzędne Canvas
    const getPos = (e) => {
        const r = canvas.getBoundingClientRect();
        return {
            x: (e.clientX - r.left) * (canvas.width / r.width),
            y: (e.clientY - r.top) * (canvas.height / r.height)
        };
    };

    const applyStyle = () => {
        const dpr = window.devicePixelRatio || 1;
        ctx.globalCompositeOperation = currentTool === 'eraser' ? 'destination-out' : 'source-over';
        ctx.lineWidth = (currentTool === 'eraser' ? currentSize * 5 : currentSize) * dpr;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        const c = getEffectiveColor();
        ctx.strokeStyle = c; ctx.fillStyle = c;
    };

    // Przelicza monochromatyczne pociągnięcia przy przełączaniu motywu
    const adaptImageData = (imageData, toDark) => {
        const data = imageData.data;
        const len = data.length;
        for (let i = 0; i < len; i += 4) {
            if (data[i + 3] === 0) continue;
            const r = data[i], g = data[i + 1], b = data[i + 2];
            const max = Math.max(r, g, b);
            const min = Math.min(r, g, b);
            const sat = max - min;
            if (sat <= 35) {
                if (toDark && max < 120) {
                    data[i] = 248;
                    data[i + 1] = 250;
                    data[i + 2] = 252;
                } else if (!toDark && min > 150) {
                    data[i] = 30;
                    data[i + 1] = 41;
                    data[i + 2] = 59;
                }
            }
        }
    };

    const adaptCanvasTheme = (toDark) => {
        if (!canvas || canvas.width === 0 || canvas.height === 0) return;
        try {
            const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            adaptImageData(imgData, toDark);
            ctx.putImageData(imgData, 0, 0);
        } catch (e) {
            console.warn('Scratchpad canvas adaptation error:', e);
        }
    };

    const adaptSnapshotTheme = (snap, toDark) => {
        if (!snap || snap.width === 0 || snap.height === 0) return;
        try {
            const sctx = snap.getContext('2d');
            if (!sctx) return;
            const imgData = sctx.getImageData(0, 0, snap.width, snap.height);
            adaptImageData(imgData, toDark);
            sctx.putImageData(imgData, 0, 0);
        } catch (e) {
            console.warn('Scratchpad snapshot adaptation error:', e);
        }
    };

    const handleThemeChange = () => {
        const newTheme = getIsDark() ? 'dark' : 'light';
        if (newTheme === currentTheme) return;
        const toDark = newTheme === 'dark';
        adaptCanvasTheme(toDark);
        undoStack.forEach(snap => adaptSnapshotTheme(snap, toDark));
        updateDefaultDot();
        if (isDefaultColor) {
            currentColor = getEffectiveColor();
        }
        currentTheme = newTheme;
    };

    const themeObserver = new MutationObserver((mutations) => {
        for (const m of mutations) {
            if (m.attributeName === 'data-bs-theme') {
                handleThemeChange();
            }
        }
    });
    themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-bs-theme'] });
    updateDefaultDot();

    // Zapisuje stan płótna przed kolejną kreską
    const pushUndo = () => {
        const snap = document.createElement('canvas');
        snap.width = canvas.width;
        snap.height = canvas.height;
        const sc = snap.getContext('2d');
        if (sc) sc.drawImage(canvas, 0, 0);
        undoStack.push(snap);
        if (undoStack.length > 20) undoStack.shift();
    };

    // Obsługa zdarzeń wskaźnika
    canvas.addEventListener('pointerdown', (e) => {
        if (e.button && e.button !== 0) return;
        isDrawing = true;
        pushUndo();
        const p = getPos(e);
        lastX = p.x;
        lastY = p.y;
        applyStyle();
        ctx.beginPath();
        ctx.arc(p.x, p.y, ctx.lineWidth / 2, 0, Math.PI * 2);
        ctx.fill();
    });

    canvas.addEventListener('pointermove', (e) => {
        if (!isDrawing) return;
        const p = getPos(e);
        applyStyle();
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
        lastX = p.x;
        lastY = p.y;
    });

    const stopDrawing = () => {
        isDrawing = false;
    };
    canvas.addEventListener('pointerup', stopDrawing);
    canvas.addEventListener('pointercancel', stopDrawing);

    const toggleDrawer = (open) => {
        const isOpen = open !== undefined ? open : drawer.classList.contains('is-collapsed');
        drawer.classList.toggle('is-collapsed', !isOpen);
        if (edgeTab) edgeTab.style.display = isOpen ? 'none' : 'flex';
        if (isOpen) resize();
        window.dispatchEvent(new Event('resize'));
    };

    document.querySelectorAll('[data-scratchpad-toggle="true"]').forEach(el => el.addEventListener('click', (e) => {
        e.preventDefault(); e.stopPropagation(); toggleDrawer();
    }));

    document.getElementById('scratchpadClearBtn')?.addEventListener('click', () => {
        pushUndo(); ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    document.getElementById('scratchpadUndoBtn')?.addEventListener('click', () => {
        if (!undoStack.length) return;
        const snap = undoStack.pop();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(snap, 0, 0, canvas.width, canvas.height);
    });

    const setTool = (t) => {
        currentTool = t;
        document.getElementById('toolPen')?.classList.toggle('active', t === 'pen');
        document.getElementById('toolEraser')?.classList.toggle('active', t === 'eraser');
    };
    document.getElementById('toolPen')?.addEventListener('click', () => setTool('pen'));
    document.getElementById('toolEraser')?.addEventListener('click', () => setTool('eraser'));

    document.querySelectorAll('.scratchpad-color-dot').forEach(dot => dot.addEventListener('click', () => {
        document.querySelectorAll('.scratchpad-color-dot').forEach(d => d.classList.toggle('active', d === dot));
        const colorVal = dot.getAttribute('data-color');
        if (colorVal === 'default' || colorVal === '#1e293b' || colorVal === '#f8fafc') {
            isDefaultColor = true;
            currentColor = getEffectiveColor();
        } else {
            isDefaultColor = false;
            currentColor = colorVal || '#0d6efd';
        }
        if (currentTool === 'eraser') setTool('pen');
    }));

    document.querySelectorAll('#scratchpadSizes button').forEach(btn => btn.addEventListener('click', () => {
        document.querySelectorAll('#scratchpadSizes button').forEach(b => b.classList.toggle('active', b === btn));
        currentSize = parseInt(btn.getAttribute('data-size') || '4', 10);
    }));

    window.addEventListener('resize', resize);
    toggleDrawer(false);
});
