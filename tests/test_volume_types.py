import mock
import unittest

from usage.fields import volume_types


class FakeVolumeType:
    """Model a fake volume type returned by a cinder client."""

    def __init__(self, id, name):
        """Init the fake volume type

        :param id: Id of the volume type
        :type id: str
        :param name: Name of the volume type
        :type name: str
        """
        self.id = id
        self.name = name


class FakeVolumeTypes:
    """Model the fake volume_types portion of the cinder client."""

    def list(self):
        """Return a list of fake volume types.

        :returns: List of fake volume types
        :rtype: list
        """
        return [
            FakeVolumeType('1', 'lvm'),
            FakeVolumeType('2', 'ceph')
        ]


class FakeCinderClient:
    """Model a cinder client for testing purposes."""

    def __init__(self):
        self.volume_types = FakeVolumeTypes()


class FakeClientManager:
    """Model the client manager."""

    def get_cinder(self):
        """Returns an instance of the fake cinder client.

        :returns: A fake cinder client
        :rtype: FakeCinderClient
        """
        return FakeCinderClient()


class TestVolumeTypes(unittest.TestCase):

    @mock.patch(
        'usage.fields.volume_types.get_client_manager',
        return_value=FakeClientManager()
    )
    def test_load_when_none(self, mocked_get):
        self.assertEquals('lvm', volume_types.name_from_id('1'))
        self.assertEquals('ceph', volume_types.name_from_id('2'))
        # Test a known id but no mapping for the id
        self.assertTrue(volume_types.name_from_id('3') is None)
        # Test not having an id.
        self.assertTrue(volume_types.name_from_id(None) is None)
