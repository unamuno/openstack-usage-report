import logging
import pprint
from usage.clients import get_client_manager

logger = logging.getLogger('usage.fields.volume_types')
_TYPE_MAP = None


def _load_type_map():
    """Load a map of volume type ids to names.

    Store the result in the module variable _TYPE_MAP
    """
    global _TYPE_MAP
    try:
        cinder = get_client_manager().get_cinder()
        volume_types = cinder.volume_types.list()
        _TYPE_MAP = {t.id: t.name for t in volume_types}
    except Exception:
        logger.exception('Unable to load volume types.')
        _TYPE_MAP = {}


def name_from_id(type_id):
    """Get the volume type name from the volume type id.

    :param type_id: Volume type id
    :type type_id: str
    :returns: The name of the volume type
    :rtype: str
    """
    # Load the type map on the first use
    if _TYPE_MAP is None:
        _load_type_map()

    # Don't bother if we do not have a type id
    if type_id is None:
        return None

    # Return the type name for the given type id
    return _TYPE_MAP.get(type_id)
