import os

import robotics_extraction as rx

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def test_extract_end_to_end_datasheet():
    rec = rx.extract(os.path.join(FIXTURES, "tiny_datasheet.pdf"))
    assert set(rec) == {"entries", "unresolved", "source", "extractor_version"}
    assert rec["extractor_version"] == rx.__version__
    assert rec["entries"][0]["kind"] == "Robot"


def test_extract_end_to_end_layout():
    rec = rx.extract(os.path.join(FIXTURES, "tiny_layout.dxf"))
    assert rec["entries"][0]["kind"] == "Cell"
    assert rec["unresolved"]  # the FENCE line, deliberately unresolved not guessed


def test_extract_unrecognised_file_is_empty_not_an_error():
    rec = rx.extract(os.path.join(FIXTURES, "unrecognised.txt") if os.path.exists(
        os.path.join(FIXTURES, "unrecognised.txt")) else "no_such_file.txt")
    assert rec["entries"] == [] and rec["unresolved"] == []
    assert rec["source"]["file"].endswith(".txt")


def test_extract_is_deterministic():
    a = rx.extract(os.path.join(FIXTURES, "tiny_datasheet.pdf"))
    b = rx.extract(os.path.join(FIXTURES, "tiny_datasheet.pdf"))
    assert a == b
