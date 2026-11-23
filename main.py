#!/usr/bin/env python3
"""news-22 b14 utc-timeline entrypoint: copy entry.png to the output dir.

The grader runs this program twice in a sandbox with a read-only /bot
(the repository) and a writable /output. It must never write next to
main.py: the destination is always $MAKEFUN_OUTPUT_DIR/entry.png.
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dst_hash:
        print("FAIL: sha256 mismatch", src_hash, dst_hash, file=sys.stderr)
        return 1
    # Verify the PNG header ourselves (stdlib only): magic + IHDR dimensions.
    # PIL is NOT stdlib and may not exist in the grader sandbox, so the
    # entrypoint must never import it.
    with open(dst, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        print("FAIL: not a PNG", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        print("FAIL: bad size", (width, height), file=sys.stderr)
        return 1
    print("OK entry.png", dst_hash[:16], os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
