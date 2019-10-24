#!/usr/bin/env python
"""Demonsrates attaching files to the Testplan report."""
import os
import sys
import tempfile

import testplan
from testplan.testing import multitest

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("""\
This example requires the Pillow library, which is not automatically
installed as a part of testplan.

To install it run: `pip install Pillow`

For more information about Pillow see: https://pillow.readthedocs.io/en/stable/
""")


@multitest.testsuite
class TestSuite(object):
    """Example test suite."""

    def __init__(self):
        """
        For example purposes, write out a temporary file to attach to the
        report. Realistically you would likely want to attach a file
        generated by the application you are testing.
        """
        with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False) as tmpfile:
            tmpfile.write("testplan\n" * 100)
        self.tmpfile = tmpfile.name

    @multitest.testcase
    def test_attach(self, env, result):
        """Attaches a file to the report."""
        result.attach(self.tmpfile, description="Attaching a text file")

    @multitest.testcase
    def test_attach_again(self, env, result):
        """
        Attach the same file to the report again. This is allowed, only
        one copy of the file will be made under the attachments dir.
        """
        result.attach(self.tmpfile,
                      description="Attaching the same text file again")

    @multitest.testcase
    def test_attach_img(self, env, result):
        """
        Attach an image instead of a plain text file. We draw an image and
        save it as a .png using the Pillow library.
        """
        canvas = (400, 300)

        # Rectangles (width, height, left position, top position)
        frames = [(50, 50, 5, 5), (60, 60, 100, 50), (100, 100, 205, 120)]

        # Init canvas
        im = Image.new('RGBA', canvas, (255, 255, 255, 255))
        draw = ImageDraw.Draw(im)

        # Draw rectangles
        for frame in frames:
            x1, y1 = frame[2], frame[3]
            x2, y2 = frame[2] + frame[0], frame[3] + frame[1]
            draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, 255))

        # Save image
        img_path = os.path.join(env.runpath, "image.png")
        im.save(img_path)

        # Attach to report.
        result.attach(img_path, description="I drew some rectangles")


@testplan.test_plan(name="AttachmentPlan")
def main(plan):
    """Define a Testplan with a single MultiTest."""
    plan.add(multitest.MultiTest(
        name="TestAttachments",
        suites=[TestSuite()]))


if __name__ == "__main__":
    res = main()
    sys.exit(res.exit_code)

