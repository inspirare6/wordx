from wordx.fake_zip import FakeZip
from wordx.utility import ResourceUtility, RelationUtility
from lxml import etree
from lxml.builder import E
from io import BytesIO
import random


class WordFile(FakeZip, ResourceUtility, RelationUtility):
    def __init__(self, file_path):
        super().__init__(file_path)

    def add_footer(self, footer):
        footer_relation_id, footer_file = self.add_footer_relation()
        self.add(f'word/{footer_file}', footer)
        self.register_xml({'path': f'/word/{footer_file}','type': 'footer'})
        return footer_relation_id

    def add_header(self, header):
        header_relation_id, header_file = self.add_header_relation()
        self.add(f'word/{header_file}', header)
        self.register_xml({'path': f'/word/{header_file}','type': 'header'})
        return header_relation_id

    def register_xml(self, xml_data):
        xml_path = xml_data['path']
        xml_type = xml_data['type']
        content_type_xml = self.get('[Content_Types].xml')
        content_type_tree = etree.fromstring(content_type_xml)
        content_type = f'application/vnd.openxmlformats-officedocument.wordprocessingml.{xml_type}+xml'
        content_type_new_element = E.Override(PartName = xml_path, ContentType = content_type)
        content_type_tree.append(content_type_new_element)
        content_type_xml = etree.tostring(content_type_tree)
        self.replace('[Content_Types].xml', content_type_xml)
        return self

    def mask_relations(self, xml_file):
        relations = self.get_relations(xml_file)
        relation_tree = etree.fromstring(relations)
        tmp = []
        for relation_element in relation_tree:
            relation_id_str = relation_element.attrib['Id']
            relation_type = relation_element.attrib['Type']
            relation_target = relation_element.attrib['Target']
            pass_types = ['endnotes', 'theme', 'setting', 'styles', 'fontTable', 'footnotes', 'webSettings']
            if any([(pass_type in relation_type) for pass_type in pass_types]):
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
            content = wf.get(filename)
            filename_ = 'word/' + wf_relation['target_']
            self.add(filename_, content)
        # 合并映射
        document_relations = self.get_document_relations()
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
        self.replace('word/document.xml', etree.tostring(etree1).decode())
       	self.save('merge.docx')
