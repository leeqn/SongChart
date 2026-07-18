import musicbrainzngs

musicbrainzngs.set_useragent("SongChart-App", "1.0.0", "contact.danya@example.com")

def get_tag(artist: str, title: str):
    search_results=musicbrainzngs.search_recordings(artist=artist.strip(), recording=title.strip(), limit=1)

    if not search_results.get('recording-list'):
        return 'Unknown'

    recording = search_results['recording-list'][0]

    if 'tag-list' in recording:
        tags = sorted(recording['tag-list'], key=lambda x: int(x.get('count', 0)), reverse=True)
        if tags:
            return tags[0]['name'].capitalize()

    if 'artist-credit' in recording:
        artist_info = recording['artist-credit'][0]
        if 'artist' in artist_info and 'id' in artist_info['artist']:
            artist_details = musicbrainzngs.get_artist_by_id(artist_info['artist']['id'], includes=["tags"])
            artist_tags = sorted(artist_details.get('artist', {}).get('tag-list', []),
                                 key=lambda x: int(x.get('count', 0)), reverse=True)
            if artist_tags:
                return artist_tags[0]['name'].capitalize()

    return 'Unknown'