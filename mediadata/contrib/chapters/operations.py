"""
Chapter operations for merging chapters into audio files
"""

import subprocess
import tempfile
from pathlib import Path

from mutagen.id3 import CHAP, CTOC, CTOCFlags, ID3, TIT2

from mediadata.core.models.chapter import Chapter
from mediadata.utils.log import CoreLogger


def merge_chapters_to_file(file_path: Path, chapters: list[Chapter], file_type: str):
    """
    Merge chapters into an audio file based on file type.

    Args:
        file_path: Path to the audio file
        chapters: List of Chapter objects to merge
        file_type: File type ("MP3" or "MP4")

    Raises:
        ValueError: If file type is not supported
    """

    if file_type == "MP3":
        merge_chapters_mp3(file_path, chapters)
    elif file_type == "MP4":
        merge_chapters_mp4(file_path, chapters)
    else:
        raise ValueError(f"File type {file_type} not supported for chapter merging")


def merge_chapters_mp3(file_path: Path, chapters: list[Chapter]):
    """
    Merge chapters into an MP3 file using ID3v2 CHAP frames.

    MP3 chapters use:
    - CTOC frame: Table of contents that references all chapters
    - CHAP frames: Individual chapter markers with titles

    Args:
        file_path: Path to the MP3 file
        chapters: List of Chapter objects to merge
    """

    logger = CoreLogger().logger
    logger.info("Merging chapters into MP3 file")

    try:
        audio = ID3(file_path)
    except Exception:
        audio = ID3()

    # Remove existing chapter frames
    audio.delall("CTOC")
    audio.delall("CHAP")

    # Create chapter IDs
    chapter_ids = [f"chp{i}" for i in range(len(chapters))]

    # Create CHAP frames for each chapter
    for i, chapter in enumerate(chapters):
        chap_id = chapter_ids[i]

        chap = CHAP(
            encoding=3,
            element_id=chap_id,
            start_time=chapter.start_position,
            end_time=chapter.end_position,
            start_offset=0xFFFFFFFF,  # Not used
            end_offset=0xFFFFFFFF,  # Not used
            sub_frames=[TIT2(encoding=3, text=chapter.title)],
        )
        audio.add(chap)

    # Create table of contents that references all chapters
    ctoc = CTOC(
        encoding=3,
        element_id="toc",
        flags=CTOCFlags.TOP_LEVEL | CTOCFlags.ORDERED,
        child_element_ids=chapter_ids,
        sub_frames=[TIT2(encoding=3, text="Chapters")],
    )
    audio.add(ctoc)

    audio.save(file_path)
    logger.info("Saved %d chapters to MP3 file", len(chapters))


def merge_chapters_mp4(file_path: Path, chapters: list[Chapter]):
    """
    Merge chapters into an MP4/M4B file using ffmpeg.

    MP4/M4B files support chapter metadata via ffmpeg's FFMETADATA format.
    This function creates a temporary metadata file and uses ffmpeg to merge it.

    Args:
        file_path: Path to the MP4/M4B file
        chapters: List of Chapter objects to merge
    """

    logger = CoreLogger().logger
    logger.info("Merging chapters into MP4/M4B file using ffmpeg")

    metadata_content = _create_ffmpeg_metadata(chapters)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as metadata_file:
        metadata_file.write(metadata_content)
        metadata_path = metadata_file.name

    try:
        output_path = file_path.parent / f"{file_path.stem}_temp{file_path.suffix}"

        # Run ffmpeg to add chapters
        cmd = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-i",
            metadata_path,
            "-map_metadata",
            "0",  # Keep original file metadata
            "-map_chapters",
            "1",  # Add chapters from metadata file
            "-codec",
            "copy",
            "-y",  # Overwrite output file
            str(output_path),
        ]

        logger.info("Running ffmpeg to add chapters")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode != 0:
            logger.error("ffmpeg error: %s", result.stderr)
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")

        # Replace original file with new file
        import shutil

        shutil.move(str(output_path), str(file_path))

        logger.info("Saved %d chapters to MP4/M4B file", len(chapters))

    finally:
        import os

        if os.path.exists(metadata_path):
            os.remove(metadata_path)


def _create_ffmpeg_metadata(chapters: list[Chapter]) -> str:
    """
    Create ffmpeg FFMETADATA format for chapters.

    Format:
    ;FFMETADATA1
    [CHAPTER]
    TIMEBASE=1/1000
    START=0
    END=6501309
    title=Chapter 1

    Args:
        chapters: List of Chapter objects

    Returns:
        String containing ffmpeg metadata format
    """

    lines = [";FFMETADATA1"]

    for chapter in chapters:
        lines.append("[CHAPTER]")
        lines.append("TIMEBASE=1/1000")
        lines.append(f"START={chapter.start_position}")
        lines.append(f"END={chapter.end_position}")
        lines.append(f"title={chapter.title}")

    return "\n".join(lines)
