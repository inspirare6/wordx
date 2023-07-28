from wordx.utils.tree import Tree, E
import random


class ResourceMixin:
    def get_resource(self, res_path):
        return self[f'word/{res_path}']

    def add_resource(res_path, res_bytes):
        self[f'word/{res_path}'] = res_bytes

    def get_document(self):
        return self[f'word/document.xml']

    def save_resource(self, res_path, file_path):
        with open(file_path, 'wb') as f:
            res_bytes = self.get_resource(res_path)
            f.write(res_bytes)


class RelationMixin:
    def get_relations(self, xml_file):
        return self[f'word/_rels/{xml_file}.rels']

    def add_relations(self, xml_file, relations):
        self[f'word/_rels/{xml_file}.rels'] = relations

    def merge_relations(self, relations_a, relations_b):
        relation_tree = etree.fromstring(relations_a)
        for relation in relations_b:
            relation_element = E.Relationship(
                Id=relation['id'], 
                Type=relation['type'], 
                Target=relation['target'])
            relation_tree.append(relation_element)
        return etree.tostring(relation_tree)

    def add_relation(self, xml_file, relation_type, relation_target, relation_id = None):
        relations = self.get_relations(xml_file)
        if not relations:
            relations = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>"""
        relation_tree = Tree(relations)
        relation_id = random.randint(1000,9999) if not relation_id else relation_id
        relation_type = f"http://schemas.openxmlformats.org/officeDocument/2006/relationships/{relation_type}"
        relation_tree +=  E.Relationship(Id=f'rId{relation_id}', Type=relation_type, Target=relation_target)
        self.add_relations(xml_file, bytes(relation_tree))
        return relation_id

    def add_footer_relation(self):
        footer_relation_id = random.randint(1000,9999)
        footer_file = f'footer{footer_relation_id}.xml'
        self.add_relation('document.xml', 'footer', footer_file, footer_relation_id)
        return f'rId{footer_relation_id}', footer_file

    def add_header_relation(self):
        header_relation_id = random.randint(1000,9999)
        header_file = f'header{header_relation_id}.xml'
        self.add_relation('document.xml', 'header', header_file, header_relation_id)
        return f'rId{header_relation_id}', header_file
