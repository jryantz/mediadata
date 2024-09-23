"""
File action tests
"""

import unittest

from mediadata.contrib.file.actions import get_chapters_from_start_positions
from mediadata.core.models.chapter import Chapter


class TestFileActions(unittest.TestCase):
    """
    File action tests
    """

    def test_chapters_length_calculation(self):
        """
        Chapters length calculation test
        """

        file_length = 6000
        start_positions = [0, 1000, 2000, 5000]

        chapters = get_chapters_from_start_positions(start_positions, file_length)

        expected_chapters = [
            Chapter("", 0, 1000),
            Chapter("", 1000, 1000),
            Chapter("", 2000, 3000),
            Chapter("", 5000, 1000),
        ]

        self.assertEqual(
            [(chapter.start_position, chapter.end_position) for chapter in chapters],
            [
                (chapter.start_position, chapter.end_position)
                for chapter in expected_chapters
            ],
        )
