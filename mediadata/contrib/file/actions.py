from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from mediadata.core.models.chapter import Chapter
from mediadata.utils.ffmpeg.actions import (
    detect_silence,
    extract_chapter_positions_from_response,
)


def get_chapters_from_start_positions(chapter_start_positions, file_length):
    chapters: list[Chapter] = []

    for i, start in enumerate(chapter_start_positions):
        if i < len(chapter_start_positions) - 1:
            length = chapter_start_positions[i + 1] - start
        else:
            length = file_length - start

        chapter = Chapter(
            "",
            start,
            length,
        )
        chapters.append(chapter)

    return chapters


def get_chapters_from_silence(file, silence_duration=4.0):
    """Identify chapter markers by locating silence in the file"""

    data = detect_silence(file, silence_duration)

    chapter_start_positions = extract_chapter_positions_from_response(data)

    file_type = Path(file).suffix.lower()
    match file_type:
        case ".mp3":
            file_obj = MP3(file)
        case ".m4b":
            file_obj = MP4(file)
        case _:
            raise TypeError(f"File type {file_type} not supported")

    chapters = get_chapters_from_start_positions(
        chapter_start_positions, file_obj.info.length
    )

    return chapters
