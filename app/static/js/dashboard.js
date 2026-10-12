document.addEventListener('DOMContentLoaded', () => {
    initAccuracyChart();
    initKnowledgeStructure();
});

function initAccuracyChart() {
    const canvas = document.getElementById('accuracyChart');
    if (!canvas || typeof Chart === 'undefined') return;
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = '#94a3b8';
    let labels = [];
    let values = [];
    try {
        labels = JSON.parse(canvas.dataset.labels || '[]');
        values = JSON.parse(canvas.dataset.values || '[]');
    } catch (e) {
        console.error('Błąd parsowania danych wykresu:', e);
    }
    if (!labels.length || !values.length) {
        const targetAccuracy = parseFloat(canvas.dataset.accuracy || '0');
        labels = ['Dziś'];
        values = [targetAccuracy];
    }
    const ctxAccuracy = canvas.getContext('2d');
    const lastValue = values[values.length - 1] || 0;
    const strokeColor = lastValue >= 50 ? '#10b981' : '#f59e0b';
    const fillColor = lastValue >= 50 ? 'rgba(16, 185, 129, 0.12)' : 'rgba(245, 158, 11, 0.12)';
    new Chart(ctxAccuracy, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                borderColor: strokeColor,
                backgroundColor: fillColor,
                borderWidth: 2.5,
                fill: true,
                tension: 0.35,
                pointRadius: values.length === 1 ? 4 : 3,
                pointBackgroundColor: strokeColor,
                pointBorderColor: '#ffffff',
                pointBorderWidth: 1.5,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: strokeColor,
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: true,
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        font: { size: 10, family: "'Inter', sans-serif" },
                        color: '#94a3b8',
                        maxRotation: 0,
                        autoSkip: false
                    }
                },
                y: {
                    display: false,
                    min: 0,
                    max: 100
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    enabled: true,
                    backgroundColor: '#1e293b',
                    titleFont: { size: 11, family: "'Inter', sans-serif" },
                    bodyFont: { size: 12, family: "'Inter', sans-serif", weight: 'bold' },
                    padding: 8,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return 'Skuteczność: ' + context.parsed.y + '%';
                        }
                    }
                }
            },
            interaction: { mode: 'index', intersect: false }
        }
    });
}

function initKnowledgeStructure() {
    const filterButtons = document.querySelectorAll('.knowledge-filter-btn');
    const categoryItems = document.querySelectorAll('.category-accordion-item');
    const emptyMessage = document.getElementById('filterEmptyMessage');
    const toggleAllBtn = document.getElementById('toggleAllCategoriesBtn');
    const resetFilterBtn = document.getElementById('resetFilterBtn');
    if (!categoryItems.length) return;
    let isAllExpanded = false;
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            let visibleCategoriesCount = 0;
            categoryItems.forEach(catItem => {
                const topicItems = catItem.querySelectorAll('.topic-item');
                const catCollapse = catItem.querySelector('.accordion-collapse');
                let matchingTopicsInCat = 0;
                topicItems.forEach(topic => {
                    const status = topic.dataset.status;
                    const matches = (filter === 'all' || status === filter);
                    topic.classList.toggle('d-none', !matches);
                    if (matches) matchingTopicsInCat++;
                });
                const isVisible = (filter === 'all' || matchingTopicsInCat > 0);
                catItem.classList.toggle('d-none', !isVisible);
                if (isVisible) {
                    visibleCategoriesCount++;
                    if (filter !== 'all' && catCollapse && typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                        bootstrap.Collapse.getOrCreateInstance(catCollapse, { toggle: false }).show();
                    }
                }
            });
            if (emptyMessage) {
                emptyMessage.classList.toggle('d-none', visibleCategoriesCount > 0);
            }
        });
    });
    if (resetFilterBtn) {
        resetFilterBtn.addEventListener('click', () => {
            const allBtn = document.querySelector('.knowledge-filter-btn[data-filter="all"]');
            if (allBtn) allBtn.click();
        });
    }
    if (toggleAllBtn) {
        toggleAllBtn.addEventListener('click', () => {
            isAllExpanded = !isAllExpanded;
            const textSpan = toggleAllBtn.querySelector('span');
            const icon = toggleAllBtn.querySelector('i');
            categoryItems.forEach(catItem => {
                if (catItem.classList.contains('d-none')) return;
                const catCollapse = catItem.querySelector('.accordion-collapse');
                if (catCollapse && typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                    const bsCollapse = bootstrap.Collapse.getOrCreateInstance(catCollapse, { toggle: false });
                    bsCollapse[isAllExpanded ? 'show' : 'hide']();
                }
            });
            if (textSpan) {
                textSpan.textContent = isAllExpanded ? 'Zwiń wszystkie' : 'Rozwiń wszystkie';
            }
            if (icon) {
                icon.className = isAllExpanded ? 'bi bi-arrows-collapse me-1' : 'bi bi-arrows-expand me-1';
            }
        });
    }
}
