function showModalById(modalId) {
    const modalEl = document.getElementById(modalId);
    if (modalEl && window.bootstrap) {
        bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
}

function resetNewTopicModal(catId = '') {
    const form = document.getElementById('formNewTopic');
    if (form) form.reset();
    const select = document.getElementById('topicCategory');
    if (select) {
        select.value = catId ? String(catId) : '';
    }
}

function openNewTopicForCategory(catId) {
    resetNewTopicModal(catId);
    showModalById('modalNewTopic');
}

function configureEntityModalForm(formId, actionUrl, modalId, populate) {
    const form = document.getElementById(formId);
    if (!form) return;
    form.action = actionUrl;
    if (typeof populate === 'function') populate();
    showModalById(modalId);
}

function openEditCategoryModal(catId, catName) {
    configureEntityModalForm(
        'formEditCategory',
        '/admin/category/' + encodeURIComponent(catId) + '/edit',
        'modalEditCategory',
        () => {
            const nameInput = document.getElementById('editCatName');
            if (nameInput) nameInput.value = catName || '';
        }
    );
}

function openDeleteCategoryModal(catId, catName, topicsCount) {
    configureEntityModalForm(
        'formDeleteCategory',
        '/admin/category/' + encodeURIComponent(catId) + '/delete',
        'modalDeleteCategory',
        () => {
            const nameEl = document.getElementById('deleteCatName');
            if (nameEl) nameEl.textContent = catName || '';
            const warningBox = document.getElementById('deleteCatTopicsWarning');
            const countEl = document.getElementById('deleteCatTopicsCount');
            if (warningBox) {
                warningBox.style.display = topicsCount > 0 ? 'block' : 'none';
                if (topicsCount > 0 && countEl) countEl.textContent = topicsCount;
            }
        }
    );
}

function openDeleteTopicModal(topicId, topicName) {
    configureEntityModalForm(
        'formDeleteTopic',
        '/admin/topic/' + encodeURIComponent(topicId) + '/delete',
        'modalDeleteTopic',
        () => {
            const nameEl = document.getElementById('deleteTopicName');
            if (nameEl) nameEl.textContent = topicName || '';
        }
    );
}

function previewTheory(topicId, topicName) {
    const contentEl = document.getElementById('theory-content-' + topicId);
    const bodyEl = document.getElementById('previewTheoryBody');
    const titleEl = document.getElementById('previewTheoryTitle');
    if (!bodyEl || !titleEl) return;
    titleEl.textContent = '';
    const icon = document.createElement('i');
    icon.className = 'bi bi-book-half text-primary me-2';
    titleEl.appendChild(icon);
    titleEl.appendChild(document.createTextNode('Teoria: ' + (topicName || '')));
    const rawHtml = contentEl ? contentEl.innerHTML.trim() : '';
    bodyEl.innerHTML = rawHtml || '<em class="text-muted">Brak treści</em>';
    showModalById('modalPreviewTheory');
    window.renderMathInElement?.(bodyEl, { clearFirst: true });
}

document.addEventListener('DOMContentLoaded', () => {
    const btnExpandAll = document.getElementById('btnExpandAllChapters');
    const btnCollapseAll = document.getElementById('btnCollapseAllChapters');
    const chapterCollapses = document.querySelectorAll('.chapter-collapse');
    const toggleAllChapters = (action) => {
        chapterCollapses.forEach(el => {
            bootstrap.Collapse.getOrCreateInstance(el, { toggle: false })[action]();
        });
    };
    btnExpandAll?.addEventListener('click', () => toggleAllChapters('show'));
    btnCollapseAll?.addEventListener('click', () => toggleAllChapters('hide'));
    const setChevronRotation = (collapseEl, deg) => {
        const chevron = collapseEl.closest('.chapter-card')?.querySelector('.chapter-chevron');
        if (chevron) chevron.style.transform = `rotate(${deg}deg)`;
    };
    chapterCollapses.forEach(el => {
        el.addEventListener('show.bs.collapse', () => setChevronRotation(el, 180));
        el.addEventListener('hide.bs.collapse', () => setChevronRotation(el, 0));
    });
    const modalNewTopicEl = document.getElementById('modalNewTopic');
    if (modalNewTopicEl) {
        modalNewTopicEl.addEventListener('show.bs.modal', (e) => {
            if (e.relatedTarget) {
                resetNewTopicModal('');
            }
        });
        modalNewTopicEl.addEventListener('shown.bs.modal', () => {
            document.getElementById('topicName')?.focus();
        });
    }
    const formNewTopic = document.getElementById('formNewTopic');
    if (formNewTopic) {
        formNewTopic.addEventListener('submit', (e) => {
            const nameInput = document.getElementById('topicName');
            if (!nameInput) return;
            nameInput.value = nameInput.value.trim();
            if (!nameInput.value) {
                e.preventDefault();
                nameInput.reportValidity();
            }
        });
    }

    document.addEventListener('click', (e) => {
        const btnAddTopic = e.target.closest('.btn-add-topic-for-cat');
        if (btnAddTopic) {
            e.preventDefault();
            openNewTopicForCategory(btnAddTopic.dataset.catId);
            return;
        }
        const btnEditCat = e.target.closest('.btn-edit-cat');
        if (btnEditCat) {
            e.preventDefault();
            openEditCategoryModal(btnEditCat.dataset.catId, btnEditCat.dataset.catName);
            return;
        }
        const btnDeleteCat = e.target.closest('.btn-delete-cat');
        if (btnDeleteCat) {
            e.preventDefault();
            openDeleteCategoryModal(
                btnDeleteCat.dataset.catId,
                btnDeleteCat.dataset.catName,
                parseInt(btnDeleteCat.dataset.topicsCount, 10) || 0
            );
            return;
        }
        const btnPreview = e.target.closest('.btn-preview-theory');
        if (btnPreview) {
            e.preventDefault();
            previewTheory(btnPreview.dataset.topicId, btnPreview.dataset.topicName);
            return;
        }
        const btnDeleteTopic = e.target.closest('.btn-delete-topic');
        if (btnDeleteTopic) {
            e.preventDefault();
            openDeleteTopicModal(btnDeleteTopic.dataset.topicId, btnDeleteTopic.dataset.topicName);
            return;
        }
    });
});
