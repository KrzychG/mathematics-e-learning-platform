window.apiFetchJson = async function apiFetchJson(url, options = {}) {
    const {
        method = 'GET',
        body = undefined,
        csrfToken = document.querySelector('input[name="csrf_token"]')?.value
            || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
            || '',
        headers: extraHeaders = {},
        errorMessage = 'Błąd połączenia z serwerem.',
    } = options;
    const headers = {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        ...extraHeaders,
    };
    if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
    }
    const fetchOptions = { method, headers };
    if (body !== undefined) {
        if (!headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }
        fetchOptions.body = typeof body === 'string' ? body : JSON.stringify(body);
    } else if (method !== 'GET' && method !== 'HEAD' && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }
    const response = await fetch(url, fetchOptions);
    let data = null;
    try {
        data = await response.json();
    } catch (err) {
        data = null;
    }
    if (!response.ok) {
        throw new Error((data && data.error) || errorMessage);
    }
    return data ?? {};
};

document.addEventListener('DOMContentLoaded', () => {
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        const updateIcon = (theme) => {
            if (!icon) return;
            const isDark = theme === 'dark';
            icon.classList.toggle('bi-sun-fill', isDark);
            icon.classList.toggle('bi-moon-stars', !isDark);
            icon.classList.toggle('text-warning', isDark);
        };
        updateIcon(htmlElement.getAttribute('data-bs-theme'));
        themeToggle.addEventListener('click', () => {
            const newTheme = htmlElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });
    }
    const hash = window.location.hash;
    if (hash) {
        const tabBtn = document.querySelector(`button[data-bs-target="${hash}"]`);
        if (tabBtn) tabBtn.click();
    }
    document.querySelectorAll('button[data-bs-toggle="pill"]').forEach(tabEl => {
        tabEl.addEventListener('click', event => {
            const newHash = event.currentTarget.getAttribute('data-bs-target');
            if (newHash) window.history.replaceState(null, null, newHash);
        });
    });
    const fontToggle = document.getElementById('dyslexiaFont');
    const motionToggle = document.getElementById('reduceMotion');
    const updateTextSize = (size) => {
        htmlElement.classList.remove('a11y-text-small', 'a11y-text-large');
        if (size !== 'default') htmlElement.classList.add(`a11y-text-${size}`);
        localStorage.setItem('a11y_textSize', size);
    };
    const textSizes = { textSize1: 'small', textSize2: 'default', textSize3: 'large' };
    const savedSize = localStorage.getItem('a11y_textSize') || 'default';
    Object.entries(textSizes).forEach(([id, size]) => {
        const radio = document.getElementById(id);
        if (!radio) return;
        if (savedSize === size) radio.checked = true;
        radio.addEventListener('change', () => updateTextSize(size));
    });
    [
        { el: fontToggle, storageKey: 'a11y_dyslexic', className: 'a11y-dyslexic' },
        { el: motionToggle, storageKey: 'a11y_reduceMotion', className: 'a11y-reduce-motion' },
    ].forEach(({ el, storageKey, className }) => {
        if (!el) return;
        if (localStorage.getItem(storageKey) === 'true') el.checked = true;
        el.addEventListener('change', (e) => {
            htmlElement.classList.toggle(className, e.target.checked);
            localStorage.setItem(storageKey, e.target.checked ? 'true' : 'false');
        });
    });
    let timeFormatTemplates = {};
    const formatsEl = document.getElementById('appTimeFormats');
    if (formatsEl && formatsEl.textContent) {
        try {
            const parsed = JSON.parse(formatsEl.textContent);
            if (parsed && typeof parsed === 'object') {
                timeFormatTemplates = parsed;
            }
        } catch (err) {
            // Ignorujemy błędy parsowania JSON - zostają czasy z SSR
        }
    }
    const formatLocalTime = (template, parts) =>
        template.replace(/\{(year|month|day|time)\}/g, (_, key) => parts[key] ?? '');
    const updateLocalTimes = () => {
        const pad = (n) => String(n).padStart(2, '0');
        document.querySelectorAll('.activity-time[data-utc]').forEach(el => {
            const utcVal = el.getAttribute('data-utc');
            if (!utcVal) return;
            const date = new Date(utcVal);
            if (isNaN(date.getTime())) return;
            const parts = {
                time: `${pad(date.getHours())}:${pad(date.getMinutes())}`,
                day: pad(date.getDate()),
                month: pad(date.getMonth() + 1),
                year: date.getFullYear(),
            };
            const format = el.getAttribute('data-format') || 'relative';
            const template = timeFormatTemplates[format];
            if (template) {
                el.textContent = formatLocalTime(template, parts);
            } else if (!el.textContent.trim() && timeFormatTemplates['date-time']) {
                el.textContent = formatLocalTime(timeFormatTemplates['date-time'], parts);
            }
        });
    };
    updateLocalTimes();
    if (typeof window.initAiHintModal === 'function') {
        window.initAiHintModal('aiHintModal');
    }
    if (typeof window.initConfirmModal === 'function') {
        window.initConfirmModal('appConfirmModal');
    }
});
