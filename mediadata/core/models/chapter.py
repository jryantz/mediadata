class Chapter:
    title: str
    _position: int
    _length: int

    def __init__(self, title, position, length):
        self.title = title
        self._position = position
        self._length = length

    def __str__(self):
        return f"{self.timecode} - {self.title}"

    @property
    def start_position(self):
        return self._position

    @property
    def end_position(self):
        return self._position + self._length

    @property
    def timecode(self):
        position = int(self.start_position)

        seconds = (position / 1000) % 60

        minutes = (position / (1000 * 60)) % 60
        minutes = int(minutes)

        hours = position / (1000 * 60 * 60)

        return "%02d:%02d:%06.3f" % (hours, minutes, seconds)
