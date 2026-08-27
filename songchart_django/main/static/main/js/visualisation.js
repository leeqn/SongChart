// main/static/main/js/components/visualisation.js
let topTracksChartInstance = null;

function updateScrobblesTable(tracks) {
  const tbody = document.getElementById('scrobbles-table-body');
  if (!tbody) return;

  if (!Array.isArray(tracks) || tracks.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 24px;">No scrobbles recorded yet</td></tr>`;
    return;
  }

  tbody.innerHTML = tracks.map(t => `
    <tr>
      <td style="font-weight: 600; color: #fff;">${t.title}</td>
      <td>${t.artist}</td>
      <td><span class="tag">#${(t.tag || 'SoundCloud').replace(/^#/, '')}</span></td>
      <td style="color: var(--text-muted); font-size: 0.85rem;">${t.time || 'Just now'}</td>
    </tr>
  `).join('');
}

function updateChart(tracks, limit=5) {
  const canvas = document.getElementById('topTracksChart');
  if (!canvas || typeof Chart === 'undefined') return;

  if (!Array.isArray(tracks)) {
    tracks = [];
  }

  const topTracks = tracks.slice(0, limit);
  const labels = topTracks.map(t => `${t.artist} - ${t.title}`);
  const plays = topTracks.map(t => t.plays);

  if (topTracksChartInstance) {
    topTracksChartInstance.data.labels = labels;
    topTracksChartInstance.data.datasets[0].data = plays;
    topTracksChartInstance.update('none');
    return;
  }

  const ctx = canvas.getContext('2d');
  topTracksChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Plays',
        data: plays,
        backgroundColor: 'rgba(255, 85, 0, 0.75)',
        borderColor: '#ff5500',
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#a0a0a0', stepSize: 1 }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
        y: { ticks: { color: '#ffffff', font: { size: 11 } }, grid: { display: false } }
      }
    }
  });
}