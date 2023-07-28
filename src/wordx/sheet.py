from wordx.word_file import WordFile
from jinja2 import Template


class Sheet(WordFile):
    """Word表单对象"""
    def __init__(self, tpl_path):
        super().__init__(tpl_path)

    @staticmethod
    def render_template(tpl, data):
        lib = {
            'enumerate': enumerate,
            'len': len,
            'isinstance': isinstance,
            'tuple': tuple,
            'list': list
        }
        return Template(tpl).render(**data, **lib)

    def render_header(self, data):
        """页眉渲染"""
        header_tpl = self['word/header.xml'].decode()
        self['word/header.xml'] = self.render_template(header_tpl, data).encode()

    def render_footer(self, data):
        """页脚渲染""" 
        footer_tpl = self['word/footer.xml'].decode()
        self['word/footer.xml'] = self.render_template(footer_tpl, data).encode()

    def render_document(self, data):
        """文档渲染"""
        document_tpl = self['word/document.xml'].decode()
        self['word/document.xml'] = self.render_template(document_tpl, data).encode()

    def render_and_add_header(self, data):
        """添加页眉"""
        header_xml_data = self.render_template(self.retrieve(f'word/header.xml'), data)
        return self.add_header(header_xml_data)

    def render_and_add_footer(self, data):
        """添加页脚"""
        footer_xml_data = self.render_template(self.retrieve(f'word/footer.xml'), data)
        return self.add_footer(footer_xml_data)

    def render(self, data):
        self.render_header(data)
        self.render_footer(data)
        self.render_document(data)
        return self