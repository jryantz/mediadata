import re

from mediadata.utils.ffmpeg.actions import detect_silence


def _get_timecode(milliseconds):
    """Convert milliseconds to timecode"""

    position = int(milliseconds)

    seconds = (position / 1000) % 60

    minutes = (position / (1000 * 60)) % 60
    minutes = int(minutes)

    hours = position / (1000 * 60 * 60)

    return "%02d:%02d:%06.3f" % (hours, minutes, seconds)


def get_chapters_from_silence(file, silence_duration=4.0):
    """Identify chapter markers by locating silence in the file"""

    data = detect_silence(file, silence_duration)

    # Decode command response and split by line
    lines = data.decode('utf-8').split('\n')

    # Filter the output lines
    matches = [re.search(r'silence_(start|end): [0-9.]+', x) for x in lines]

    # Filter out the None values and extract matches
    matches = [x.group() for x in matches if x]
    
    # Extract the values
    values = [float(x.split(':')[1].strip()) for x in matches if "end" in x]

    # Add the start value
    if values[0] != 0:
        values = [0.0] + values

    timecodes = [_get_timecode(x * 1000) for x in values]

    return timecodes
