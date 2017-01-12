import sys
from typing import List, Tuple, Dict
from ply.lex import lex
from ply.yacc import yacc

from ql.parse import lexer, parser as grammar
from ql.parse.parser import TK
from ql.parse.ASTNode import Node
from parser.utility import recursive_import

__debug = False
__lexer = None
__parser = None
ElementDict = None
ProcessorDict = None


def init(optimize, debug):
    """ Init parser
    """
    global __debug, __lexer, __parser, ElementDict, ProcessorDict
    __debug = debug
    __lexer = lex(module=lexer, optimize=optimize, debug=debug)
    __parser = yacc(debug=debug, module=grammar)

    ElementDict, ProcessorDict = {}, {}

    recursive_import(sys.modules[__name__])

    for element_class in Element.__subclasses__():
        if hasattr(element_class, 'mapping'):
            ElementDict[element_class.mapping] = element_class

    for processor_class in Processor.__subclasses__():
        ProcessorDict[processor_class.mapping] = processor_class
        

def parse(sql):
    return __parser.parse(input=sql, lexer=__lexer.clone(), debug=__debug)


def chk_explain(sql) -> Tuple[Node, bool]:
    _ast = parse(sql)
    if _ast.type == TK.TOK_EXPLAIN:
        return _ast.sub(0), True
    else:
        return _ast, False


class Processor(object):
    """ AST & ES Mapping Class
    """

    def __init__(self, sql, _ast: Node, _rst=None, explain_only=False):
        self.sql = sql
        self.ast = _ast
        self.rst = _rst
        self.explain_only = explain_only

    @staticmethod
    def execute(sql):
        _ast, explain_only = chk_explain(sql)
        _rst = None
        if _ast.type in ElementDict:
            rst_class = ElementDict[_ast.type]
            _rst = rst_class(_ast)

        processor_class = ProcessorDict.get(_ast.type, Processor)
        processor = processor_class(sql, _ast, _rst, explain_only)

        return processor.rst.dsl()


# ------------------------------------------------------------------------------------
#  common sql element
# ------------------------------------------------------------------------------------

class Element(object):
    pass


class Attribute(Element):
    __slots__ = ('key', 'value')

    def __init__(self, tree: Node = None):
        if tree.type == TK.TOK_KEY_VALUE:
            self.key = tree.sub(0).value
            self.value = tree.sub(1).value


class AttributeList(List[Attribute]):

    def __init__(self, attributes):
        for attribute in attributes:
            self.append(Attribute(attribute))


class AttributeDict(Dict):

    def __init__(self, attributes):
        for attribute in attributes:
            item = Attribute(attribute)
            self[item.key] = item.value

    def dsl(self):
        return dict(self)


class ItemList(list):

    def __init__(self, items):
        for item in items:
            if item.type == TK.TOK_VALUE:
                self.append(item.value)
            elif item.type == TK.TOK_DICT:
                self.append(AttributeDict(item.children))


class TableName(Element):
    __slots__ = ('index_name', 'doc_type')

    def __init__(self, tree):
        for item in tree:
            if item.type == TK.TOK_DOT:
                self.index_name = item.sub(0).value
                self.doc_type = item.sub(1).value
