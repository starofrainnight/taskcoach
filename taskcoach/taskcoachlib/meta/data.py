name = 'Task Coach'
description = 'Your friendly task manager'
version = '0.24'
date = 'February 26, 2005'
author = 'Frank Niessink'
author_email = 'frank@niessink.com'
url = 'http://taskcoach.niessink.com/'
copyright = 'Copyright (C) 2004-2005 Frank Niessink'
license = 'GNU GENERAL PUBLIC LICENSE Version 2, June 1991'
platform = 'Any'
filename = 'TaskCoach'
pythonversion = '2.3'
wxpythonversion = '2.5.3.1'

def __createDict(locals):
    ''' Provide the local variables as a dictionary for use in string
    formatting. See e.g. meta/help.py. '''
    metaDict = {}
    for key in locals:
        if not key.startswith('__'):
            metaDict[key] = locals[key]
    return metaDict

metaDict = __createDict(locals())

