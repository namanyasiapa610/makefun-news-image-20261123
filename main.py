#!/usr/bin/env python3
"""Deliver entry.png for THE DAY AT A GLANCE (akun14, news-image-20261123).

The picture itself — a sepia front page for Monday 23 November 2026 whose
lead card follows gold down to $3,538 an ounce — was composed and frozen
before this program was written. What remains for a program to do is
small and worth doing carefully:

* find the PNG that lives next to this file,
* prove it is still the exact frozen page (size and SHA-256 pinned below),
* copy those bytes, untouched, into MAKEFUN_OUTPUT_DIR (default /output).

Standard library only. The copy is the whole job; nothing is re-encoded,
so repeated runs always produce byte-identical output.
"""

import hashlib
import os
import sys

# The frozen front page, pinned. If either value stops matching, the run
# fails loudly instead of delivering the wrong day's news.
FROZEN_BYTES = 293937
FROZEN_SHA256 = "68d6e1d93c3ae5e1893d8b93e2b89143d518136b8f7fb4d4a8bebfaa9805b339"

HARD_CAP = 1048576  # competition rule: images may not exceed 1 MiB
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_page():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as handle:
        return handle.read()


def verify(page):
    """Check the page against its pins; return its digest when it matches."""
    if len(page) == 0:
        sys.exit("entry.png is empty — nothing to deliver")
    if page[:8] != SIGNATURE:
        sys.exit("entry.png does not start with the PNG signature")
    if len(page) > HARD_CAP:
        sys.exit("entry.png is over the 1 MiB cap (%d bytes)" % len(page))
    if len(page) != FROZEN_BYTES:
        sys.exit("entry.png should be %d bytes, found %d" % (FROZEN_BYTES, len(page)))
    if hashlib.sha256(page).hexdigest() != FROZEN_SHA256:
        sys.exit("entry.png digest does not match the frozen page")
    return hashlib.sha256(page).hexdigest()


def main():
    page = read_page()
    digest = verify(page)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as handle:
        handle.write(page)
    sys.stderr.write("delivered entry.png: %d bytes sha256=%s\n" % (len(page), digest))


if __name__ == "__main__":
    main()
