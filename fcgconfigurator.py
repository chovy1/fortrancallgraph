import os
from assertions import assertType
from printout import printError

CFG_SOURCE_DIRS = 'SOURCE_DIRS'
CFG_SOURCE_DIRS_LEGACY = 'SOURCE_DIR'
CFG_ASSEMBLER_DIRS = 'ASSEMBLER_DIRS'
CFG_ASSEMBLER_DIRS_LEGACY = 'ASSEMBLER_DIR'
CFG_SPECIAL_MODULE_FILES = 'SPECIAL_MODULE_FILES'
CFG_SOURCE_FILES_PREPROCESSED = 'SOURCE_FILES_PREPROCESSED'
CFG_CACHE_DIR = 'CACHE_DIR'
CFG_EXCLUDE_MODULES = 'EXCLUDE_MODULES'
CFG_IGNORE_GLOBALS_FROM_MODULES = 'IGNORE_GLOBALS_FROM_MODULES'
CFG_IGNORE_DERIVED_TYPES = 'IGNORE_DERIVED_TYPES'
CFG_ABSTRACT_TYPES = 'ABSTRACT_TYPE_IMPLEMENTATIONS'
CFG_ALWAYS_FULL_TYPES = 'ALWAYS_FULL_TYPES'
        
def loadFortranCallGraphConfiguration(configFile, incomplete = False, baseConfig = {}):
    assertType(configFile, 'configFile', str, True)

    if configFile:
        configFile = configFile.strip('"\'')
    else:
        configFile = 'config_fortrancallgraph.py'
    originalConfigFile = configFile
    if not os.path.isfile(configFile):
        configFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), originalConfigFile)
    if not os.path.isfile(configFile):
        configFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', originalConfigFile)
    if not os.path.isfile(configFile):
        printError('Config file not found: ' + originalConfigFile, location='FortranCallGraph')
        return None
        
    config = baseConfig
    
    with open(configFile) as f:
        code = compile(f.read(), configFile, 'exec')
        globalNamespace = globals()
        exec(code, globalNamespace, config)
    
    configError = False
    if CFG_SOURCE_DIRS not in config and CFG_SOURCE_DIRS_LEGACY in config:
        config[CFG_SOURCE_DIRS] = config[CFG_SOURCE_DIRS_LEGACY]
    if CFG_SOURCE_DIRS not in config or not config[CFG_SOURCE_DIRS]:
        if not incomplete:
            printError('Missing config variable: ' + CFG_SOURCE_DIRS, location='FortranCallGraph')
            configError = True
    elif isinstance(config[CFG_SOURCE_DIRS], str):
        config[CFG_SOURCE_DIRS] = [config[CFG_SOURCE_DIRS]]

    if CFG_ASSEMBLER_DIRS not in config and CFG_ASSEMBLER_DIRS_LEGACY in config:
        config[CFG_ASSEMBLER_DIRS] = config[CFG_ASSEMBLER_DIRS_LEGACY]
    if CFG_ASSEMBLER_DIRS not in config or not config[CFG_ASSEMBLER_DIRS]:
        if not incomplete:
            printError('Missing config variable: ' + CFG_ASSEMBLER_DIRS, location='FortranCallGraph')
            configError = True
    elif isinstance(config[CFG_ASSEMBLER_DIRS], str):
        config[CFG_ASSEMBLER_DIRS] = [config[CFG_ASSEMBLER_DIRS]]
        
    if CFG_SPECIAL_MODULE_FILES not in config or not config[CFG_SPECIAL_MODULE_FILES]:
        config[CFG_SPECIAL_MODULE_FILES] = {}
        
    if CFG_SOURCE_FILES_PREPROCESSED not in config or not config[CFG_SOURCE_FILES_PREPROCESSED]:
        config[CFG_SOURCE_FILES_PREPROCESSED] = False

    if CFG_CACHE_DIR not in config or not config[CFG_CACHE_DIR]:
        config[CFG_CACHE_DIR] = None

    if CFG_EXCLUDE_MODULES not in config or not config[CFG_EXCLUDE_MODULES]:
        config[CFG_EXCLUDE_MODULES] = []

    if CFG_IGNORE_GLOBALS_FROM_MODULES not in config or not config[CFG_IGNORE_GLOBALS_FROM_MODULES]:
        config[CFG_IGNORE_GLOBALS_FROM_MODULES] = []

    if CFG_IGNORE_DERIVED_TYPES not in config or not config[CFG_IGNORE_DERIVED_TYPES]:
        config[CFG_IGNORE_DERIVED_TYPES] = []

    if CFG_ALWAYS_FULL_TYPES not in config or not config[CFG_ALWAYS_FULL_TYPES]:
        config[CFG_ALWAYS_FULL_TYPES] = []

    if CFG_ABSTRACT_TYPES not in config or not config[CFG_ABSTRACT_TYPES]:
        config[CFG_ABSTRACT_TYPES] = {}
    
    if configError:
        return None
    
    return config