#!/usr/bin/env python3
"""Entry for make.fun news-image-20261127.

Ships the front page for Friday 27 November 2026 ("THE WORLD", drawn at
build time by draw.py) as entry.png and writes it to the grader's output
path. Python 3.13 standard library only, no network, deterministic: the
same bytes on every run, because the bundled image is copied unchanged.
"""
import os
import shutil
import sys

# Bootstrap: the grader runs `python3 -P -s /bot/main.py`, which leaves
# the script's own directory off sys.path. Anchor everything to this
# file's directory so the bundled image is found wherever we run from.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)

_BUNDLED_IMAGE = "entry.png"
_RESULT_NAME = "entry.png"
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def bundled_image_path():
    """Absolute path of the image shipped beside this program."""
    return os.path.join(_BASE_DIR, _BUNDLED_IMAGE)


def pick_destination():
    """Choose where the image is written.

    Priority: ENTRY_OUT (a file path, or a directory that receives
    entry.png) -> MAKEFUN_OUTPUT_DIR (a directory) -> /output/entry.png.
    """
    entry_out = os.environ.get("ENTRY_OUT", "").strip()
    if entry_out:
        if os.path.isdir(entry_out) or entry_out.endswith(os.sep):
            return os.path.join(entry_out, _RESULT_NAME)
        return entry_out

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if output_dir:
        return os.path.join(output_dir, _RESULT_NAME)

    return os.path.join("/output", _RESULT_NAME)


def verify_bundled_png(path):
    """Sanity-check the shipped image: PNG magic plus an IHDR header
    describing a 1024x1024 canvas. A corrupt bundle fails loudly here
    instead of shipping a broken entry."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != _PNG_MAGIC:
        raise ValueError("bundled image is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("bundled PNG has no IHDR chunk")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != (1024, 1024):
        raise ValueError("bundled PNG is %dx%d, expected 1024x1024"
                         % (width, height))


def deliver(source, destination):
    """Copy the bundled image to destination, making parent dirs."""
    parent = os.path.dirname(os.path.abspath(destination))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(source, destination)


def deliver_with_fallback(source, destination):
    """Copy to the chosen destination; if that path is unusable (a
    read-only or missing /output in some sandboxes), fall back to
    ./entry.png in the current working directory as a last resort."""
    try:
        deliver(source, destination)
    except OSError:
        deliver(source, os.path.join(os.getcwd(), _RESULT_NAME))


def run():
    source = bundled_image_path()
    verify_bundled_png(source)
    deliver_with_fallback(source, pick_destination())
    return 0


if __name__ == "__main__":
    sys.exit(run())
