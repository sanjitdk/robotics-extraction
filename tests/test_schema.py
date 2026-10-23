import pytest
from pydantic import ValidationError

from robotics_extraction.schema import Entry, ExtractionRecord, Source, Unresolved


def test_entry_requires_kind_and_source():
    e = Entry(id="robot:r1", kind="Robot", fields={"reach_mm": 1800.0}, unit={"reach_mm": "mm"},
               confidence=0.9, source=Source(file="a.pdf", page=1), extractor="datasheet", version="0.1.0")
    assert e.kind == "Robot" and e.source.file == "a.pdf"
    with pytest.raises(ValidationError):
        Entry(id="x", fields={}, source=Source(file="a.pdf"), extractor="x", version="1")  # missing kind


def test_extraction_record_round_trip():
    rec = ExtractionRecord(
        entries=[Entry(id="e1", kind="Robot", fields={}, source=Source(file="a.pdf"), extractor="datasheet", version="0.1.0")],
        unresolved=[Unresolved(reason="low confidence", source=Source(file="a.pdf"))],
        source=Source(file="a.pdf"), extractor_version="0.1.0")
    d = rec.model_dump(mode="json")
    assert set(d) == {"entries", "unresolved", "source", "extractor_version"}
    assert d["entries"][0]["kind"] == "Robot" and d["unresolved"][0]["reason"] == "low confidence"
