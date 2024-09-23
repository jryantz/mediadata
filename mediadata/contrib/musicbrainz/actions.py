"""
MusicBrainz actions
"""

import requests

from mediadata.contrib.musicbrainz.models.release import Release
from mediadata.contrib.musicbrainz.validators import validate_mbid


def _get_url(key: str):
    """
    Returns a valid MusicBrainz URL for a given MusicBrainz ID
    """

    if validate_mbid(key):
        return f"https://musicbrainz.org/ws/2/release/{key}"

    return None


def get_data(key: str):
    """
    Retrieves data for a given MusicBrainz ID
    """

    response = requests.get(
        url=_get_url(key),
        params={
            "fmt": "json",
            "inc": "aliases+artist-credits+labels+discids+recordings",
        },
        timeout=10,
    )

    if not response.ok:
        raise ValueError("Couldn't retrieve data from MusicBrainz")

    data = response.json()
    return Release(**data)


def get_chapters(key: str):
    """
    Retrieves chapter data for a given MusicBrainz ID
    """

    release = get_data(key)
    chapters = release.get_chapters()
    return chapters
