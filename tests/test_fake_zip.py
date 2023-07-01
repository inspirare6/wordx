import pytest
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

from ..src.fake_zip import FakeZip


class TestFakeZip:
    @pytest.fixture
    def fake_zip(self):
        zip_data = BytesIO()
        with ZipFile(zip_data, mode='w', compression=ZIP_DEFLATED) as zf:
            zf.writestr('file1.txt', 'content1')
            zf.writestr('file2.txt', 'content2')
        zip_data.seek(0)
        return FakeZip(zip_data)

    def test_get_existing_file(self, fake_zip):
        content = fake_zip.get('file1.txt')
        assert content == b'content1'

    def test_get_non_existing_file(self, fake_zip):
        content = fake_zip.get('file3.txt')
        assert content is None

    def test_replace_existing_file(self, fake_zip):
        fake_zip.replace('file1.txt', 'new_content')
        content = fake_zip.get('file1.txt')
        assert content == b'new_content'

    def test_replace_non_existing_file(self, fake_zip):
        fake_zip.replace('file3.txt', 'new_content')
        content = fake_zip.get('file3.txt')
        assert content == b'new_content'

    def test_add_new_file(self, fake_zip):
        fake_zip.add('file3.txt', 'new_content')
        content = fake_zip.get('file3.txt')
        assert content == b'new_content'

    def test_save_zip_file(self, fake_zip, tmp_path):
        file_path = tmp_path / 'test.zip'
        fake_zip.save(file_path)
        assert file_path.exists()

    def test_bytes_conversion(self, fake_zip):
        zip_data = bytes(fake_zip)
        assert isinstance(zip_data, bytes)
        assert len(zip_data) > 0