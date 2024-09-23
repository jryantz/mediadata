import tempfile
import unittest

from mediadata.core.models import chapter


class TestChapterCreation(unittest.TestCase):
    def test_chapters_from_file(self):
        file_content_list = [
            "00:00:00.000 - Chapter 1",
            "00:01:00.000 - Chapter 2",
            "01:00:00.000 - Chapter 3",
        ]

        expected_chapters = [
            chapter.Chapter("Chapter 1", 0, 60_000),
            chapter.Chapter("Chapter 2", 60_000, 3_600_000),
            chapter.Chapter("Chapter 3", 3_600_000, 3_601_000),
        ]

        file = tempfile.NamedTemporaryFile("w+")
        file.write("\n".join(file_content_list))
        file.seek(0)

        chapters = chapter.Chapter.chapters_from_file(file.name, 3_601_000)

        file.close()

        self.assertListEqual(expected_chapters, chapters)
