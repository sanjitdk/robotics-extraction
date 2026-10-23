#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
io_list.py  (robotics_extraction.readers)
=======================================
I/O list / simulation export (CSV/XLSX) -> Controller entries, by a strict declared
column mapping - no inference of what a column might mean (plan §13.3). Correct in
shape, not tuned (P8).
"""
from __future__ import annotations

import math

from robotics_extraction.schema import Entry, Source, Unresolved

EXTRACTOR = "io_list"
VERSION = "0.1.0"

REQUIRED_COLUMNS = ("signal", "type")


def read(path: str) -> tuple[list[Entry], list[Unresolved]]:
    import pandas as pd

    entries: list[Entry] = []
    unresolved: list[Unresolved] = []
    df = pd.read_excel(path) if path.lower().endswith((".xlsx", ".xls")) else pd.read_csv(path)
    cols = {str(c).strip().lower(): c for c in df.columns}
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    if missing:
        unresolved.append(Unresolved(reason=f"missing required column(s): {', '.join(missing)}",
                                      source=Source(file=path), raw={"columns": [str(c) for c in df.columns]}))
        return entries, unresolved
    for i, row in df.iterrows():
        signal = row.get(cols["signal"])
        if signal is None or (isinstance(signal, float) and math.isnan(signal)):
            continue
        fields: dict = {"signal": str(signal).strip()}
        kind = row.get(cols["type"])
        if kind is not None and not (isinstance(kind, float) and math.isnan(kind)):
            fields["type"] = str(kind).strip()
        if "protocol" in cols:
            proto = row.get(cols["protocol"])
            if proto is not None and not (isinstance(proto, float) and math.isnan(proto)):
                fields["protocol"] = str(proto).strip()
        entries.append(Entry(id=f"controller_signal:{fields['signal']}", kind="Controller", fields=fields, unit={},
                              confidence=0.7, source=Source(file=path, locator=f"row[{i}]"),
                              extractor=EXTRACTOR, version=VERSION))
    return entries, unresolved
