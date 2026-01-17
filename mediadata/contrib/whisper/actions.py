import re
from pathlib import Path

import torch
import whisper

from mediadata.contrib.file.models.file import File
from mediadata.core.models.chapter import Chapter
from mediadata.utils.log import CoreLogger


def _get_device():
    """
    Detect the best available device for Whisper inference.

    Returns:
        str: Device name - "mps" for Apple Silicon, "cuda" for NVIDIA GPU, or "cpu"
    """

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def get_chapters_from_whisper(file_path: Path):
    """
    Identify chapter markers by locating chapter markers using transcription.

    This function:
    1. Transcribes the audio using Whisper
    2. Identifies chapter positions by detecting chapter markers in the transcription
    3. Returns a list of Chapter objects with positions and titles
    """

    logger = CoreLogger().logger

    device = _get_device()
    device_name = {
        "mps": "Apple Silicon GPU (Metal)",
        "cuda": "NVIDIA GPU (CUDA)",
        "cpu": "CPU",
    }.get(device, device)

    logger.info("Using device: %s", device_name)
    logger.info("Loading Whisper model")
    model = whisper.load_model("tiny.en", device=device)

    logger.info("Loading audio file: %s", file_path)
    audio = whisper.load_audio(str(file_path))

    logger.info("Transcribing audio on %s (this may take a while)", device_name)

    result = model.transcribe(audio, word_timestamps=False)

    file = File(file_path).file
    file_length_ms = int(file.info.length * 1000)

    logger.info("Analyzing transcription for chapter markers")
    chapters = extract_chapters_from_transcription(result, file_length_ms)

    logger.info("Found %d chapters in transcription", len(chapters))

    return chapters


def extract_chapters_from_transcription(transcription_result, file_length):
    """
    Extract chapter markers from Whisper transcription result.

    Looks for patterns like:
    - "Chapter 1", "Chapter One", "Chapter Two"
    - "Part 1", "Part One"
    - "Section 1"
    - Common section names: "Introduction", "Prologue", "Epilogue", "Conclusion"
    """

    chapters = []
    segments = transcription_result.get("segments", [])

    # Patterns to identify chapter markers
    chapter_patterns = [
        r"\b(chapter)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
        r"nineteen|twenty)\b",
        r"\b(part)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b",
        r"\b(section)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b",
        r"\b(introduction|prologue|preface|foreword|epilogue|conclusion|"
        r"appendix|afterword)\b",
    ]

    compiled_patterns = [
        re.compile(pattern, re.IGNORECASE) for pattern in chapter_patterns
    ]

    for segment in segments:
        text = segment.get("text", "").strip()
        start_time = segment.get("start", 0)

        # Check each pattern
        for pattern in compiled_patterns:
            match = pattern.search(text)
            if match:
                chapter_title = extract_chapter_title(text, match)
                position_ms = int(start_time * 1000)

                chapters.append(
                    {"title": chapter_title, "position": position_ms, "text": text}
                )

                CoreLogger().logger.debug(
                    "Found chapter at %d ms: %s", position_ms, chapter_title
                )
                break

    # If no chapters found, create a single chapter for the whole file
    if not chapters:
        CoreLogger().logger.warning(
            "No chapter markers found in transcription, creating single chapter"
        )
        return [Chapter("Full Recording", 0, file_length)]

    # Convert to Chapter objects with proper lengths
    chapter_objects = []
    for i, chapter_data in enumerate(chapters):
        # Calculate length: distance to next chapter or end of file
        if i < len(chapters) - 1:
            length = chapters[i + 1]["position"] - chapter_data["position"]
        else:
            length = file_length - chapter_data["position"]

        chapter_objects.append(
            Chapter(chapter_data["title"], chapter_data["position"], length)
        )

    return chapter_objects


def extract_chapter_title(text, match):
    """
    Extract a clean chapter title from the matched text.

    Tries to extract the full sentence or phrase containing the chapter marker.
    """

    # Get the matched chapter marker
    marker = match.group(0)

    # Try to extract the sentence containing the marker
    # Look for common sentence boundaries
    sentences = re.split(r"[.!?]\s+", text)
    for sentence in sentences:
        if marker.lower() in sentence.lower():
            # Clean up and return the sentence
            title = sentence.strip()
            # Capitalize first letter
            if title:
                title = title[0].upper() + title[1:]
            return title

    # Fallback: just return the marker capitalized
    return marker.title()
