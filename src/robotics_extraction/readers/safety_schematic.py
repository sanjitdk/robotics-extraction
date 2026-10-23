#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
safety_schematic.py  (robotics_extraction.readers)
================================================
Safety-circuit symbols (cabinet wiring PDF / EPLAN export) -> SafetyFunction entries,
scoped to safety-relevant tags only (plan §13.3). The category (B/1/2/3/4) must be read
from circuit topology, never guessed (plan §13.2) - this stub has no topology analysis
yet, so every finding stays `unresolved` until P8 builds a real reader against an actual
safety schematic. It never fabricates a category to fill the gap.
"""
from __future__ import annotations

from robotics_extraction.schema import Entry, Source, Unresolved

EXTRACTOR = "safety_schematic"
VERSION = "0.1.0"

#: safety-relevant tags this stub looks for (E-stops, light curtains, safety relays, interlocks)
TAGS = ("e-stop", "estop", "light curtain", "safety relay", "interlock", "safety plc")


def read(path: str) -> tuple[list[Entry], list[Unresolved]]:
    import pdfplumber

    entries: list[Entry] = []
    unresolved: list[Unresolved] = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text() or "").lower()
            found = [t for t in TAGS if t in text]
            if found:
                unresolved.append(Unresolved(
                    reason="safety-relevant tags found but circuit topology is not analysed - "
                           "category (B/1/2/3/4) must not be guessed",
                    source=Source(file=path, page=pno), raw={"tags_found": found}))
    return entries, unresolved
