from django.db.models.functions import ExtractHour
from django.db.models import Count
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Header
from .models import Track, UserProfile
from .schemas import TrackDetails
from .services import services
from django.utils import timezone
from datetime import timedelta
api = NinjaAPI(title='Song Chart API')
@api.get('/scrobble/add')
def scrobble_add(request, payload:dict, x_api_key:str=Header(...)):
    profile_user=get_object_or_404(UserProfile, api_key=x_api_key)
    user=profile_user
    track = Track.objects.create(
        user=user,
        title=payload.get("title"),
        artist=payload.get("artist"),
        tag=payload.get("tag", "")
    )
    return {"status": "ok", "track_id": track.id}
@api.get('/analytics')
def get_analytics(request):
    top_tags=list(Track.objects.values('tag').annotate(Count('tag')).order_by('-tag'))
    hourly_tracks = (Track.objects.annotate(hour=ExtractHour('time'))
                    .values('hour')
                    .annotate(count=Count('id'))
                    .order_by('hour'))
    data_hourly=[0]*24
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
def get_stats(request, limit:int=10):
    if not request.user.is_authenticated:
        return {'error': "Unauthorized"}, 401

    user_tracks = Track.objects.filter(user=request.user)

    return {
        'recent_scrobbles': services.recent_tracks(limit, user_tracks),
        'unique_artist': user_tracks.values('artist').distinct().count(),
        'top_tracks': services.top_tracks(user_tracks),
        'total_scrobbles': user_tracks.count(),
        'recent': user_tracks.last().title if user_tracks else 'None',
        'tags': user_tracks.values('tag').distinct().count()
    }