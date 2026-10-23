"""One-off generator for the hand-built synthetic fixtures (plan §13.6). Not a test;
not shipped as part of the package. Re-run after editing to regenerate the fixture
files in this directory."""
from __future__ import annotations

import os

HERE = os.path.dirname(__file__)


def make_layout_dxf():
    import ezdxf

    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    doc.layers.add("ROBOT")
    doc.layers.add("FENCE")
    block = doc.blocks.new(name="ROBOT_BASE")
    block.add_circle((0, 0), radius=50)
    msp.add_blockref("ROBOT_BASE", (1200.0, 800.0), dxfattribs={"layer": "ROBOT"})
    msp.add_line((0, 0), (3000, 0), dxfattribs={"layer": "FENCE"})
    doc.saveas(os.path.join(HERE, "tiny_layout.dxf"))


def make_datasheet_pdf():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table, TableStyle

    path = os.path.join(HERE, "tiny_datasheet.pdf")
    c = canvas.Canvas(path, pagesize=letter)
    data = [["model", "reach_mm", "payload_kg", "mass_kg"], ["R-2000A", "1800", "165", "280"]]
    t = Table(data)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.75, colors.black)]))  # pdfplumber's default
    t.wrapOn(c, 400, 200)                                                    # "lines" strategy needs
    t.drawOn(c, 72, 600)                                                     # visible borders
    c.save()


if __name__ == "__main__":
    make_layout_dxf()
    make_datasheet_pdf()
    print("wrote tiny_layout.dxf, tiny_datasheet.pdf")
