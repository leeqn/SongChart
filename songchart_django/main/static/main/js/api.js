// main/static/main/js/api.js
async function fetchDashboardStats(limit = 10) {
  try {
    const res = await fetch(`/api/stats?limit=${limit}`);
    if (!res.ok) throw new Error(`HTTP: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('[API Error]:', err);
    return null;
  }
}