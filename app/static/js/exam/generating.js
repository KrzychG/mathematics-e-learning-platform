document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('examGeneratingCard');
    if (!card) return;
    const csrfToken = card.dataset.csrfToken || '';
    const startUrl = card.dataset.startUrl || '';
    const lobbyUrl = card.dataset.lobbyUrl || '/';
    window.apiFetchJson(startUrl, {
        method: 'POST',
        csrfToken,
        errorMessage: 'Błąd serwera podczas generowania egzaminu.'
    })
    .then(data => {
        window.location.href = (data && data.redirect_url) ? data.redirect_url : lobbyUrl;
    })
    .catch(error => {
        console.error('Błąd generowania egzaminu:', error);
        window.location.href = lobbyUrl;
    });
});
