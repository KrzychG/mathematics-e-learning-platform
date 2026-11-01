function generateStrongPassword() {
    const chars = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%';
    let result = '';
    for (let i = 0; i < 10; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return `${result}1A`;
}

function bindPasswordGenerator(btnId, inputId) {
    const btn = document.getElementById(btnId);
    const input = document.getElementById(inputId);
    if (!btn || !input) return;
    btn.addEventListener('click', () => {
        input.value = generateStrongPassword();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    bindPasswordGenerator('generatePasswordBtn', 'userPasswordField');
    bindPasswordGenerator('generateEditPasswordBtn', 'editUserPasswordField');
    const isActiveCheck = document.getElementById('isActiveCheck');
    const welcomeCheck = document.getElementById('sendWelcomeEmailCheck');
    const welcomeHint = document.getElementById('welcomeEmailBlockedHint');
    if (isActiveCheck && welcomeCheck) {
        const syncWelcomeState = () => {
            const active = isActiveCheck.checked;
            welcomeCheck.disabled = !active;
            if (!active) {
                welcomeCheck.checked = false;
            }
            if (welcomeHint) {
                welcomeHint.classList.toggle('d-none', active);
            }
        };
        syncWelcomeState();
        isActiveCheck.addEventListener('change', syncWelcomeState);
    }
    const editForm = document.getElementById('editUserForm');
    const editFirstName = document.getElementById('editUserFirstName');
    const editEmail = document.getElementById('editUserEmail');
    const editPassword = document.getElementById('editUserPasswordField');
    const editAvatarGroup = document.getElementById('editUserAvatarGroup');
    const editRemoveAvatar = document.getElementById('editUserRemoveAvatar');
    document.addEventListener('click', (event) => {
        const btn = event.target.closest('.btn-edit-user');
        if (!btn || !editForm) return;
        editForm.action = btn.dataset.editUrl || '';
        if (editFirstName) editFirstName.value = btn.dataset.firstName || '';
        if (editEmail) editEmail.value = btn.dataset.email || '';
        if (editPassword) editPassword.value = '';
        const hasAvatar = btn.dataset.hasAvatar === '1';
        if (editAvatarGroup) editAvatarGroup.classList.toggle('d-none', !hasAvatar);
        if (editRemoveAvatar) editRemoveAvatar.checked = false;
    });
    ['addUserModal', 'editUserModal'].forEach((modalId) => {
        const modalEl = document.getElementById(modalId);
        if (modalEl && modalEl.dataset.reopen === '1' && window.bootstrap?.Modal) {
            window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
        }
    });
});
