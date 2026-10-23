import os

from robotics_extraction.readers import datasheet, layout

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def test_datasheet_reader_on_fixture():
    entries, unresolved = datasheet.read(os.path.join(FIXTURES, "tiny_datasheet.pdf"))
    assert len(entries) == 1 and unresolved == []
    e = entries[0]
    assert e.kind == "Robot" and e.fields["model"] == "R-2000A"
    assert e.fields["reach_mm"] == 1800.0 and e.unit["reach_mm"] == "mm"
    assert e.fields["payload_kg"] == 165.0 and e.fields["mass_kg"] == 280.0
    assert e.source.file.endswith("tiny_datasheet.pdf") and e.source.page == 1
    assert e.confidence < 1.0  # correct in shape, not tuned - never claims full confidence


def test_layout_reader_on_fixture():
    entries, unresolved = layout.read(os.path.join(FIXTURES, "tiny_layout.dxf"))
    assert len(entries) == 1
    e = entries[0]
    assert e.kind == "Cell" and e.fields["layer"] == "ROBOT"
    assert e.fields["x_mm"] == 1200.0 and e.fields["y_mm"] == 800.0
    # the FENCE line has no INSERT/location/center position this stub reader understands -
    # it goes to unresolved, never a guessed position
    assert len(unresolved) == 1 and "FENCE" in unresolved[0].raw["layer"]
