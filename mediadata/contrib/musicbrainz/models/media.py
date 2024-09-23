"""
Media model
"""

from mediadata.contrib.musicbrainz.models.track import Track


class Media:
    """
    Media model
    """

    title: str
    position: int
    track_offset: int
    track_count: int

    format_id: str
    format: str

    tracks: list[Track]

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.position = kwargs.get("position")
        self.track_offset = kwargs.get("track_offset")
        self.track_count = kwargs.get("track_count")

        self.format_id = kwargs.get("format_id")
        self.format = kwargs.get("format")

        tracks = kwargs.get("tracks")
        self.tracks = [Track(**track) for track in tracks]
        self.tracks.sort(key=lambda x: x.position)
