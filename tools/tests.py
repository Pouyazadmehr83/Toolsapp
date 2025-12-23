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
