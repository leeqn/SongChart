function renderTopTracksChart(tracks) {
  const ctx = document.getElementById('topTracksChart')?.getContext('2d');
  if (!ctx) return;

  const labels = tracks.map(t => `${t.artist} - ${t.title}`);
  const plays = tracks.map(t => t.plays);

  if (topTracksChartInstance) {
    topTracksChartInstance.destroy();
  }

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
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          ticks: { color: '#a0a0a0', stepSize: 1 },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y: {
          ticks: { color: '#ffffff', font: { size: 11 } },
          grid: { display: false }
        }
      }
    }
  });
}

function renderRecentScrobbles(tracks) {
  const tbody = document.getElementById('scrobbles-table-body');
  if (!tbody) return;

  if (!tracks || tracks.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="4" style="text-align: center; color: var(--text-muted); padding: 24px;">
          No scrobbles recorded yet
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = tracks.map(track => `
    <tr>
      <td style="font-weight: 600; color: #fff;">${track.title}</td>
      <td>${track.artist}</td>
      <td><span class="tag">#${(track.tag || 'SoundCloud').replace(/^#/, '')}</span></td>
      <td style="color: var(--text-muted); font-size: 0.85rem;">${track.time || 'Just now'}</td>
    </tr>
  `).join('');
}