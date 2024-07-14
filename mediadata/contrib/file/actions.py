import re

from mediadata.utils.ffmpeg.actions import detect_silence


def get_chapters_from_silence(file, silence_duration=4.0):
    """Identify chapter markers by locating silence in the file"""

    data = detect_silence(file, silence_duration)

    # Decode command response and split by line
    lines = data.decode("utf-8").split("\n")

    # Filter the output lines
    matches = [re.search(r"silence_(start|end): [0-9.]+", x) for x in lines]

    # Filter out the None values and extract matches
    matches = [x.group() for x in matches if x]

    # Extract the values
    values = [int(float(x.split(":")[1].strip()) * 1000) for x in matches if "end" in x]

    # Add the start value
    if values[0] != 0:
        values = [0] + values

    return values
