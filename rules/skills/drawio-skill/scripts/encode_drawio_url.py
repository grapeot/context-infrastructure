#!/usr/bin/env python3
"""Encode a .drawio XML file into a diagrams.net viewer URL.

Used as the browser fallback when the draw.io desktop CLI is unavailable.
Produces a client-side URL — the diagram XML is encoded in the URL
fragment (after `#`), so nothing is uploaded to any server.

Usage: python3 encode_drawio_url.py <path/to/input.drawio>
"""
import base64
import sys
import urllib.parse
import zlib


def encode(xml: str) -> str:
    # Raw deflate (no zlib header) — diagrams.net uses mxGraph's raw inflate
    c = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    compressed = c.compress(xml.encode("utf-8")) + c.flush()
    # Standard base64 (atob rejects url-safe -/_); strip newlines
    encoded = base64.b64encode(compressed).decode("utf-8").replace("\n", "")
    return (
        "https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&edit=_blank#R"
        + urllib.parse.quote(encoded, safe="")
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: encode_drawio_url.py <path>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        print(encode(f.read()))
