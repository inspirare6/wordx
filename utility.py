from wordx.word_file import WordFile 
from wordx.sheet import Sheet
import os
import json
import time
import sys


class SuperWordFile(WordFile):
    testing_word = ''  
    testing_xml = ''  

    def __init__(self, folder, file):
        path = os.path.join(folder, file)
        super().__init__(path)
        self.folder = folder

    @staticmethod
    def timestamp():
        return str(int(time.time()))

    def super_replace(self, file):
        path = os.path.join(self.folder, file)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                file_bytes = f.read()
                self[f'word/{file}'] = file_bytes

    def super_save(self, file):
        path = os.path.join(self.folder, file)
        self.save(path)

    def generate(self):
        for xml_file in ['header.xml', 'footer.xml', 'document.xml']:
            self.super_replace(xml_file)
        dst_file = f'template{self.timestamp()}.docx'
        self.super_save(dst_file)
        return dst_file
        
    def test(self):
        self.render()
        # template_file = self.generate()
        # python_file_path = os.path.join(self.folder, 'test.py')
        # os.system(f'python {python_file_path} {template_file}')

    def render(self):
        python_file_path = os.path.join(self.folder, 'test.py')
        print(f'python {python_file_path}')
        os.system(f'python {python_file_path}')

    def extract(self, res_path):
        dst_path = os.path.join(self.folder, f'{res_path}')
        dst_path = os.path.join(self.folder, f'{self.timestamp()}{res_path}') if os.path.exists(dst_path) else dst_path
        with open(dst_path, 'wb') as f:
            res_bytes = self.get_resource(res_path)
            f.write(res_bytes)

    def write(self, res_file, res_path):
        res_path_ = os.path.join(self.folder, res_file)
        with open(res_path_, 'rb') as f:
            data = f.read()
            self.replace(res_path, data)
        dst_file = os.path.join(self.folder, f'{self.timestamp()}.docx')
        wf.super_save(dst_file)

    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(relative_path)

    @classmethod
    def word2xml(cls, orientation='h'):
        if cls.testing_word:
            cls.extract_document(orientation)
        else:
            cls.new_word(orientation)

    @classmethod
    def xml2word(cls, orientation='h'):
        if cls.testing_xml:
            cls.create_word(orientation)
        else:
            cls.new_xml(orientation)

    @classmethod
    def new_word(cls, orientation):
        docx_file = 'h.docx' if orientation == 'h' else 'v.docx'
        docx_path = cls.get_resource_path(docx_file)
        save_path = f'd:/tmp/{cls.timestamp()}test.docx'
        wf = WordFile(docx_path)
        wf.save(save_path)
        os.startfile(save_path)
        cls.testing_word = save_path

    @classmethod
    def extract_document(cls, orientation):
        wf = WordFile(cls.testing_word)
        save_path = f'd:/tmp/{cls.timestamp()}document.xml'
        wf.save_resource('document.xml', save_path)
        os.startfile(save_path)
        cls.testing_word = ''

    @classmethod
    def new_xml(cls, orientation):
        docx_file = 'h.docx' if orientation == 'h' else 'v.docx'
        docx_path = cls.get_resource_path(docx_file)
        wf = WordFile(docx_path)
        save_path = f'd:/tmp/{cls.timestamp()}document.xml'
        wf.save_resource('document.xml', save_path)
        os.startfile(save_path)
        cls.testing_xml = save_path 

    @classmethod
    def create_word(cls, orientation):
        docx_file = 'h.docx' if orientation == 'h' else 'v.docx'
        docx_path = cls.get_resource_path(docx_file)
        wf = WordFile(docx_path)
        with open(cls.testing_xml, 'rb') as f:
            content = f.read()
            wf['word/document.xml'] = content
            save_path = f'd:/tmp/{cls.timestamp()}test.docx'
            wf.save(save_path)
            os.startfile(save_path)
            cls.testing_xml = ''

    

    
    
if __name__ == '__main__':
    wf = SuperWordFile(r'd:\git\lims\template\inspect\record - 副本','template.docx')
    wf.extract('document.xml')
    exit()
    wf = SuperWordFile('.','123.docx')
    # wf.extract('document.xml')
    # wf.write('document.xml', 'document2.xml')