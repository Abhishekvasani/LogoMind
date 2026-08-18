#!/usr/bin/env python3
"""Sync 05_RS_LICs into backend/05_RS_LICs (serverless bundle copy).

Run after editing any LIC volume:  python scripts/sync_backend_lics.py
"""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "05_RS_LICs"
dst = root / "backend" / "05_RS_LICs"
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print(f"synced {len(list(dst.glob(chr(42)+chr(46)+chr(109)+chr(100))))} files")
