"""
Chapter position conversion tests
"""

import unittest

from mediadata.core.models import chapter


class TestChapterPositionConversion(unittest.TestCase):
    """
    Chapter position conversion tests
    """

    def test_timestamp_from_timecode_0s(self):
        """
        Test 0 seconds timecode conversion to timestamp
        """

        timecode = "00:00:00.000"
        expected_timestamp = 0

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_1m(self):
        """
        Test 1 minute timecode conversion to timestamp
        """

        timecode = "00:01:00.000"
        expected_timestamp = 60_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_5m(self):
        """
        Test 5 minute timecode conversion to timestamp
        """

        timecode = "00:05:00.000"
        expected_timestamp = 300_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_10m(self):
        """
        Test 10 minute timecode conversion to timestamp
        """

        timecode = "00:10:00.000"
        expected_timestamp = 600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_20m(self):
        """
        Test 20 minute timecode conversion to timestamp
        """

        timecode = "00:20:00.000"
        expected_timestamp = 1_200_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_30m(self):
        """
        Test 30 minute timecode conversion to timestamp
        """

        timecode = "00:30:00.000"
        expected_timestamp = 1_800_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_60m(self):
        """
        Test 60 minute timecode conversion to timestamp
        """

        timecode = "00:60:00.000"
        expected_timestamp = 3_600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_1h(self):
        """
        Test 1 hour timecode conversion to timestamp
        """

        timecode = "01:00:00.000"
        expected_timestamp = 3_600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_10h(self):
        """
        Test 10 hour timecode conversion to timestamp
        """

        timecode = "10:00:00.000"
        expected_timestamp = 36_000_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_100h(self):
        """
        Test 100 hour timecode conversion to timestamp
        """

        timecode = "100:00:00.000"
        expected_timestamp = 360_000_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)
