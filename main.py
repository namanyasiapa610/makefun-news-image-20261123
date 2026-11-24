#!/usr/bin/env python3
"""THE DAY AT A GLANCE — entry program for news-image-20261123 (akun14, G4).

The newspaper is a one-page front sheet for Monday 23 November 2026:
pale sepia paper, midnight-blue ink, silver accents, and a gold lead —
the day world markets watched bullion slide to $3,538 an ounce.

STDLIB ONLY, COPY ONLY. This program copies the finished entry.png that
sits beside it into the output directory, after checking the byte count
and digest so a truncated or swapped image can never slip through.
No PIL, no network, no randomness: two runs write identical bytes.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 293645
EXPECTED_SHA256 = "4f697d321d57d03dcbab018b99e838696ecec49168ed82153ac97e8ff6f59987"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # the competition's hard 1 MiB cap


def load_entry():
    """Read entry.png from this file's own directory, ready to validate."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        return fh.read()


def check_image(data):
    """Refuse anything that is not exactly the composed front page."""
    if not data:
        sys.exit("entry.png is empty")
    if data[:8] != PNG_MAGIC:
        sys.exit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds the 1 MiB cap: %d bytes" % len(data))
    if len(data) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size drifted: %d bytes, expected %d"
            % (len(data), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch: %s" % digest)
    return digest


def main():
    data = load_entry()
    digest = check_image(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)
    sys.stderr.write("entry.png: %d bytes sha256=%s\n" % (len(data), digest))


if __name__ == "__main__":
    main()
