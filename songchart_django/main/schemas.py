from datetime import datetime
from typing import Optional
from ninja import Schema

class TrackDetails(Schema):
    title: str
    artist: str
    tag: Optional[str] = "Unknown"
    time: datetime
