// main/static/main/js/app.js
async function refreshDashboard() {
  const data = await fetchDashboardStats();
  if (!data) return;

  const recent = data.recent_scrobbles || [];

  updateNowPlaying(recent);
  updateScrobblesTable(recent);
  updateCounters(data);
  updateChart(data.top_tracks || []);
}

function updateCounters(data) {
  const totalEl = document.getElementById('total-scrobbles');
  const artistsEl = document.getElementById('unique-artist');
  const tagsEl = document.getElementById('tags');

  if (totalEl) totalEl.innerText = data.total_scrobbles ?? 0;
  if (artistsEl) artistsEl.innerText = data.unique_artist ?? 0;
  if (tagsEl) tagsEl.innerText = data.tags ?? 0;
}

document.addEventListener('DOMContentLoaded', () => {
  refreshDashboard();
  setInterval(refreshDashboard, 4000);
});