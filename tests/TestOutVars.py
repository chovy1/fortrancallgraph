#!/usr/bin/python

import unittest
import os
import sys

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCE_DIR = TEST_DIR + '/samples/outvars'
ASSEMBLER_DIR = SOURCE_DIR

FCG_DIR = TEST_DIR + '/..'
sys.path.append(FCG_DIR)

from assembler import FromAssemblerCallGraphBuilder
from source import SourceFiles, SubroutineFullName
from usetraversal import UseTraversal
from trackvariable import VariableTracker
from globals import GlobalVariableTracker

''' 
Tests whether assignments of function results are tracked correctly
'''
class OutVarsTest(unittest.TestCase):
    def setUp(self):
        specialModuleFiles = {}
        callGraphBuilder = FromAssemblerCallGraphBuilder(ASSEMBLER_DIR, specialModuleFiles)
        self.sourceFiles = SourceFiles(SOURCE_DIR, specialModuleFiles);
        
        self.srcFile = SOURCE_DIR + '/outvars.f90'
        self.assFile = ASSEMBLER_DIR + '/outvars.s'
        self.filesExist = os.path.exists(self.srcFile) and os.path.exists(self.assFile)
        
        self.get = SubroutineFullName('__outvars_MOD_get')
        self.callGraphGet = callGraphBuilder.buildCallGraph(self.get)
        
        self.testFunc1 = SubroutineFullName('__outvars_MOD_testFunc1')
        self.callGraphTestFunc1 = callGraphBuilder.buildCallGraph(self.testFunc1)
        
        self.testFunc2 = SubroutineFullName('__outvars_MOD_testFunc2')
        self.callGraphTestFunc2 = callGraphBuilder.buildCallGraph(self.testFunc2)
        
    def testAssemberFileExists(self):
        self.assertTrue(os.path.exists(self.srcFile), 'Test will fail. Source file not found: ' + self.srcFile)
        self.assertTrue(os.path.exists(self.assFile), 'Test will fail. Assembler file not found: ' + self.assFile)

    def testCallGraphs(self):
        if not self.filesExist:
            self.skipTest('Files not there')
        
        self.assertEqual({'get'}, set(map(SubroutineFullName.getSimpleName, self.callGraphGet.getAllSubroutineNames())))
        self.assertEqual({'testfunc1', 'get'}, set(map(SubroutineFullName.getSimpleName, self.callGraphTestFunc1.getAllSubroutineNames())))
        self.assertEqual({'testfunc2', 'part'}, set(map(SubroutineFullName.getSimpleName, self.callGraphTestFunc2.getAllSubroutineNames())))
                
    def testSourceFiles(self):
        if not self.filesExist:
            self.skipTest('Files not there')
        
        sourceFile = self.sourceFiles.findSourceFile('outvars.f90')
        self.assertIsNotNone(sourceFile)
        moduleFile = self.sourceFiles.findModuleFile('outvars')
        self.assertIsNotNone(moduleFile)
        self.assertEqual(sourceFile, moduleFile)
        self.assertEqual(1, len(sourceFile.getModules()))

        module = sourceFile.getModule('outvars')
        self.assertIsNotNone(module)
        
        simpleNames = set(module.getSubroutines().keys())
        self.assertEqual({'get', 'part', 'testfunc1', 'testfunc2'}, simpleNames)
        
        
    def testOutArguments(self):
        if not self.filesExist:
            self.skipTest('Files not there')
         
        module = self.sourceFiles.findModule('outvars')
        self.assertIsNotNone(module)
        t1 = module.getVariable('t1')
        self.assertIsNotNone(t1)

        useTraversal = UseTraversal(self.sourceFiles, [])
        useTraversal.parseModules(self.testFunc1)
        tracker = VariableTracker(self.sourceFiles, [], [], useTraversal.getInterfaces(), useTraversal.getTypes())
        self.assertEqual(0, len(tracker.outAssignments))
        
        refs = tracker.trackVariables([t1], self.callGraphGet)
        self.assertFalse(refs)
        self.assertEqual(1, len(tracker.outAssignments))
                 
    def testArgumentAsFunctionResult(self):
        if not self.filesExist:
            self.skipTest('Files not there')
         
        useTraversal = UseTraversal(self.sourceFiles, [])
        useTraversal.parseModules(self.testFunc2)
        tracker = VariableTracker(self.sourceFiles, [], [], useTraversal.getInterfaces(), useTraversal.getTypes())
         
        refs = tracker.trackDerivedTypeArguments(self.callGraphTestFunc2)
        globalVars = set([ref.getExpression() for ref in refs])
        self.assertEqual({'mother%child%second'}, globalVars)
                 
    def testGlobalAsFunctionResult(self):
        if not self.filesExist:
            self.skipTest('Files not there')
         
        useTraversal = UseTraversal(self.sourceFiles, [])
        useTraversal.parseModules(self.testFunc1)
        tracker = GlobalVariableTracker(self.sourceFiles, [], [], [], useTraversal.getInterfaces(), useTraversal.getTypes())
         
        refs = tracker.trackGlobalVariables(self.callGraphTestFunc1)
        globalVars = set([ref.getExpression() for ref in refs])
        self.assertEqual({'t1%first'}, globalVars)
        
if __name__ == "__main__":
    unittest.main()