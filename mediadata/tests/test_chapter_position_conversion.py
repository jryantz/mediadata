import unittest

from mediadata.core.models import chapter


class TestChapterPositionConversion(unittest.TestCase):
    def test_timestamp_from_timecode_0s(self):
        timecode = "00:00:00.000"
        expected_timestamp = 0

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_1m(self):
        timecode = "00:01:00.000"
        expected_timestamp = 60_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_5m(self):
        timecode = "00:05:00.000"
        expected_timestamp = 300_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_10m(self):
        timecode = "00:10:00.000"
        expected_timestamp = 600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_20m(self):
        timecode = "00:20:00.000"
        expected_timestamp = 1_200_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_30m(self):
        timecode = "00:30:00.000"
        expected_timestamp = 1_800_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_60m(self):
        timecode = "00:60:00.000"
        expected_timestamp = 3_600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_1h(self):
        timecode = "01:00:00.000"
        expected_timestamp = 3_600_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_10h(self):
        timecode = "10:00:00.000"
        expected_timestamp = 36_000_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_from_timecode_100h(self):
        timecode = "100:00:00.000"
        expected_timestamp = 360_000_000

        timestamp = chapter.convert_timecode_to_timestamp(timecode)

        self.assertEqual(expected_timestamp, timestamp)
