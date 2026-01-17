"""
Chapters management command
"""

from pathlib import Path

from mediadata.contrib.chapters.operations import merge_chapters_to_file
from mediadata.contrib.file.actions import get_chapters_from_silence
from mediadata.contrib.file.models.file import File
from mediadata.contrib.musicbrainz.actions import (
    get_chapters as get_chapters_from_musicbrainz,
)
from mediadata.contrib.musicbrainz.validators import validate_mbid
from mediadata.contrib.whisper.actions import get_chapters_from_whisper
from mediadata.core.management.base import BaseCommand
from mediadata.core.models.chapter import Chapter
from mediadata.utils.log import CoreLogger


class Command(BaseCommand):
    """
    Chapters management command
    """

    help = "Generate a chapters file from a selected source"

    def add_arguments(self, parser):
        parser.add_argument(
            "input",
            action="store",
            nargs=1,
            help="",
        )

        parser.add_argument(
            "-a",
            "--action",
            action="store",
            type=str,
            choices=[
                "generate-file",
                "merge",
            ],
            required=True,
            help="",
        )

        parser.add_argument(
            "-s",
            "--source",
            action="store",
            type=str,
            choices=[
                "detect-silence",
                "musicbrainz",
                "whisper",
            ],
            help="",
        )

        parser.add_argument(
            "--musicbrainz-id",
            action="store",
            type=str,
            help="",
        )

    def handle(self, *args, **options):
        file_path = _get_file(options)
        action, kwargs = _get_action(file_path, options)
        action(**kwargs)


def _get_file(options: dict):
    """Get the file and verify that it exists"""

    input_value = options["input"][0]
    input_path = Path(input_value)

    CoreLogger().logger.info("Retrieving file: %s", options["input"][0])

    if not input_path.exists():
        raise ValueError(f"File not found: {input_value}")
    absolute_path = input_path.absolute()
    return absolute_path


def _get_action(file_path: Path, options: dict):
    """Get the action and verify that dependencies are met"""

    action = options.get("action")
    match action:
        case "generate-file":
            source = options.get("source")
            match source:
                case "detect-silence":
                    chapters = get_chapters_from_silence(file_path)
                case "musicbrainz":
                    musicbrainz_id = options.get("musicbrainz_id")
                    validate_mbid(musicbrainz_id)
                    chapters = get_chapters_from_musicbrainz(musicbrainz_id)
                case "whisper":
                    chapters = get_chapters_from_whisper(file_path)
                case _:
                    raise ValueError(f"Source {source} not supported")
            return _generate_file, {"file_path": file_path, "chapters": chapters}
        case "merge":
            return _merge, {"file_path": file_path}

    raise ValueError(f"Action {action} not supported")


def _generate_file(file_path: Path, chapters: list[Chapter]):
    CoreLogger().logger.info("Generating %s chapters", len(chapters))

    output_file = file_path.parent / f"{file_path.stem}.txt"
    with output_file.open("w", encoding="utf-8") as f:
        for chapter in chapters:
            f.write(f"{str(chapter)}\n")

    CoreLogger().logger.info("Wrote %s chapters to file", len(chapters))


def _merge(file_path: Path):
    """
    Merge chapters from a text file into an audio file.

    Reads chapters from a .txt file and writes them to the audio file metadata.
    Supports MP3 (via ID3v2 CHAP frames) and MP4/M4B (via chapter atoms).
    """

    logger = CoreLogger().logger
    audio_file_path = file_path
    chapters_file_path = file_path.parent / f"{file_path.stem}.txt"

    if not chapters_file_path.exists():
        raise ValueError(
            f"Chapters file not found: {chapters_file_path}. "
            f"Generate it first with --action generate-file"
        )

    logger.info("Reading chapters from: %s", chapters_file_path)

    audio_file = File(audio_file_path).file
    file_type = type(audio_file).__name__

    file_length_ms = int(audio_file.info.length * 1000)
    chapters = Chapter.chapters_from_file(chapters_file_path, file_length_ms)
    logger.info("Loaded %d chapters from file", len(chapters))

    merge_chapters_to_file(audio_file_path, chapters, file_type)

    logger.info(
        "Successfully merged %d chapters into %s", len(chapters), file_path.name
    )
