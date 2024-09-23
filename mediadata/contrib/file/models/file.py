"""
File model
"""

from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from mediadata.utils.log import CoreLogger


class File:
    """
    File model
    """

    file: MP3 | MP4
    path: Path

    def __init__(self, path):
        self.path = path
        self.file = self._file

    @property
    def _file(self):
        file_path = self.path
        file_type = Path(file_path).suffix.lower()
        match file_type:
            case ".mp3":
                file_obj = MP3(file_path)
            case ".m4b":
                file_obj = MP4(file_path)
            case _:
                raise TypeError(f"File type {file_type} not supported")

        CoreLogger().logger.info(
            "Parsing file as %s", file_type.replace(".", "").upper()
        )

        return file_obj
