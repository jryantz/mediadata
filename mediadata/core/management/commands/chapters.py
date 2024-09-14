from pathlib import Path

from mediadata.contrib.file.actions import (
    get_chapters_from_silence,
)
from mediadata.contrib.musicbrainz.actions import (
    get_chapters as get_chapters_from_musicbrainz,
)
from mediadata.contrib.musicbrainz.validators import validate_mbid
from mediadata.core.management.base import BaseCommand


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
        file = _get_file(options)
        action, kwargs = _get_action(file, options)
        response = action(**kwargs)
        print(response)


def _get_file(options: dict):
    """Get the file and verify that it exists"""

    input_value = options["input"][0]
    input_path = Path(input_value)
    if not input_path.exists():
        raise ValueError(f"File not found: {input_value}")
    absolute_path = input_path.absolute()
    return absolute_path


def _get_action(file: Path, options: dict):
    """Get the action and verify that dependencies are met"""

    action = options.get("action")
    match action:
        case "generate-file":
            source = options.get("source")
            match source:
                case "detect-silence":
                    return get_chapters_from_silence, {"file": file}
                case "musicbrainz":
                    musicbrainz_id = options.get("musicbrainz_id")
                    validate_mbid(musicbrainz_id)
                    return get_chapters_from_musicbrainz, {"id": musicbrainz_id}

    raise ValueError(f"Action {action} not supported")
