#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eoat.py  (robotics_extraction.readers)
====================================
Gripper/EOAT drawing or datasheet -> EndEffector entries, by the same table-extraction
approach as `datasheet.py` (plan §13.2/§13.3). Correct in shape, not tuned (P8).
"""
from __future__ import annotations

from robotics_extraction.schema import Entry, Source, Unresolved

EXTRACTOR = "eoat"
VERSION = "0.1.0"

FIELD_MAP = {
    "type": ("type", None),
    "mass": ("mass_kg", "kg"), "mass_kg": ("mass_kg", "kg"),
    "grip_force": ("grip_force_n", "N"), "grip_force_n": ("grip_force_n", "N"),
    "actuation_time": ("actuation_time_s", "s"), "actuation_time_s": ("actuation_time_s", "s"),
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
                        if field == "type":
                            fields[field] = str(cell).strip()
                            continue
                        try:
                            fields[field] = float(str(cell).replace(",", ""))
                        except ValueError:
                            continue
                        if unit:
                            units[field] = unit
                    if not fields:
                        unresolved.append(Unresolved(reason="no recognised EOAT column in this row",
                                                      source=Source(file=path, page=pno), raw={"row": row}))
                        continue
                    entries.append(Entry(id=f"eoat:{pno}:{len(entries)}", kind="EndEffector", fields=fields, unit=units,
                                          confidence=0.5, source=Source(file=path, page=pno, locator="table"),
                                          extractor=EXTRACTOR, version=VERSION))
    return entries, unresolved
