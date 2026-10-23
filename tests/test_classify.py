from robotics_extraction.classify import classify


def test_classify_by_extension():
    assert classify("layout.dxf") == "layout"
    assert classify("layout.DWG") == "layout"
    assert classify("io.csv") == "io_list"
    assert classify("io.xlsx") == "io_list"


def test_classify_pdf_by_filename_hint():
    assert classify("robot_r2000a_datasheet.pdf") == "datasheet"
    assert classify("cell_safety_schematic.pdf") == "safety_schematic"
    assert classify("gripper_eoat.pdf") == "eoat"
    assert classify("some_eplan_export.pdf") == "safety_schematic"


def test_classify_unrecognised():
    assert classify("random_notes.txt") is None
    assert classify("plain.pdf") is None
