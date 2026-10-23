#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datasheet.py  (robotics_extraction.readers)
=========================================
PDF spec tables -> Robot entries, by table extraction and a declared header map - no
LLM. Correct in shape, not tuned: a real vendor datasheet's table layout may not match
this stub's column names at all (plan §13.6/§13.9); P8 rewrites this against real files.
"""
from __future__ import annotations

from robotics_extraction.schema import Entry, Source, Unresolved

EXTRACTOR = "datasheet"
VERSION = "0.1.0"

#: declared header -> (Robot field, unit); plan §13.2's data dictionary
FIELD_MAP = {
    "model": ("model", None),
    "reach": ("reach_mm", "mm"), "reach_mm": ("reach_mm", "mm"),
    "payload": ("payload_kg", "kg"), "payload_kg": ("payload_kg", "kg"),
    "repeatability": ("repeatability_mm", "mm"), "repeatability_mm": ("repeatability_mm", "mm"),
    "mass": ("mass_kg", "kg"), "mass_kg": ("mass_kg", "kg"),
}


def read(path: str) -> tuple[list[Entry], list[Unresolved]]:
    import pdfplumber

    entries: list[Entry] = []
    unresolved: list[Unresolved] = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables() or []:
                if not table or len(table) < 2:
                    continue
                header = [str(h or "").strip().lower().replace(" ", "_") for h in table[0]]
                for row in table[1:]:
                    fields: dict = {}
                    units: dict = {}
                    for h, cell in zip(header, row):
                        mapped = FIELD_MAP.get(h)
                        if mapped is None or cell in (None, ""):
                            continue
                        field, unit = mapped
                        if field == "model":
                            fields[field] = str(cell).strip()
                            continue
                        try:
                            fields[field] = float(str(cell).replace(",", ""))
                        except ValueError:
                            continue
                        if unit:
                            units[field] = unit
                    if "model" not in fields:
                        unresolved.append(Unresolved(reason="no model column recognised in this row",
                                                      source=Source(file=path, page=pno), raw={"row": row}))
                        continue
                    entries.append(Entry(id=f"robot:{fields['model']}", kind="Robot", fields=fields, unit=units,
                                          confidence=0.6, source=Source(file=path, page=pno, locator="table"),
                                          extractor=EXTRACTOR, version=VERSION))
    return entries, unresolved
