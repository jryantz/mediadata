import uuid


def validate_mbid(id: str):
    try:
        uuid.UUID(id)
    except Exception:
        raise ValueError("MusicBrainz ID is not a valid UUID")

    return True
