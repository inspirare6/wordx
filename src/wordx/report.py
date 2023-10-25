from wordx.sheet import Sheet
from pathlib import Path
import os 


class Report(Sheet):
    """Word表单对象"""
    def __init__(self, tpl_path, component_folder=None, xml_folder=None):
        super().__init__(tpl_path, xml_folder)
        self.component_folder = component_folder


    def render(self, data):
        template_xml = '($ for item in data $)'
        index = 0
        for root, dirs, filenames in os.walk(self.component_folder):
            for filename in filenames:
                component_type = filename.split('.')[0]
                file = open(Path(root) / filename, 'r', encoding='utf-8')
                component_content = file.read()
                template_xml += f"($ {'if' if index==0 else 'elif'} item['type']=='{component_type}' $){component_content}"
                index += 1
        template_xml += '($ endif $)($ endfor $)'
        document_xml = self.render_xml('document', dict(document=template_xml)).decode()
        syntax_map = {
            r'($': '{%',
            r'$)': '%}',
            r'((': '{{',
            r'))': '}}',
        }
        for k, v in syntax_map.items():
            document_xml = document_xml.replace(k, v)
        self['word/document.xml'] = bytes(document_xml, 'utf-8')
        items = data['data']
        for item in items: 
            if item['type'] == 'image':
                url = item['content']['url']
                self['word/media/1.png'] = open(url, 'rb').read()
                relation_id = self.append_relation('document.xml', 'image', 'media/1.png')
                item['content']['relation_id'] = relation_id
        super().render(data)

