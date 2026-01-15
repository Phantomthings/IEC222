function updateTimestamp() {
    const now = new Date();
    const formatted = now.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const timestampEl = document.getElementById('timestamp');
    if (timestampEl) {
        timestampEl.textContent = formatted;
    }
}

function initTimestamp() {
    updateTimestamp();
    setInterval(updateTimestamp, 1000);
}

export { initTimestamp };
