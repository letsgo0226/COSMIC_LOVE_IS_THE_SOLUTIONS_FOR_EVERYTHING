#!/bin/sh
command -v python3 >/dev/null 2>&1 || apk add --no-cache python3 >/dev/null 2>&1
python3 - "$@" <<'PY'
import base64
import json
import sys
import time
import zlib

PROTO = "CLZeroPack-Core/iSH/1.0_NO_SHA"
MOD = 1000000007


def read_bytes(path):
    if path in ("", "-"):
        return sys.stdin.buffer.read()
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path, data):
    if path:
        with open(path, "wb") as f:
            f.write(data)
    else:
        sys.stdout.buffer.write(data)


def write_text(path, text):
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


def g_alg(zbytes):
    return sum((i + 1) * b for i, b in enumerate(zbytes)) % MOD


def pack(src, dst):
    raw = read_bytes(src)
    zbytes = zlib.compress(raw, 9)
    payload = base64.b64encode(zbytes).decode("ascii")
    g = g_alg(zbytes)
    out = {
        "P": PROTO,
        "A": "CL",
        "Z": "zlib9+b64",
        "G": g,
        "r": "1/2+i*log(1+%d)" % g,
        "n": len(raw),
        "zn": len(zbytes),
        "H": 0 if zlib.decompress(base64.b64decode(payload)) == raw else 1,
        "B": payload,
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    write_text(dst, json.dumps(out, ensure_ascii=False, separators=(",", ":")))


def unpack(src, dst):
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    payload = data.get("B", data.get("Payload", ""))
    raw = zlib.decompress(base64.b64decode(payload))
    write_bytes(dst, raw)


mode = sys.argv[1] if len(sys.argv) > 1 else "pack"
src = sys.argv[2] if len(sys.argv) > 2 else "-"
dst = sys.argv[3] if len(sys.argv) > 3 else ""

if mode in ("u", "unpack", "decode"):
    unpack(src, dst)
else:
    pack(src, dst)
PY
