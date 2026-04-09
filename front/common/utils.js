function escapeHtml(str) {
    if (typeof str !== 'string') return '';
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return str.replace(/[&<>"']/g, c => map[c]);
}

function showLoading(container) {
    if (typeof container === 'string') container = document.getElementById(container);
    if (!container) return;
    container.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><span>加载中...</span></div>';
}

function hideLoading(container) {
    if (typeof container === 'string') container = document.getElementById(container);
    if (!container) return;
    const spinner = container.querySelector('.loading-spinner');
    if (spinner) spinner.remove();
}
