"""
Collection of functions for altering a list of samples.
"""

_COMPUTE_STATUSES = set([
    "active",
    "build",
    "rebuild",
    "resize",
    # "verify_resize",
    "migrating",
])

_CINDER_STATUSES = set([
    'creating',
    'deleting',
    'updating'
])

_WEIRD_STATUSES = _COMPUTE_STATUSES.union(_CINDER_STATUSES)

# Threshold = 60 * 60 * 2 in seconds
_THRESHOLD = 7200


def _is_weird(status):
    """Determine if a status can be considered weird.

    :returns: Bool
    """
    return (status and status.lower() in _WEIRD_STATUSES)


def trim(samples):
    """Trim bad data from the end of a list of samples.

    In order to qualify as bad data,

    A sample must have a "weird" status.
    There must be enough sequential weird status samples at the end of
    a list of samples such that a time threshold is exceeded.

    :param samples: List of samples sorted by timestamp
    :type samples: List
    """
    n = 0
    for i in xrange(len(samples) - 1, -1, -1):
        if _is_weird(samples[i].resource_metadata.get('status')):
            n += 1
        else:
            break

    if n > 1:
        end = samples[-1].timestamp
        start = samples[-n].timestamp
        elapsed = (end - start).total_seconds()
        if (elapsed) > _THRESHOLD:
            del samples[-n:]
