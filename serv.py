from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import settings
from sqlalchemy import create_engine, text
import uvicorn
from services import get_tag

engine = create_engine(settings.POSTGRES)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrackDetails(BaseModel):
    title: str
    artist: str
    time: int

@app.post("/api/scrobble")
def scrobble(track: TrackDetails):
    event_time=datetime.fromtimestamp(track.time)

    try:
        tag=get_tag(track.artist,track.title)
        with engine.begin() as conn:
            conn.execute(text('''
                              INSERT INTO songs (title, artist, tag, time)
                              VALUES(:title, :artist,:tag, :time)
                              ON CONFLICT(title,artist,time) DO NOTHING'''),{
                'title': track.title.strip(),
                'artist': track.artist.strip(),
                'tag': tag,
                'time': event_time,
            })
            conn.commit()
            return {'status':'success','message`':'Track saved'}

    except Exception as exc:
        print(f"error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

