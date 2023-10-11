from wordx.word_file import WordFile
from jinja2 import Template
from pathlib import Path


class Sheet(WordFile):
    """Word表单对象"""
    def __init__(self, tpl_path, xml_folder=None):
        super().__init__(tpl_path)
        self.xml_folder = xml_folder

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

    def render_xml(self, xml_filename, data):
        try: 
            if self.xml_folder:
                xml_path = Path(self.xml_folder) / f'{xml_filename}.xml'
                xml_template = open(xml_path, 'r', encoding='utf-8').read()
            else:
                xml_template = self[f'word/{xml_filename}.xml'].decode()
            xml_string = self.render_template(xml_template, data).encode()
            self[f'word/{xml_filename}.xml'] = xml_string
            return xml_string
        except Exception as e:
            print(e)
            raise e

    def render_and_add_xml(self, xml_type, data):
        xml_content = self.render_template(self.retrieve(f'word/{xml_type}.xml'), data)
        return self.add_xml(xml_type, xml_content)

    def render(self, data):
        self.render_xml('header', data)
        self.render_xml('footer', data)
        self.render_xml('document', data)
        return self