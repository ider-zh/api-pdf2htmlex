"""Compatibility smoke tests for the Python 3.12 dependency upgrade."""

import base64
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from file_compress import compress_html, compress_png
from run import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_upload = app.config["UPLOAD_FOLDER"]
        app.config["UPLOAD_FOLDER"] = self.temp.name
        self.client = app.test_client()

    def tearDown(self):
        app.config["UPLOAD_FOLDER"] = self.original_upload
        self.temp.cleanup()

    def test_status(self):
        response = self.client.get("/pdf2htmlEX")
        self.assertEqual(response.status_code, 200)
        self.assertIn("document conversions", response.get_data(as_text=True))

    def test_missing_file(self):
        response = self.client.post("/pdf2htmlEX", data={"command": "\"\""})
        self.assertEqual(response.status_code, 404)

    def test_download_filename_with_modern_flask(self):
        with patch("run.pdf2htmlEX", return_value=io.BytesIO(b"fake zip")), patch(
            "run.remove_old_fold"
        ):
            response = self.client.post(
                "/pdf2htmlEX",
                data={"file": (io.BytesIO(b"%PDF-1.7"), "sample.pdf"), "command": '""'},
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("sample.zip", response.headers["Content-Disposition"])
        self.assertEqual(response.data, b"fake zip")


class ImageTests(unittest.TestCase):
    def test_png_to_webp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "sample.png")
            Image.new("RGB", (3, 3), "red").save(path)
            output = compress_png(path)
            self.assertTrue(output.endswith(".webp"))
            self.assertTrue(os.path.isfile(output))

    def test_embedded_image_recompression(self):
        with tempfile.TemporaryDirectory() as directory:
            img = io.BytesIO()
            Image.new("RGB", (3, 3), "blue").save(img, format="PNG")
            data_uri = "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()
            path = os.path.join(directory, "sample.html")
            with open(path, "w", encoding="utf-8") as output:
                output.write('<html><img src="{}"></html>'.format(data_uri))
            compress_html(path)
            with open(path, encoding="utf-8") as source:
                self.assertIn("data:image/webp;base64,", source.read())


if __name__ == "__main__":
    unittest.main()
