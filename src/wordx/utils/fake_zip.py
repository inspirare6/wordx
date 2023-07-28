from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO


class FakeZip(object):
    """伪Zip对象，只作文件内容存储
    解决Zip无法直接替换文件问题
    """
    def __init__(self, file_path):
        self._dict = {}
        if isinstance(file_path, bytes):
            zip = ZipFile(BytesIO(file_path), 'r')
        else:
            zip = ZipFile(file_path)
        for fileinfo in zip.infolist():
            file_data = zip.open(fileinfo).read()
            self._dict[fileinfo.filename] = file_data

    def __getitem__(self, filename):
        return self._dict.get(filename)

    def __setitem__(self, filename, content):
        self._dict[filename] = content  

    def __bytes__(self):
        with BytesIO() as f:
            self.write(f)
            return f.getvalue()

    def write(self, f):
        """写入到文件"""
        with ZipFile(f, mode='w', compression=ZIP_DEFLATED) as zf:
            for k, v in self._dict.items():
                zf.writestr(k, v)

    def save(self, path):
        """保存为文件"""
        with open(path, 'wb') as f:
            self.write(f)


