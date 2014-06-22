# -*- coding: utf-8 -*-
""" Common properties """

class Language(object):
    """ Class to hold properties of languages, for easier notation (ex lang.code) """
    self.code='en'
    self.name='English'
    def __init__(self, code=None, name=None):
        if code:
            self.code = code
        if name:
            self.name = name
        
# global variables
LANGUAGES = [
    Language(),
    Language(name='Norsk bokmål', code='nb'),
    Language(name='Norsk nynorsk', code='nn'),
]
