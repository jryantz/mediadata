from pathlib import Path

from mediadata.core.management.base import BaseCommand

from mediadata.contrib.file.actions import (
    get_chapters_from_silence as get_file_chapters,
)
from mediadata.contrib.musicbrainz.actions import (
    get_chapters as get_musicbrainz_chapters,
)


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

    def get_file(self, options: dict):
        """Get the file and verify that it exists"""

        input_value = options.get("input")
        input_path = Path(input_value)
        if not input_path.exists():
            raise ValueError(f"File not found: {input_value}")
        absolute_path = input_path.absolute()
        return absolute_path

    def get_action(self, options: dict):
        """Get the action and verify that dependencies are met"""

        action = options.get("action")
        match action:
            case "generate-file":
                source = options.get("source")
                match source:
                    case "detect-silence":
                        pass
                    case "musicbrainz":
                        musicbrainz_id = options.get("musicbrainz_id")

    def handle(self, *args, **options):
        file = self.get_file(options.get("input"))
        action = options.get("action")

        # source = str(options["source"])
        source = options.get("source")

        if source == "musicbrainz":
            id = str(options["musicbrainz_id"])
            x = get_file_chapters(file)
            print(x)
            # data = get_musicbrainz_data(ref)
