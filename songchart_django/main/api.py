from ninja import NinjaAPI
from django.db.models import Count
from sqlalchemy import distinct
from .models import Track
from .schemas import TrackDetails
from .services import services
api = NinjaAPI(title='Song Chart API')

def top_tracks():
    top_tracks_qs = (
        Track.objects.values('title','artist')
        .annotate(plays=Count('id'))
        .order_by('-plays')
    )
    top_tracks=[
        {
            'title':item['title'],
            'artist':item['artist'],
            'plays':item['plays']
        }
        for item in top_tracks_qs
    ]
    return list(top_tracks)

def recent_tracks():
    recent_tracks_qs = (
        Track.objects.order_by('-id')[:10]
    )
    recent_tracks=[
        {
        'title':item.title,
        'artist':item.artist,
        'tag':item.tag,
        'time':(item.time.strftime('%I:%M %p'))
        }
        for item in recent_tracks_qs
    ]
    return list(recent_tracks)

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
        'recent_scrobbles': recent_tracks(),
        'unique_artist': Track.objects.values('artist').distinct().count(),
        'top_tracks': top_tracks(),
        'total_scrobbles': Track.objects.values('title').count(),
        'recent': Track.objects.last().title if Track.objects else 'None',
        'tags': Track.objects.values('tag').distinct().count()
    }