#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify.py  (robotics_extraction)
================================
Which reader a file routes to - extension plus filename signature only, before any
reader runs. No LLM, no structural guessing at this stage either (plan §13.3). `None`
means "not recognised"; the caller's generic parser handles it (stays `stated` at best,
never substitutes for a `measured` value a tool needs).
"""
from __future__ import annotations

import os

READER_KINDS = ("datasheet", "layout", "eoat", "safety_schematic", "io_list")

_PDF_NAME_HINTS = (
    ("eoat", "eoat"), ("gripper", "eoat"), ("end_effector", "eoat"), ("end-effector", "eoat"),
    ("safety", "safety_schematic"), ("schematic", "safety_schematic"), ("eplan", "safety_schematic"),
    ("datasheet", "datasheet"), ("spec", "datasheet"),
)


def classify(path: str) -> str | None:
    ext = os.path.splitext(path)[1].lower()
    name = os.path.basename(path).lower()
    if ext in (".dxf", ".dwg"):
        return "layout"
    if ext in (".csv", ".xlsx", ".xls"):
        return "io_list"
    if ext == ".pdf":
        for hint, kind in _PDF_NAME_HINTS:
            if hint in name:
                return kind
    return None
