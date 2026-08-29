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

// Получение настроек из chrome.storage
function getStoredConfig() {
    return new Promise((resolve) => {
        chrome.storage.sync.get(['songchart_server', 'songchart_api_key'], (items) => {
            resolve({
                serverUrl: (items.songchart_server || 'http://127.0.0.1:8000').replace(/\/+$/, ''),
                apiKey: items.songchart_api_key || ''
            });
        });
    });
}

async function sendScrobbleToServer(trackData) {
    try {
        const { serverUrl, apiKey } = await getStoredConfig();

        if (!apiKey) {
            console.warn('[SongChart] Scrobble skipped: API Key is missing. Open the extension popup to set it.');
            return;
        }

        console.log('[SongChart] Sending data to server:', trackData);

        const response = await fetch(`${serverUrl}/api/scrobble`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey  // Передача персонального API-ключа
            },
            body: JSON.stringify(trackData)
        });

        if (!response.ok) {
            const errDetails = await response.text();
            throw new Error(`Server responded with status: ${response.status} - ${errDetails}`);
        }

        const result = await response.json();
        console.log('[SongChart] Server response success:', result);
    } catch (err) {
        console.error('[SongChart] Failed to send scrobble directly to server:', err);
    }
}

let currentTrackKey = '';
console.log('[SongChart DEBUG] content.js successfully initialized with API Key support!');

setInterval(() => {
    const track = getTrackDetails();
    if (track) {
        const trackKey = `${track.artist}-${track.title}`;

        if (trackKey !== currentTrackKey) {
            currentTrackKey = trackKey;
            console.log("[SongChart] New track detected:", trackKey);

            setTimeout(async () => {
                // Повторная проверка актуальности трека перед отправкой
                const currentTrack = getTrackDetails();
                if (currentTrack && `${currentTrack.artist}-${currentTrack.title}` === currentTrackKey) {
                    const payload = {
                        title: track.title,
                        artist: track.artist,
                        time: Math.floor(Date.now() / 1000),
                    };

                    await sendScrobbleToServer(payload);
                }
            }, 3000);
        }
    }
}, 10000);