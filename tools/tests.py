from django.test import TestCase

# Create your tests here.
from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from tools.utils.hash_utils import calculate_file_hash

class FileHashUtilTest(SimpleTestCase):

    def test_sha256_hash(self):
        content = b"hello world"
        uploaded_file = SimpleUploadedFile(
            "test.txt",
            content,
            content_type="text/plain"
        )

        result = calculate_file_hash(uploaded_file, "sha256")

        self.assertEqual(
            result,
            "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        )
    def test_invalid_algorithm_raises_error(self):
        content = b"hello"
        uploaded_file = SimpleUploadedFile(
            "test.txt",
            content,
            content_type="text/plain"
        )

        with self.assertRaises(ValueError):
            calculate_file_hash(uploaded_file, "invalid_algo")

    def test_empty_file_hash(self):
        content = b""
        uploaded_file = SimpleUploadedFile(
            "empty.txt",
            content,
            content_type="text/plain"
        )

        result = calculate_file_hash(uploaded_file, "sha256")

        self.assertEqual(
            result,
            "e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855"
        )

    def test_sha1_hash(self):
        content = b"hello world"
        uploaded_file = SimpleUploadedFile(
            "test.txt",
            content,
            content_type="text/plain"
        )

        result = calculate_file_hash(uploaded_file, "sha1")

        self.assertEqual(
            result,
            "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
        )
