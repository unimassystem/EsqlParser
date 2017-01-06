'''
Created on Dec 26, 2016

@author: unimas
'''




class ASTNode(object):
    __slots__ = ('tokType','tokValue','children')
    
    def __init__(self,tokType,tokValue,children):
        self.tokType = tokType
        self.tokValue = tokValue
        self.children = children

    def setTokType(self,tokType):
        self.tokType = tokType
        
    def getTokType(self):
        return self.tokType
    
    def getTokValue(self):
        return self.tokValue
    
    def getChildrenCount(self):
        return len(self.children)
    
    def getChild(self,i):
        return self.children[i]
    
    def getChildren(self):
        return self.children

    def appendChildren(self,val):
        return self.children.append(val)
    
    def toStringTree(self,depth=0):
        tab = ''
        for i in range(depth):
            i = i
            tab += '\t'
        print( tab + '('+ self.tokType.name)
        if self.tokValue != None:
            print( tab + '\t'+ self.tokValue)
        if(self.getChildren() != None):
            depth += 1
            for node in self.getChildren():
                node.toStringTree(depth)
        print(tab + ')')
        

