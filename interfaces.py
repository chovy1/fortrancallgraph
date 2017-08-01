# coding=utf8

import re
from utils import assertType
from supertypes import UseTraversalPassenger
from source import Interface

class InterfaceFinder(UseTraversalPassenger):

    def __init__(self):
        self.__types = dict()
        self.__currentType = None
        
    def getResult(self):
        return self.__types
        
    def reset(self):      
        self.__types = dict()
        self.__currentType = None
    
    def parseStatement(self, i, statement, j, module):
        assertType(i, 'i', int) 
        assertType(statement, 'statement', str) 
        assertType(j, 'j', int)
        
        interfaceRegEx = re.compile(r'^INTERFACE\s+(?P<interfacename>[a-z0-9_]+)$', re.IGNORECASE);
        endInterfaceRegEx = re.compile(r'^END\s*INTERFACE(\s+[a-z0-9_]+)?$', re.IGNORECASE);
        procedureRegEx = re.compile(r'^MODULE\s+PROCEDURE\s+(?P<procedurelist>[a-z0-9_\s\,]+)$', re.IGNORECASE);
        
        if self.__currentType is None:
            interfaceRegExMatch = interfaceRegEx.match(statement)
            if interfaceRegExMatch is not None:
                self.__currentType = Interface(interfaceRegExMatch.group('interfacename'))
        else:
            procedureRegExMatch = procedureRegEx.match(statement)
            if procedureRegExMatch is not None:
                for procedure in procedureRegExMatch.group('procedurelist').split(','):
                    self.__currentType.addProcedure(procedure.strip())
            else:
                endInterfaceRegExMatch = endInterfaceRegEx.match(statement)
                if endInterfaceRegExMatch is not None:
                    self.__types[self.__currentType.getName().lower()] = self.__currentType
                    self.__currentType = None
