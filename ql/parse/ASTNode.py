'''
Created on Dec 26, 2016

@author: unimas
'''

from collections import OrderedDict


class Node(object):
    __slots__ = ('type','value','children')
    
    def __init__(self,_type,_value,_children):
        self.type = _type
        self.value = _value
        self.children = _children

    def set_type(self,_type):
        self.type = _type
        
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value
    
    def get_children_count(self):
        return len(self.children)

    def get_children(self):
        return self.children

    def append_children(self,val):
        self.children.append(val)
    
    def to_string(self,depth=0):
        tab = ''
        for i in range(depth):
            i = i
            tab += '\t'
        print( tab + '('+ self.get_type().name)
        if self.value != None:
            print( tab + '\t'+ self.get_value())
        if(self.children != None):
            depth += 1
            for node in self.get_children():
                node.to_string(depth)
        print(tab + ')')

    def sub(self, index):
        """ Get child by index
        """
        def _sub(elm, _index) -> Node:  # provide convenience for coding
            return elm.children[_index]
        return _sub(self, index)

    def sub_token(self, child_type):
        """ Get child by it's token type
        """
        def _sub_type(elm, _type) -> Node:  # provide convenience for coding
            if elm.children:
                for child in elm.children:
                    if child.type == _type:
                        return child
        return _sub_type(self, child_type)
