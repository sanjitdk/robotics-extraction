#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layout.py  (robotics_extraction.readers)
======================================
Native DXF/DWG -> Cell / SafetyDevice entries, by layer name and block position - no
LLM. Correct in shape, not tuned: a real cell layout's layer-naming convention may not
match this stub's `ROBOT`/`FENCE`/`LC`/`DOOR` names at all (plan §13.6/§13.9); P8
rewrites this against a real sample.
"""
from __future__ import annotations

from robotics_extraction.schema import Entry, Source, Unresolved

EXTRACTOR = "layout"
VERSION = "0.1.0"

#: layer name -> entry kind (plan §13.3's layer convention: ROBOT, FENCE, LC, DOOR)
LAYER_KIND = {"ROBOT": "Cell", "FENCE": "SafetyDevice", "LC": "SafetyDevice", "DOOR": "SafetyDevice"}


def read(path: str) -> tuple[list[Entry], list[Unresolved]]:
    import ezdxf

    entries: list[Entry] = []
    unresolved: list[Unresolved] = []
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    for i, e in enumerate(msp):
        layer = (e.dxf.layer or "").upper()
        kind = LAYER_KIND.get(layer)
        if kind is None:
            continue
        pos = None
        try:
            if e.dxftype() == "INSERT":
                pos = e.dxf.insert
            elif hasattr(e.dxf, "location"):
                pos = e.dxf.location
            elif hasattr(e.dxf, "center"):
                pos = e.dxf.center
        except Exception:
            pos = None
        if pos is None:
            unresolved.append(Unresolved(reason=f"no position on a {layer} entity ({e.dxftype()})",
                                          source=Source(file=path, locator=f"entity[{i}]"), raw={"layer": layer}))
            continue
        fields = {"layer": layer, "x_mm": float(pos[0]), "y_mm": float(pos[1])}
        entries.append(Entry(id=f"{kind.lower()}:{layer.lower()}:{i}", kind=kind, fields=fields,
                              unit={"x_mm": "mm", "y_mm": "mm"}, confidence=0.6,
                              source=Source(file=path, locator=f"{layer}[{i}]"), extractor=EXTRACTOR, version=VERSION))
    return entries, unresolved
