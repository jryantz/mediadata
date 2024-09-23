"""
Release model
"""

from mediadata.contrib.musicbrainz.models.media import Media
from mediadata.core.models.chapter import Chapter


class Release:
    """
    Release model
    """

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
        """
        Retrieve all chapter objects
        """

        chapters: list[Chapter] = []

        for position in self.media:
            for track in position.tracks:
                previous_chapter = chapters[-1] if len(chapters) > 0 else None
                chapter = Chapter(
                    track.title,
                    previous_chapter.end_position if previous_chapter else 0,
                    track.length,
                )
                chapters.append(chapter)

        return chapters
