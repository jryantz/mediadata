from pathlib import Path

from mediadata.contrib.file.actions import (
    get_chapters_from_silence,
)
from mediadata.contrib.file.models.file import File
from mediadata.contrib.musicbrainz.actions import (
    get_chapters as get_chapters_from_musicbrainz,
)
from mediadata.contrib.musicbrainz.validators import validate_mbid
from mediadata.core.management.base import BaseCommand
from mediadata.core.models.chapter import Chapter
from mediadata.utils.log import CoreLogger


class Command(BaseCommand):
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
                "musicbrainz",
                "detect-silence",
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

    CoreLogger().logger.info(f"Retrieving file: {options['input'][0]}")

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
                case _:
                    raise ValueError(f"Source {source} not supported")
            return _generate_file, {"file_path": file_path, "chapters": chapters}
        case "merge":
            return _merge, {"file_path": file_path}

    raise ValueError(f"Action {action} not supported")


def _generate_file(file_path: Path, chapters: list[Chapter]):
    CoreLogger().logger.info(f"Generating {len(chapters)} chapters")

    output_file = file_path.parent / f"{file_path.stem}.txt"
    with output_file.open("w", encoding="utf-8") as f:
        for chapter in chapters:
            f.write(f"{str(chapter)}\n")

    CoreLogger().logger.info(f"Wrote {len(chapters)} chapters to file")


def _merge(file_path: Path):
    audio_file_path = file_path
    chapters_file_path = file_path.parent / f"{file_path.stem}.txt"

    audio_file = File(audio_file_path).file
    if type(audio_file).__name__ == "MP4":
        pass

    Chapter.chapters_from_file(chapters_file_path, audio_file.info.length)

    # TODO: Merge the chapters onto the file
