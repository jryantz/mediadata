"""
Track model
"""


class Track:
    """
    Track model
    """

    id: str
    title: str
    position: int
    length: int

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.position = kwargs.get("position")
        self.length = kwargs.get("length")
