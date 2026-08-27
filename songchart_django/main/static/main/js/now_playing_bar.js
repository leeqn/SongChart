// main/static/main/js/components/now_playing.js
function updateNowPlaying(recentTracks) {
  if (!Array.isArray(recentTracks) || recentTracks.length === 0) return;
  const current = recentTracks[0];

  const titleEl = document.getElementById('title');
  const artistEl = document.getElementById('artist');
  const tagEl = document.getElementById('tag');

  if (titleEl) titleEl.innerText = current.title;
  if (artistEl) artistEl.innerText = current.artist;
  if (tagEl) tagEl.innerText = `#${(current.tag || 'SoundCloud').replace(/^#/, '')}`;
}