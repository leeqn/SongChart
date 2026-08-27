let lastTrackId = null;

async function updateNowPlaying() {
  try {
    const response = await fetch('/api/now-playing');
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

    const data = await response.json();

    const titleEl = document.getElementById('now-playing-title');
    const artistEl = document.getElementById('now-playing-artist');
    const tagEl = document.getElementById('now-playing-tag');
    const badgeEl = document.getElementById('now-playing-badge');
    const artEl = document.getElementById('now-playing-art');

    if (titleEl) titleEl.innerText = data.title;
    if (artistEl) artistEl.innerText = data.artist;
    if (tagEl) tagEl.innerText = `#${(data.tag || 'SoundCloud').replace(/^#/, '')}`;

    if (data.is_playing) {
      if (badgeEl) {
        badgeEl.innerText = '🔴 LIVE STREAM';
        badgeEl.style.color = '#ff5500';
      }
      if (artEl) {
        artEl.classList.add('spinning');
      }
    } else {
      if (badgeEl) {
        badgeEl.innerText = '⚪ LAST PLAYED';
        badgeEl.style.color = 'var(--text-muted, #a0a0a0)';
      }
      if (artEl) {
        artEl.classList.remove('spinning');
      }
    }

  } catch (error) {
    console.error('Ошибка обновления Now Playing:', error);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateNowPlaying();
  setInterval(updateNowPlaying, 20000);
});