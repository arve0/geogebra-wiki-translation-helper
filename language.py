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
        'bs': u'Početna strana',
        'ca': u'Pàgina principal',
        'cs': u'Hlavní stránka',
        'da': u'Forside',
        'de': u'Hauptseite',
        'es': u'Página Principal',
        'et': u'Pealeht',
        'fa': u'صفحه اصلی',
        'fr': u'Accueil',
        'he': u'עמוד מרכזי',
        'hr': u'Glavna stranica',
        'hu': u'Főoldal',
        'is': u'Aðalsíða',
        'it': u'Pagina principale',
        'kk': u'Басты бет',
        'ko': u'메인 페이지',
        'lt': u'Pagrindinis puslapis',
        'mk': u'Главна страна',
        'pl': u'Strona główna',
        'pt': u'Página Principal',
        'sk': u'Hlavná stránka',
        'sl': u'Glavna stran',
        'tr': u'Ana Sayfa',
        'zh': u'首页',
    }

    def __init__(self, code):
        self.code = code.lower()
        try:
            self.name = self._languages[code]
        except KeyError:
            raise NameError('Language code "' + code + '" not found. '\
                'Please add it to language.py.')

	# set properties_infix
        if self.code == 'nb':
            self.properties_infix = '_no_NO'
        elif self.code == 'nn':
            self.properties_infix = '_no_NO_NY'
        elif self.code != 'en':
            self.properties_infix = '_' + self.code
        else:
            self.properties_infix = ''


    def __str__(self):
        """
        Returns language(code)
        """
        return u'{0}({1})'.format(self.name, self.code)
