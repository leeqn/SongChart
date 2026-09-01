// main/static/main/js/analytics.js
let hourlyChartInstance = null;
let topTracksChartInstance = null;
let topArtistsChartInstance = null;

function circleChart(tracks, limit = 8) {
  const canvas = document.getElementById('topTracksChart');
  if (!canvas || typeof Chart === 'undefined') return;

  if (!Array.isArray(tracks)) {
    tracks = [];
  }

  const topTracks = tracks.slice(0, limit);
  const labels = topTracks.map(t => `${t.artist || 'Unknown'} - ${t.title || 'Unknown'}`);
  const plays = topTracks.map(t => t.plays ?? 0);

  const colors = [
    '#ff5500', '#ff7a33', '#ffa066', '#ffc499',
    '#06d6a0', '#118ab2', '#8338ec', '#3a86ff'
  ];

  if (topTracksChartInstance) {
    topTracksChartInstance.data.labels = labels;
    topTracksChartInstance.data.datasets[0].data = plays;
    topTracksChartInstance.update('none');
    return;
  }

  const ctx = canvas.getContext('2d');
  topTracksChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: 'Plays',
        data: plays,
        backgroundColor: colors.slice(0, topTracks.length),
        borderColor: '#18181b',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'right',
          labels: {
            color: '#a0a0a0',
            font: { size: 12 },
            boxWidth: 14,
            padding: 16
          }
        }
      }
    }
  });
}

function renderHourlyHistPlot(labels, counts) {
  const canvas = document.getElementById('hourlyHistChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const ctx = canvas.getContext('2d');

  if (hourlyChartInstance) {
    hourlyChartInstance.data.labels = labels;
    hourlyChartInstance.data.datasets[0].data = counts;
    hourlyChartInstance.update('none');
    return;
  }

  hourlyChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels, // ['00:00', '01:00', ..., '23:00']
      datasets: [{
        label: 'Scrobbles',
        data: counts,
        backgroundColor: 'rgba(255, 85, 0, 0.75)',
        borderColor: '#ff5500',
        borderWidth: 1,
        borderRadius: 2,

        categoryPercentage: 1.0,
        barPercentage: 0.9
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => `Time: ${items[0].label}`,
            label: (item) => `Tracks played: ${item.raw}`
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#a0a0a0',
            font: { size: 10 },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 12
          },
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#a0a0a0', stepSize: 1 },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      }
    }
  });
}


function renderTopArtistsChart(artist_labels, counts) {
  const canvas = document.getElementById('topArtistsChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const labels = artist_labels || [];
  const data = counts || [];

  if (topArtistsChartInstance) {
    topArtistsChartInstance.data.labels = artist_labels;
    topArtistsChartInstance.data.datasets[0].data = counts;
    topArtistsChartInstance.update('none');
    return;
  }

  const ctx = canvas.getContext('2d');
  topArtistsChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Scrobbles',
        data: data,
        backgroundColor: 'rgba(255, 122, 51, 0.75)',
        borderColor: '#ff7a33',
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => ` ${context.raw} scrobbles`
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { color: '#a0a0a0', precision: 0 },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y: {
          ticks: { color: '#a0a0a0', font: { size: 11 } },
          grid: { display: false }
        }
      }
    }
  });
}

async function loadHourlyStats() {
  try {
    const res = await fetch('/api/analytics');
    if (!res.ok) return;
    const data = await res.json();
    renderHourlyHistPlot(data.labels, data.counts);
    renderTopArtistsChart(data.artist_labels, data.artist_counts);
  } catch (err) {
    console.error('[Analytics Load Error]:', err);
  }
}

async function loadTopTracks() {
  if (typeof fetchDashboardStats !== 'function') return;
  try {
    const data = await fetchDashboardStats(10);
    if (data && data.top_tracks) {
      circleChart(data.top_tracks, 8);
    }
  } catch (err) {
    console.error('[Top Tracks Load Error]:', err);
  }
}

async function refreshAnalytics() {
  await Promise.allSettled([
    loadHourlyStats(),
    loadTopTracks()
  ]);
}

document.addEventListener('DOMContentLoaded', () => {
  refreshAnalytics();
  setInterval(refreshAnalytics, 5000);
});