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

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Chapter):
            return NotImplemented

        return self.title == other.title and self.timecode == other.timecode

    @staticmethod
    def chapters_from_file(file_path, length):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()

        chapters = []
        reversed_lines = list(reversed(lines))
        for i, line in enumerate(reversed_lines):
            content = line.split(" - ")
            title = content[1]
            position = convert_timecode_to_timestamp(content[0])

            if i == 0:
                chapters.append(Chapter(title, position, length))
            else:
                chapters.append(Chapter(title, position, reversed_lines[i - 1]))

        return list(reversed(chapters))

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


def convert_timecode_to_timestamp(timecode):
    hours, minutes, seconds = timecode.split(":")

    hours_to_ms = int(hours) * 1000 * 60 * 60
    minutes_to_ms = int(minutes) * 1000 * 60
    seconds_to_ms = float(seconds) * 1000

    start_position = hours_to_ms + minutes_to_ms + seconds_to_ms

    return start_position
