from ninja import NinjaAPI
from .models import Track
from .schemas import TrackDetails
from .services import services
from django.utils import timezone
from datetime import timedelta
api = NinjaAPI(title='Song Chart API')

@api.get('/now-playing')
def now_playing(request):
    track=Track.objects.order_by('-id').first()
    if not track:
        return {
            "is_playing": False,
            "title": "No tracks played yet",
            "artist": "Waiting for stream...",
            "tag": "Offline",
            "time": None,
        }
    is_live=False
    if hasattr(track,'time') and track.time:
        is_live=(timezone.now()-track.time)<timedelta(minutes=5)

    return{
        "is_playing": is_live,
        "title": track.title,
        "artist": track.artist,
        'tag': track.tag,
        "time": track.time.strftime('%I:%M %p')
        if hasattr(track, "time") and track.time
        else "Just now"
        }

@api.post('/scrobble')
def scrobble(request, track: TrackDetails):
    track.tag=services.get_tag(track.artist, track.title)
    track = Track.objects.create(**track.dict())
    return {
        "id": track.id,
        "title": track.title,
        "artist": track.artist,
        "tag": track.tag,
        "status": "created"
    }
@api.get('/stats')
def get_stats(request):
    return {
        'recent_scrobbles': services.recent_tracks(),
        'unique_artist': Track.objects.values('artist').distinct().count(),
        'top_tracks': services.top_tracks(),
        'total_scrobbles': Track.objects.count(),
        'recent': Track.objects.last().title if Track.objects else 'None',
        'tags': Track.objects.values('tag').distinct().count()
    }