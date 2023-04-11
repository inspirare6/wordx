from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO


class FakeZip(object):
    """伪Zip对象，只作文件内容存储
    解决Zip无法直接替换文件问题
    """
    def __init__(self, file_path):
        self.dict = {}
        if isinstance(file_path, bytes):
            zip = ZipFile(BytesIO(file_path), 'r')
        else:
            zip = ZipFile(file_path)
        for fileinfo in zip.infolist():
            file_data = zip.open(fileinfo).read()
            self.dict[fileinfo.filename] = file_data


    def get(self, filename):
        """获取文件内容
        fz.get('haha.txt')
        """
        if filename in self.dict:
            return self.dict[filename]
        else:
            return None

    def replace(self, filename, content):
        """替换文件内容
        fz.replace('haha.txt', '567')
        """
        self.dict[filename] = content
        return self

    def add(self, filename, content):
        """添加文件
        fz.add('haha.txt', 'haha')"""
        self.dict[filename] = content
        return self

    def save(self, path):
        with open(path, 'wb') as f:
            with ZipFile(f, mode='w', compression=ZIP_DEFLATED) as zf:
                for k, v in self.dict.items():
                    zf.writestr(k, v)

    def __bytes__(self):
        with BytesIO() as f:
            with ZipFile(f, mode='w', compression=ZIP_DEFLATED) as zf:
                for k, v in self.dict.items():
                    zf.writestr(k, v)
            return f.getvalue()

