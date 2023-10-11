from wordx.utils.tree import Tree, E
import random


class RelationMixin:
    def get_relations(self, xml_file):
        '''获取指定xml文件的资源映射
        wf.get_relations('document.xml')
        '''
        return self[f'word/_rels/{xml_file}.rels']

    def write_relations(self, xml_file, relations):
        '''写入指定xml文件的资源映射
        '''
        self[f'word/_rels/{xml_file}.rels'] = relations

    def append_relation(self, xml_file, relation_type, relation_target, relation_id = None):
        '''添加单条资源映射
        sheet.append_relation('document.xml', 'footer', 'footer111.xml', 123)
        '''
        relations = self.get_relations(xml_file)
        if not relations:
            relations = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>"""
        relation_tree = Tree(relations)
        relation_id = random.randint(1000,9999) if not relation_id else relation_id
        relation_type = f"http://schemas.openxmlformats.org/officeDocument/2006/relationships/{relation_type}"
        relation_tree +=  E.Relationship(Id=f'rId{relation_id}', Type=relation_type, Target=relation_target)
        self.write_relations(xml_file, bytes(relation_tree))
        return f'rId{relation_id}'

    def merge_relations(self, relations_a, relations_b):
        '''合并资源映射'''
        relation_tree = etree.fromstring(relations_a)
        for relation in relations_b:
            relation_element = E.Relationship(
                Id=relation['id'], 
                Type=relation['type'], 
                Target=relation['target'])
            relation_tree.append(relation_element)
        return etree.tostring(relation_tree)



