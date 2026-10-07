const API_BASE_URL = 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const token = localStorage.getItem('typebattle_token');
  const headers = { ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  let data = null;
  try { data = await response.json(); } catch { data = {}; }
  if (!response.ok) throw new Error(data.detail || data.message || 'Request failed');
  return data;
}

export const api = {
  register: (payload) => request('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) => request('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  me: () => request('/api/auth/me'),
  savePractice: (payload) => request('/api/practice/result', { method: 'POST', body: JSON.stringify(payload) }),
  practiceHistory: () => request('/api/practice/history'),
  leaderboard: () => request('/api/leaderboard'),
  profile: () => request('/api/profile'),
  saveBattle: (payload) => request('/api/battle/result', { method: 'POST', body: JSON.stringify(payload) }),
};

export function saveSession(data) {
  localStorage.setItem('typebattle_token', data.access_token);
  localStorage.setItem('typebattle_user', JSON.stringify(data.user));
}
export function getUser() {
  try { return JSON.parse(localStorage.getItem('typebattle_user') || 'null'); } catch { return null; }
}
export function logout() {
  localStorage.removeItem('typebattle_token');
  localStorage.removeItem('typebattle_user');
  localStorage.removeItem('typebattle_user_id');
}
