// main/static/main/js/api.js
async function fetchDashboardStats() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error(`HTTP: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('[API Error]:', err);
    return null;
  }
}