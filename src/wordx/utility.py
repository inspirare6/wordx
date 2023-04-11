from lxml import etree
from lxml.builder import E
import random


class ResourceUtility:
    def get_resource(self, res_path):
        return self.get(f'word/{res_path}')

    def get_resource_as_str(self, res_path):
        return self.get_resource(res_path).decode()

    def add_resource(res_path, file_bytes):
        self.add(f'word/{res_path}', file_bytes)

    def add_media(self, filename, file_bytes):
        self.add_resource(f'media/{filename}', file_bytes)

    def get_document(self):
        return self.get_resource('document.xml')

    def extract_resource(self, res_path, file_path):
        data = self.get_resource(res_path)
        with open(file_path, 'wb') as f:
            f.write(data)


class RelationUtility:
    def get_relations(self, xml_file):
        return self.get(f'word/_rels/{xml_file}.rels') 

    def get_document_relations(self):
        return self.get_relations('document.xml')

    def save_relations(self, xml_file, relations):
        relations_path = f'word/_rels/{xml_file}.rels'
        self.replace(relations_path, relations)

    def merge_relations(self, relations_a, relations_b):
        relation_tree = etree.fromstring(relations_a)
        for relation in relations_b:
            relation_id = relation['id']
            relation_type = relation['type']
            relation_target = relation['target']
            relation_element = E.Relationship(Id=relation_id, Type=relation_type, Target=relation_target)
            relation_tree.append(relation_element)
        return etree.tostring(relation_tree)

    def add_relation(self, xml_file, relation_type, relation_target, relation_id = None):
        relations = self.get_relations(xml_file)
        if relations:
            relation_tree = etree.fromstring(relations)
        else:
            template = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>"""
            relation_tree = etree.fromstring(template)
        relation_id = random.randint(1000,9999) if not relation_id else relation_id
        relation_type = f"http://schemas.openxmlformats.org/officeDocument/2006/relationships/{relation_type}"
        relation_element =  E.Relationship(Id=f'rId{relation_id}', Type=relation_type, Target=relation_target)
        relation_tree.append(relation_element)
        relations = etree.tostring(relation_tree)
        self.save_relations(xml_file, relations)
        return relation_id

    def add_footer_relation(self):
        footer_relation_id = random.randint(1000,9999)
        footer_file = f'footer{footer_relation_id}.xml'
        self.add_relation('document.xml', 'footer', footer_file, footer_relation_id)
        return footer_relation_id, footer_file

    def add_header_relation(self):
        header_relation_id = random.randint(1000,9999)
        header_file = f'header{header_relation_id}.xml'
        self.add_relation('document.xml', 'header', header_file, header_relation_id)
        return header_relation_id, header_file
