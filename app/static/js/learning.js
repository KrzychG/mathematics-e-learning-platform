document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('learningDeskWrapper')) return;
    const togglePanel = (e) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        const syllabus = document.getElementById('syllabusPanel');
        const workspace = document.getElementById('workspacePanel');
        const toggleBtnIcon = document.querySelector('#toggleSyllabusBtn i');
        if (!syllabus || !workspace) return;
        const isHidden = syllabus.classList.toggle('d-none');
        if (toggleBtnIcon) {
            toggleBtnIcon.classList.toggle('bi-layout-sidebar', isHidden);
            toggleBtnIcon.classList.toggle('bi-layout-sidebar-inset', !isHidden);
        }
    };
    const bindWorkspaceEvents = () => {
        const innerToggleBtn = document.getElementById('toggleSyllabusBtn');
        if (innerToggleBtn) {
            innerToggleBtn.onclick = togglePanel;
        }
        document.querySelectorAll('.ajax-link').forEach(link => {
            link.onclick = async (e) => {
                e.preventDefault();
                const url = link.getAttribute('href');
                try {
                    const response = await fetch(url);
                    if (!response.ok || response.redirected) {
                        window.location.href = response.url || url;
                        return;
                    }
                    const html = await response.text();
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const oldSyllabus = document.getElementById('syllabusPanel');
                    const newSyllabus = doc.getElementById('syllabusPanel');
                    const oldWorkspace = document.getElementById('workspacePanel');
                    const newWorkspace = doc.getElementById('workspacePanel');
                    if (!newWorkspace) {
                        window.location.href = response.url || url;
                        return;
                    }
                    if (oldSyllabus && newSyllabus) {
                        const scrollPosition = oldSyllabus.scrollTop;
                        oldSyllabus.innerHTML = newSyllabus.innerHTML;
                        oldSyllabus.scrollTop = scrollPosition;
                    }
                    if (oldWorkspace && newWorkspace) {
                        oldWorkspace.innerHTML = newWorkspace.innerHTML;
                    }
                    window.history.pushState({}, "", url);
                    bindWorkspaceEvents();
                    window.renderMathInElement?.(oldWorkspace || document.body);
                } catch (error) {
                    window.location.href = url;
                }
            };
        });
    };
    bindWorkspaceEvents();
    window.addEventListener('popstate', () => {
        window.location.reload();
    });
});
