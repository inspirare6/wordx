from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO


class FakeZip(object):
    """伪Zip对象，只作文件内容存储
    解决Zip无法直接替换文件问题
    """
    def __init__(self, file_path):
        self.__dict = {}
        if isinstance(file_path, bytes):
            zip = ZipFile(BytesIO(file_path), 'r')
        else:
            zip = ZipFile(file_path)
        for fileinfo in zip.infolist():
            file_data = zip.open(fileinfo).read()
            self.__dict[fileinfo.filename] = file_data

    def __getitem__(self, filename):
        return self.__dict.get(filename)

    def __setitem__(self, filename, content):
        self.__dict[filename] = content

    def retrieve(self, filename):
        data = self[filename]
        return data.decode() if data else ''

    def save(self, path):
        with open(path, 'wb') as f:
            with ZipFile(f, mode='w', compression=ZIP_DEFLATED) as zf:
                for k, v in self.__dict.items():
                    zf.writestr(k, v)

    def __bytes__(self):
        with BytesIO() as f:
            with ZipFile(f, mode='w', compression=ZIP_DEFLATED) as zf:
                for k, v in self.__dict.items():
                    zf.writestr(k, v)
            return f.getvalue()








        # empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        # b = BytesIO()
        # b.write(empty_zip_data)
        # with ZipFile(b, 'w') as z:
        #     for k, v in self.__dict.items():
        #         z.writestr(k, v)
        #     b.write(b'PK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\xdf\xa4\xd2l \x05\x00\x00 \x05\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x00\x00\x00\x00[Content_Types].xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\x1e\x91\x1a\xb7N\x02\x00\x00N\x02\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01Q\x05\x00\x00_rels/.relsPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7TZ\xfa(K\xa2\x0b\x00\x00\xa2\x0b\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\xc8\x07\x00\x00word/document.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\xd6d\xb3Q1\x03\x00\x001\x03\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x99\x13\x00\x00word/_rels/document.xml.relsPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7Tj\xb3\xc9\x99\x94\x1a\x00\x00\x94\x1a\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x04\x17\x00\x00word/theme/theme1.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T`\xfd\x067?\r\x00\x00?\r\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\xcb1\x00\x00word/settings.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7TJ\xf6\'\xbb\x16s\x00\x00\x16s\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x019?\x00\x00word/styles.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\xef\n)N~\x03\x00\x00~\x03\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01|\xb2\x00\x00word/webSettings.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\xa3!M&\x93\x06\x00\x00\x93\x06\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01,\xb6\x00\x00word/fontTable.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7T\r\xfa\xca\xe0\xe7\x02\x00\x00\xe7\x02\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\xef\xbc\x00\x00docProps/core.xmlPK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x00\xc1z\xd7TcM[\x12\xc5\x02\x00\x00\xc5\x02\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x05\xc0\x00\x00docProps/app.xmlPK\x05\x06\x00\x00\x00\x00\x0b\x00\x0b\x00\xc1\x02\x00\x00\xf8\xc2\x00\x00\x00\x00')
        #     return b.getvalue()
