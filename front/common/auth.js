const API_BASE = '/api';

async function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    try {
        const res = await fetch(`${API_BASE}/verify`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Token invalid');
        const data = await res.json();
        return data;
    } catch (e) {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = 'login.html';
        return false;
    }
}

async function logout() {
    const token = localStorage.getItem('token');
    if (token) {
        try {
            await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
        } catch (e) {}
    }
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('max_teams');
    window.location.href = 'login.html';
}

function getAuthHeaders() {
    return { 'Authorization': `Bearer ${localStorage.getItem('token')}` };
}

async function apiFetch(path, options = {}) {
    const headers = { ...getAuthHeaders(), ...options.headers };
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (res.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = 'login.html';
        return null;
    }
    return res;
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}


