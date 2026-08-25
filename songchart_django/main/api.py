from ninja import NinjaAPI
from .models import Track
from .schemas import TrackDetails
from .services import services
api = NinjaAPI(title='Song Chart API')

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