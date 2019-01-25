from __future__ import print_function
import sys

def printInline(line):
    print(str(line), end='')

def printLine(line = ''):
    print(str(line))

def printLines(lines):
    print('\n'.join(map(str, lines)))
    
def printError(line, location = ''):
    msg = '*** ERROR'
    if location:
        msg += ' [' + location + ']'
    msg += ': ' + str(line) + ' ***'
    print(msg, file=sys.stderr)
    
def printErrorAndExit(exitCode, line, location = ''):
    printError(line, location)
    sys.exit(exitCode)
    
def printWarning(line, location = ''):
    msg = '*** WARNING'
    if location:
        msg += ' [' + location + ']'
    msg += ': ' + str(line) + ' ***'
    print(msg, file=sys.stderr)