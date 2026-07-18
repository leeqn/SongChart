function getTrackDetails() {
    let title = '';
    let artist = '';

    if (window.location.host.includes('soundcloud')) {
        const playbackControls = document.querySelector('.playbackSoundBadge');
        if (playbackControls) {
            const titleEl = playbackControls.querySelector('.playbackSoundBadge__titleLink span:last-child');
            const artistEl = playbackControls.querySelector('.playbackSoundBadge__lightLink');

            if (titleEl && artistEl) {
                title = titleEl.innerText;
                artist = artistEl.innerText;
            }
        }
    }
    if (title && artist) {
        return { title: title.trim(), artist: artist.trim() };
    }
    return null;
}

async function sendScrobbleToServer(trackData) {
    try {
        console.log('[SongChart] Sending data directly to server:', trackData);
        const response = await fetch('http://127.0.0.1:8000/api/scrobble', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(trackData)
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const result = await response.json();
        console.log('[SongChart] Server response success:', result);
    } catch (err) {
        console.error('[SongChart] Failed to send scrobble directly to server:', err);
    }
}

let currentTrackKey = '';
console.log('[SongChart DEBUG] content.js successfully initialized!');

setInterval(() => {
    const track = getTrackDetails();
    if (track) {
        const trackKey = `${track.artist}-${track.title}`;

        if (trackKey !== currentTrackKey) {
            currentTrackKey = trackKey;
            console.log("[SongChart] New track detected:", trackKey);

            setTimeout(async () => {

                const payload = {
                    title: track.title,
                    artist: track.artist,
                    time: Math.floor(Date.now() / 1000),
                };

                await sendScrobbleToServer(payload);
            }, 2000);
        }
    }
}, 30000);