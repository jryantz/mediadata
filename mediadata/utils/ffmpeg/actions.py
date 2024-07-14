import subprocess

def detect_silence(file, silence_duration=4.0):
    """Search for silence in the file with a minimum duration"""

    process = subprocess.Popen([
        "ffmpeg",
        "-i",
        file,
        "-af",
        f"silencedetect=d={silence_duration}",
        "-f",
        "null",
        "-",
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res, err = process.communicate()

    if process.returncode != 0:
        raise Exception(err)

    return res

