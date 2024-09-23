"""
MusicBrainz validator
"""

import uuid


def validate_mbid(key: str):
    """
    Validate a MusicBrainz ID
    """

    try:
        uuid.UUID(key)
    except Exception as e:
        raise ValueError("MusicBrainz ID is not a valid UUID") from e

    return True
