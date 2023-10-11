from wordx.utils.fake_zip import FakeZip
from wordx.utils.tree import Tree, E
from wordx.mixins import RelationMixin
from io import BytesIO
import random


class WordFile(RelationMixin, FakeZip):
    '''Word文档对象'''
    def __init__(self, file_path):
        super().__init__(file_path)

    def add_xml(self, xml_type, xml_content):
        '''添加xml文件
        sheet.add_xml('footer', '123')'''
        xml_relation_id = random.randint(1000,9999)
        xml_filename = f'{xml_type}{xml_relation_id}.xml'
        self.register_xml({'path': f'/word/{xml_filename}','type': xml_type})
        self[f'word/{xml_filename}'] = xml_content
        self.append_relation('document.xml', xml_type, xml_filename, xml_relation_id)
        return f'rId{xml_relation_id}'

    def register_xml(self, xml_data):
        '''注册xml类型'''
        xml_path = xml_data['path']
        xml_type = xml_data['type']
        content_type_tree = Tree(self['[Content_Types].xml'])
        content_type = f'application/vnd.openxmlformats-officedocument.wordprocessingml.{xml_type}+xml'
        content_type_tree += E.Override(PartName = xml_path, ContentType = content_type)
        self['[Content_Types].xml'] = bytes(content_type_tree)
        return self

    def mask_relations(self, xml_file):
        relations = self.get_relations(xml_file)
        relation_tree = Tree(relations)
        tmp = []
        for relation_element in relation_tree:
            relation_id_str = relation_element.attrib['Id']
            relation_type = relation_element.attrib['Type']
            relation_target = relation_element.attrib['Target']
            if relation_type in ['endnotes', 'theme', 'setting', 'styles', 'fontTable', 'footnotes', 'webSettings']:
                continue
            rand_int = random.randint(1000, 9999)
            extension = relation_target.split('.')[-1]
            if '/' in relation_target:
                folder = relation_target.split('/')[0]
                relation_target_ = f'{folder}/{rand_int}.{extension}'
            else:
                relation_target_ = f'{rand_int}.{extension}'
            tmp.append({
                'id': relation_id_str,
                'type': relation_type,
                'target': relation_target,
                'id_': f'rId{rand_int}',
                'target_': relation_target_,
            })
        return tmp

    def merge(self, wf):
        # 合并文件
        wf_relations = wf.mask_relations('document.xml')
        for wf_relation in wf_relations:
            filename = 'word/' + wf_relation['target']
            content = wf[filename]
            filename_ = 'word/' + wf_relation['target_']
            self[filename_] = content
        # 合并映射
        document_relations = self.get_relations('document.xml')
        document_relations_ = self.merge_relations(document_relations, wf_relations)
        self.save_relations('document.xml', document_relations_)
        document = self.get_document().decode()
        for relation in wf_relations:
            relation_id = relation['id']
            relation_id_ = relation['id_']
            document = document.replace(relation_id, relation_id_)
        document1 = document.encode()
        document2 = wf.get_document()
        etree1 = etree.fromstring(document1)
        etree2 = etree.fromstring(document2)
        etree1_body = etree1[0]
        etree2_body = etree2[0]
        sect_pr = etree1_body[-1]
        etree1_body.remove(sect_pr)
        for element in etree2_body:
            etree1_body.append(element)
        self['word/document.xml'] = etree.tostring(etree1).decode()
       	self.save('merge.docx')
