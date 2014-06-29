# -*- coding: utf-8 -*-
""" Abstraction for languages """

class Language(object):
    """
    Class to hold properties of languages, for easier notation (ex lang.code)

    Raises NameError if code isn't found.
    """

    _languages = {
        'en': u'English',
        'nb': u'Norsk bokmål',
        'nn': u'Norsk nynorsk',
    }

    def __init__(self, code):
        self.code = code
        try:
            self.name = self._languages[code]
        except KeyError as error:
            raise NameError('ERROR: Language code "' + code + '" not found. '\
                'Please add it to Language._languages in language.py')

	# set commands_infix
        if self.code == 'nb':
            self.commands_infix = '_no_NO'
        elif self.code == 'nn':
            self.commands_infix = '_no_NO_NY'
        elif self.code != 'en':
            self.commands_infix = '_' + self.code
        else:
            self.commands_infix = ''


    def __str__(self):
        """
        Returns language(code)
        """
        return u'{0}({1})'.format(self.name, self.code)
