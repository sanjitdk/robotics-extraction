#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schema.py  (robotics_extraction)
=============================
The one JSON shape every reader produces and the only thing that crosses the
`robotics-sme` repo boundary (plan §13.4-13.5): `{entries, unresolved, source,
extractor_version}`. No LLM, no project, no network - `extract(path)` is a pure
function, file in, JSON out.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Source(BaseModel):
    file: str
    page: int | None = None
    locator: str | None = None


class Entry(BaseModel):
    """One extracted fact. `confidence` below the caller's threshold belongs in
    `unresolved`, never silently written as fact."""
    id: str
    kind: str  # "Robot" | "Cell" | "SafetyDevice" | "EndEffector" | "SafetyFunction" | "Controller" | "Part" | "Process"
    fields: dict[str, Any] = Field(default_factory=dict)
    unit: dict[str, str] = Field(default_factory=dict)  # per numeric field, when it has one
    confidence: float = 1.0
    source: Source
    extractor: str
    version: str


class Unresolved(BaseModel):
    """Something the reader saw but would not turn into a fact (missing column, no
    position, a category that must come from circuit topology, not a guess)."""
    reason: str
    source: Source
    raw: dict[str, Any] = Field(default_factory=dict)


class ExtractionRecord(BaseModel):
    entries: list[Entry] = Field(default_factory=list)
    unresolved: list[Unresolved] = Field(default_factory=list)
    source: Source
    extractor_version: str
