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


# root = E.root(
#     E.child1("Content for child 1"),
#     E.child2("Content for child 2")
# )


# a = etree.tostring(root)
# print(a)
# tree = Tree(a)
# print(bytes(tree))
# tree += E.haha(id='12')
# print(bytes(tree))
# # print(type(tree))


