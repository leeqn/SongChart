# SongChart 🎵

An automated music scrobbling and analytics ecosystem that tracks your listening history directly from SoundCloud, patches missing metadata using open registries, and provides deep statistical insights into your music tastes.

## 🚀 Features

- **Chrome Extension (Manifest V3):** Lightweight content script that monitors the SoundCloud web player in real-time and captures track changes without performance overhead.
- **FastAPI Backend (`serv.py`):** High-performance asynchronous Python REST API that processes incoming scrobbles and securely handles data validation via Pydantic.
- **Smart Metadata Fallback (MusicBrainz API):** A decoupled backend service (`services.py`) that uses the official `musicbrainzngs` client to automatically query and patch missing genre tags for commercial releases if the browser extension reports them as `Unknown`.
- **Relational Storage:** Stores full listening history (Title, Artist, Timestamp, Tags) inside a PostgreSQL database with strict conflict resolution (`ON CONFLICT DO UPDATE`) to prevent duplicate entry drops.
- **Data Analytics (`visualisation.py`):** Leverages Pandas and Seaborn to generate highly readable visualizations, including horizontal bar plots for top-played tracks and distribution charts for favorite genres.

## 🛠️ Tech Stack

- **Frontend:** JavaScript (DOM API, Chrome Extension API Architecture)
- **Backend:** Python 3.10+, FastAPI, Pydantic, MusicBrainz API
- **Database:** PostgreSQL, SQLAlchemy (Core / Expression Language)
- **Data Science & Visualization:** Pandas, Matplotlib, Seaborn

## 📂 Project Structure

```text
SongChart/
├── extension/          # Chrome Extension source
│   ├── manifest.json   # Extension configuration
│   └── content.js      # Player monitor
├── backend/            # Python backend services
│   ├── settings.py     # Settings
│   ├── services.py     # Third-party API integrations (MusicBrainz)
│   └── serv.py         # FastAPI app routes & HTTP request processing
├── visualisation/          # Data analysis scripts
│   └── visualisation.py        # Pandas data processing & Seaborn visualization
└── main.py        # Interactive terminal tool
```
## ⚙️ How It Works
The Chrome Extension detects a track change on SoundCloud and waits 2 seconds for the metadata to render.
It scrapes the artist, title, and page hashtags, then forwards the payload to the local FastAPI server.
If the genre is missing, the backend queries the MusicBrainz database to fetch the artist's or recording's top community tags.
The clean track data is saved into PostgreSQL with an exact timestamp.
The standalone analytics module queries the database to build custom data plots.
## 🐳 Quick Start (Docker)
The easiest way to run the backend and the PostgreSQL database is using Docker Compose.
Clone the repository:

git clone [https://github.com/leeqn/SongChart.git](https://github.com/leeqn/SongChart.git)
cd SongChart

Build and start the containers in detached mode:

docker-compose up -d --build

The FastAPI backend will be available at http://127.0.0.1:8000. You can view the interactive API documentation at http://127.0.0.1:8000/docs.
To stop the services:

docker-compose down
## 📊 CLI Analytics (main.py)
The project includes a powerful CLI tool to generate visual analytics and database statistics directly from your terminal.
python main.py -m <mode> [-d <days>]
Available Commands

Generate horizontal bar charts for your top tracks:
python main.py -m 'track'

Generate charts for your most listened genres/tags:
python main.py -m 'tag'

Analyze your listening habits by time of day (e.g., peak listening hours):
python main.py -m 'hour'

Filter by timeframe:
Use the -d (days) flag to limit the analytics to a specific number of recent days.
Bash
