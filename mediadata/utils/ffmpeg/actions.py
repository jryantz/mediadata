import re
import subprocess
from pathlib import Path

from mediadata.utils.log import CoreLogger


def detect_silence(file_path: Path, silence_duration=4.0):
    """Search for silence in the file with a minimum duration"""

    CoreLogger().logger.info(f"Starting FFmpeg silence detection")

    process = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file_path,
            "-af",
            f"silencedetect=d={silence_duration}",
            "-f",
            "null",
            "-",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    res, err = process.communicate()

    if process.returncode != 0:
        raise Exception(err)

    return res


def extract_chapter_positions_from_response(data):
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
