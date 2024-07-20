class Chapter:
    title: str
    position: int

    def __init__(self, title, position):
        self.title = title
        self.position = position

    def __str__(self):
        return f"{self.timecode} - {self.title}"

    @property
    def timecode(self):
        position = int(self.position)

        seconds = (position / 1000) % 60

        minutes = (position / (1000 * 60)) % 60
        minutes = int(minutes)

        hours = position / (1000 * 60 * 60)

        return "%02d:%02d:%06.3f" % (hours, minutes, seconds)
