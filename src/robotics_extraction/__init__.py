#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
robotics_extraction
====================
Deterministic, rule-based extraction of robotics engineering facts from drawings,
datasheets, schematics and I/O lists. No LLM, no project, no network - `extract(path)`
is a pure function, file in, JSON out (plan §13.4-§13.5): the ONLY thing that crosses
the `robotics-sme` repo boundary.
"""
from __future__ import annotations

import importlib

from robotics_extraction.classify import classify
from robotics_extraction.schema import Entry, ExtractionRecord, Source, Unresolved

__version__ = "0.1.0"

READERS = {
    "datasheet": "robotics_extraction.readers.datasheet",
    "layout": "robotics_extraction.readers.layout",
    "eoat": "robotics_extraction.readers.eoat",
    "safety_schematic": "robotics_extraction.readers.safety_schematic",
    "io_list": "robotics_extraction.readers.io_list",
}


def extract(path: str) -> dict:
    """file in -> `{entries, unresolved, source, extractor_version}` JSON out.
    An unrecognised file (plan §13.3) returns an empty, valid record, not an error -
    the caller's generic parser handles it."""
    kind = classify(path)
    if kind is None:
        return ExtractionRecord(entries=[], unresolved=[], source=Source(file=path),
                                 extractor_version=__version__).model_dump(mode="json")
    reader = importlib.import_module(READERS[kind])
    entries, unresolved = reader.read(path)
    return ExtractionRecord(entries=entries, unresolved=unresolved, source=Source(file=path),
                             extractor_version=__version__).model_dump(mode="json")
