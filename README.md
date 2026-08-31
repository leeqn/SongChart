# 🎵 SongChart

**SongChart** is a real-time music analytics and track scrobbling platform (with SoundCloud support). It tracks your music listening habits, enriches track metadata, and provides real-time dashboard analytics.

The project consists of two core components:
1. **Chrome Extension** — A lightweight browser extension that monitors active media playback in real time and sends scrobble payloads to the backend.
2. **Django Backend & Dashboard** — A web application providing REST APIs for ingestion, track/artist data processing, and an interactive analytics dashboard.

---

## 🚀 Features

- 🎧 **Real-time Scrobbling:** Background playback tracking with SoundCloud support.
- 📊 **Music Analytics:** Real-time stats for total scrobbles, unique artists, top tracks, and patched tags.
- 🔑 **API Key Authentication:** Secure scrobble ingestion via personalized API keys.
- 🌐 **Web Dashboard:** Interactive overview and comprehensive scrobble history log.
- ☁️ **Cloud Native (CI/CD):** Continuous deployment to **Azure App Service** via **GitHub Actions**.

---

## 🏗 Project Structure

```text
SongChart/
├── .github/
│   └── workflows/          # GitHub Actions (CI/CD pipeline for Azure)
├── extension/              # Browser extension (Manifest V3)
│   ├── manifest.json       # Extension configuration
│   ├── content.js          # SoundCloud player scraper & observer
│   ├── popup.html          # Extension popup UI
│   └── popup.js            # API key setup and connection logic
├── songchart_django/       # Django backend application
│   ├── main/               # Core application (models, views, API, templates, static)
│   ├── songchart_django/   # Project settings (settings.py, urls.py, wsgi.py)
│   ├── manage.py
│   └── requirements.txt
├── requirements.txt        # Root dependencies for Azure Oryx builder
└── README.md


⚙️ Local Development Setup

1. Clone the repository
Bash
git clone [https://github.com/leeqn/SongChart.git](https://github.com/leeqn/SongChart.git)
cd SongChart

2. Create and activate a virtual environment
Bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure environment variables
Create a .env file inside the songchart_django/ directory:
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

4. Run migrations and collect static files
Bash
cd songchart_django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Optional: create admin account

5. Start the development server
Bash
python manage.py runserver
Access the dashboard at http://127.0.0.1:8000/.

☁️ Azure Deployment Configuration
This repository is configured for automated deployment to Azure App Service:
Startup Command:
Bash
gunicorn --chdir songchart_django --bind=0.0.0.0:8000 --timeout 600 songchart_django.wsgi:application
Static Assets: Handled in production via WhiteNoise (STORAGES / STATIC_ROOT), eliminating the need for a separate reverse proxy.
