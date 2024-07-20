import requests

from mediadata.contrib.musicbrainz.models.release import Release
from mediadata.contrib.musicbrainz.validators import validate_mbid


def _get_url(id: str):
    if validate_mbid(id):
        return f"https://musicbrainz.org/ws/2/release/{id}"

    return None

def get_data(id: str):
    response = requests.get(
        url=_get_url(id),
        params={
            "fmt": "json",
            "inc": "aliases%2Bartist-credits%2Blabels%2Bdiscids%2Brecordings",
        }
    )

    if not response.ok:
        raise ValueError("Couldn't retrieve data from MusicBrainz")
    
    data = response.json()
    return Release(**data)

def get_chapters(id: str):
    release = get_data(id)
    chapters = release.get_chapters()
