from django.db.models.functions import ExtractHour
from django.db.models import Count
from ninja import NinjaAPI, Header
from ninja.security import APIKeyHeader
from ninja.errors import HttpError
from .models import Track, UserProfile
from .schemas import TrackDetails
from .services import services
from django.utils import timezone
from datetime import timedelta, datetime

class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            profile = UserProfile.objects.select_related('user').get(api_key=key)
            return profile.user
        except UserProfile.DoesNotExist:
            return None

auth = ApiKeyAuth()
api = NinjaAPI(title='Song Chart API')

def create_track_record(user, title: str, artist: str, tag: str = None, time_val = None):
    if not tag:
        tag = services.get_tag(artist, title)

    if time_val and isinstance(time_val, (int, float)):
        play_time = datetime.fromtimestamp(time_val, tz=timezone.cest)
    else:
        play_time = timezone.now()

    track = Track.objects.create(
        user=user,
        title=title,
        artist=artist,
        tag=tag or "Unknown",
        time=play_time
    )
    return track
@api.post('/scrobble', auth=auth)
def scrobble(request, track: TrackDetails):
    user = request.auth
    if not user:
        raise HttpError(401, "Invalid or missing API Key")

    new_track = create_track_record(
        user=user,
        title=track.title,
        artist=track.artist,
        tag=getattr(track, 'tag', None)
    )

    return {
        "id": new_track.id,
        "title": new_track.title,
        "artist": new_track.artist,
        "tag": new_track.tag,
        "status": "created"
    }
@api.get('/analytics')
@api.get('/analytics')
def get_analytics(request):
    user = request.user if request.user.is_authenticated else getattr(request, 'auth', None)

    if not user or not user.is_authenticated:
        raise HttpError(401, "Unauthorized")

    user_tracks = Track.objects.filter(user=user)

    top_tags = list(
        user_tracks.values('tag')
        .annotate(tag__count=Count('tag'))
        .order_by('-tag__count')[:5]
    )

    local_tz = timezone.get_current_timezone()
    hourly_tracks = (
        user_tracks.annotate(hour=ExtractHour('time', tzinfo=local_tz))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )

    data_hourly = [0] * 24
    for entry in hourly_tracks:
        if entry['hour'] is not None:
            data_hourly[entry['hour']] = entry['count']

    return {
        "labels": [f"{h:02d}:00" for h in range(24)],
        "counts": data_hourly,
        "top-tags": top_tags
    }

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

@api.post('/scrobble/add', auth=auth)
def scrobble_add(request, track: TrackDetails):
    return scrobble(request, track)

@api.get('/stats')
def get_stats(request, limit: int = 10):
    user = request.user

    if not user.is_authenticated:
        raise HttpError(401, "Unauthorized")

    user_tracks = Track.objects.filter(user=user)
    last_track = user_tracks.order_by('-id').first()

    return {
        'recent_scrobbles': services.recent_tracks(limit, user_tracks) if hasattr(services, 'recent_tracks') else [],
        'unique_artist': user_tracks.values('artist').distinct().count(),
        'top_tracks': services.top_tracks(user_tracks) if hasattr(services, 'top_tracks') else [],
        'total_scrobbles': user_tracks.count(),
        'recent': last_track.title if last_track else 'None',
        'tags': user_tracks.values('tag').distinct().count()
    }