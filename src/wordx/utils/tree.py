from lxml import etree
from lxml.builder import E


class Tree:
    def __init__(self, data):
        self.instance = etree.fromstring(data)

    def __add__(self, other):
        self.instance.append(other)
        return self
        
    def __bytes__(self):
        return etree.tostring(self.instance)


