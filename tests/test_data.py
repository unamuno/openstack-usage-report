import datetime
import unittest

from fakes import FakeSample
from usage import data

now = datetime.datetime.utcnow()
one_hour_ago = now - datetime.timedelta(hours=1)
two_hours_ago = now - datetime.timedelta(hours=2)
three_hours_ago = now - datetime.timedelta(hours=3)
four_hours_ago = now - datetime.timedelta(hours=4)
five_hours_ago = now - datetime.timedelta(hours=5)


class TestTrim(unittest.TestCase):
    """Tests the data.trim function."""

    def _make_sample(self, timestamp, status='good'):
        return FakeSample(
            timestamp=timestamp,
            resource_metadata={
                "status": status
            }
        )

    def test_empty(self):
        """Test trimming an empty list of samples."""
        samples = []
        data.trim(samples)

    def test_good_data_only(self):
        """Test trimming a list of samples with only good data"""
        samples = [
            self._make_sample(five_hours_ago),
            self._make_sample(four_hours_ago),
            self._make_sample(now)
        ]
        data.trim(samples)
        self.assertEquals(len(samples), 3)

    def test_bad_data_only_exceeds_threshold(self):
        """
        Test trimming list of samples with only bad data
        that exceeds threshold.
        """
        samples = [
            self._make_sample(five_hours_ago, 'build'),
            self._make_sample(four_hours_ago, 'build'),
            self._make_sample(now, 'build')
        ]
        data.trim(samples)
        self.assertEquals(len(samples), 0)

    def test_bad_data_only_within_threshold(self):
        """
        Test trimming list of samples with only bad data
        that does NOT exceed the threshold.
        """
        samples = [
            self._make_sample(now, 'build')
        ]
        data.trim(samples)
        self.assertEquals(len(samples), 1)

    def test_mixed_exceeds_threshold(self):
        """
        Test trimming list of samples with good and bad
        that exceeds threshold.
        """
        samples = [
            self._make_sample(five_hours_ago),
            self._make_sample(four_hours_ago),
            self._make_sample(three_hours_ago, 'build'),
            self._make_sample(one_hour_ago, 'build'),
            self._make_sample(now, 'build')
        ]
        data.trim(samples)
        self.assertEquals(len(samples), 2)
        for s in samples:
            self.assertEquals(s.resource_metadata.get('status'), 'good')

    def test_mixed_within_threshold(self):
        """
        Test trimming list of samples with good and bad
        that does not exceed threshold.
        """
        samples = [
            self._make_sample(five_hours_ago),
            self._make_sample(four_hours_ago),
            self._make_sample(two_hours_ago, 'build'),
            self._make_sample(one_hour_ago, 'build'),
            self._make_sample(now, 'build')
        ]
        data.trim(samples)
        self.assertEquals(len(samples), 5)
