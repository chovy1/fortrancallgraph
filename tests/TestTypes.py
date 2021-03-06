#!/usr/bin/python

import unittest
import os
import sys
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCE_DIR = TEST_DIR + '/samples/types'
ASSEMBLER_DIR = SOURCE_DIR

FCG_DIR = TEST_DIR + '/..'
sys.path.append(FCG_DIR)

from source import SourceFiles, SubroutineFullName
from usetraversal import UseTraversal


class TestTypes(unittest.TestCase):
    def setUp(self):
        
        self.srcFile = SOURCE_DIR + '/types.f90'
        self.fileExist = os.path.exists(self.srcFile)
        
        specialModuleFiles = {}
        sourceFiles = SourceFiles(SOURCE_DIR, specialModuleFiles);
        root = SubroutineFullName('__types_MOD_test')
        self.module = sourceFiles.findModule('types')
        
        self.usetraversal = UseTraversal(sourceFiles)
        self.usetraversal.parseModules(root)
        self.types = self.usetraversal.getTypes()
        
    def testFileExists(self):
        self.assertTrue(self.fileExist, 'Test will fail. Source file not found: ' + self.srcFile)

    def testSourceFiles(self):
        if not self.fileExist:
            self.skipTest('File not there')
         
        self.assertIsNotNone(self.module)
        self.assertEqual(1, len(self.module.getSubroutines()))
        self.assertEqual(4, len(self.module.getVariables()))
         
        simpleNames = set((self.module.getVariables().keys()))
        self.assertEqual({'var0', 'var1', 'var2', 'var3'}, simpleNames)
            
    def testUseTraversal(self):
        if not self.fileExist:
            self.skipTest('Files not there')
        
        self.assertEqual(0, len(self.usetraversal.getInterfaces()))
        self.assertEqual(10, len(self.usetraversal.getTypes()))
            
    def testType0FromModA(self):
        var0 = self.module.getVariable('var0')
        self.assertIsNotNone(var0)
        self.assertEqual('TYPE(type0)', var0.getTypeName())
        self.assertTrue(var0.hasDerivedType())
        self.assertEqual('type0', var0.getDerivedTypeName())
        
        type0 = self.types.getTypeOfVariable(var0)
        self.assertIsNotNone(type0)
        self.assertEqual('INTEGER', type0.getMember('member').getTypeName())
        self.assertEqual('moda', type0.getModule().getName())
        self.assertFalse(type0.isAbstract())
        self.assertTrue(type0.isPublic())
        self.assertFalse(type0.isPrivate())
            
    def testType1FromModB(self):
        var1 = self.module.getVariable('var1')
        self.assertIsNotNone(var1)
        self.assertEqual('TYPE(type1)', var1.getTypeName())
        self.assertTrue(var1.hasDerivedType())
        self.assertEqual('type1', var1.getDerivedTypeName())
        self.assertFalse(var1.isTypeAvailable())
       
        type1 = self.types.getTypeOfVariable(var1)
        self.assertIsNotNone(type1)
        self.assertEqual('type1', type1.getName())
        self.assertEqual('REAL', type1.getMember('member').getTypeName())
        self.assertEqual('modb', type1.getModule().getName())
        self.assertFalse(type1.isAbstract())
        self.assertFalse(type1.isPublic())
        self.assertTrue(type1.isPrivate())
        
        var1.setType(type1)
        self.assertTrue(var1.isTypeAvailable())
            
    def testAliasTypeBFromModB(self):
        var2 = self.module.getVariable('var2')
        self.assertIsNotNone(var2)
        self.assertEqual('TYPE(typeB)', var2.getTypeName())
        self.assertTrue(var2.hasDerivedType())
        self.assertEqual('typeb', var2.getDerivedTypeName())
        self.assertFalse(var2.isTypeAvailable())
        
        type2 = self.types.getTypeOfVariable(var2)
        self.assertIsNotNone(type2)
        self.assertEqual('type2', type2.getName())
        self.assertEqual('REAL', type2.getMember('member').getTypeName())
        self.assertEqual('modb', type2.getModule().getName())
        self.assertFalse(type2.isAbstract())
        self.assertFalse(type2.isPublic())
        self.assertFalse(type2.isPrivate())
        
        var2.setType(type2)
        self.assertTrue(var2.isTypeAvailable())
            
    def testWildcardType3FromModC(self):
        var3 = self.module.getVariable('var3')
        self.assertIsNotNone(var3)
        self.assertEqual('TYPE(type3)', var3.getTypeName())
        self.assertTrue(var3.hasDerivedType())
        self.assertEqual('type3', var3.getDerivedTypeName())
        self.assertFalse(var3.isTypeAvailable())
       
        type3 = self.types.getTypeOfVariable(var3)
        self.assertIsNotNone(type3)
        self.assertEqual('type3', type3.getName())
        self.assertEqual('TYPE(typeA)', type3.getMember('member1').getTypeName())
        self.assertEqual('modc', type3.getModule().getName())
        self.assertFalse(type3.isAbstract())
        self.assertFalse(type3.isPublic())
        self.assertFalse(type3.isPrivate())
        
        var3.setType(type3)
        self.assertTrue(var3.isTypeAvailable())

        type2 = type3.getExtends()
        self.assertIsNotNone(type2)
        self.assertEqual('type2', type2.getName())
        self.assertEqual('modc', type2.getModule().getName())
        self.assertTrue(type2.isAbstract())
        self.assertTrue(type3.isSubtypeOf(type2))
        self.assertFalse(type2.isSubtypeOf(type3))

        member1 = type3.getMember('member1')
        self.assertIsNotNone(member1)
        self.assertEqual('TYPE(typeA)', member1.getTypeName())
        self.assertTrue(member1.hasDerivedType())
        self.assertTrue(member1.isTypeAvailable())
        
        type1 = self.types.getTypeOfVariable(member1)
        self.assertIsNotNone(type1)
        self.assertEqual('type1', type1.getName())
        self.assertEqual('INTEGER', type1.getMember('member').getTypeName())
        self.assertEqual('moda', type1.getModule().getName())
        self.assertFalse(type1.isAbstract())
        
if __name__ == "__main__":
    unittest.main()