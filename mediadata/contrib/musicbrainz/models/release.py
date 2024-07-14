from mediadata.contrib.musicbrainz.models.chapter import Chapter
from mediadata.contrib.musicbrainz.models.media import Media

class Release:
    id: str
    title: str

    media: list[Media]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")

        media = kwargs.get("media")
        self.media = [Media(**media) for media in media]
        self.media.sort(key=lambda x: x.position)

    def get_chapters(self):
        data: list[Chapter] = []

        for position in self.media:
            for track in position.tracks:
                start = track.length + data[-1].position
                chapter = Chapter(track.title, start)
                data.append(chapter)

        return data
