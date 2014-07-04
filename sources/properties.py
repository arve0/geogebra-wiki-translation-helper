# -*- coding: utf-8 -*-
"""
File: properties.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class Articles: Get wiki articles from SVN. Return as dict.
             Class Commands: Get commands from SVN. Return as dict.
"""


from urllib import urlopen
import re
from language import Language

class Properties(object):
    """
    Super class of Articles and Commands.
    """
    def __init__(self, language='en', pages=None):
        """
        Setup language and pages.

        :language: Language code found in language.py.
        :pages: List of wikipages(dict) with title key. Title is used to link
                articles to wikipages(article['wikiid']).
        """
        self.language = Language(language.lower())
        self.dictionary = {}
        self._raw_data = None
        self.reversed_dictionary = {}
        self.pages = pages or []


    def convert_raw_data_to_dictionary(self):
        """
        Convert the raw data from SVN to a dictionary.
        """
        lines = self._raw_data.split('\n')
        for line in lines:
            if '=' not in line:
                # only parse lines with equal sign in it
                continue
            words = line.split('=')
            if '.Syntax' not in words[0]:
                # capitalize without lowering all other chars (ex: nPr Command)
                prop = capitalize(words[0])
                key = 'translation'
            else:
                prop = capitalize(words[0].split('.')[0])
                key = 'syntax'
            # raw data is escaped unicode, to keep format(explicit \n), decode
            # as latin1(back to str) -> decode as escaped unicode
            value = capitalize(words[1])
            value = value.encode('latin1').decode('unicode-escape')
            # two possibilities: english or not english
            # if english -> we got empty dictionary (no key)
            # if not english -> we need to update all articles (key exist)
            # -> test for key for detecting english/not english
            if prop in self.dictionary.iterkeys():
                self.dictionary[prop].update({
                    key: value,
                })
            else:
                self.dictionary.update({
                    prop: {
                        key: value,
                    }
                })


    def validate_dictionary(self):
        """
        Check that every object in dict has translation key. If not found, use
        english keyword as "translation".
        """
        for (key, obj) in self.dictionary.iteritems():
            if 'translation' not in obj.keys():
                self.dictionary[key].update({
                    'translation': key
                })


    def reverse_dictionary(self):
        """
        Map translated articles to English articles (reverse dict).
        """
        for (key, obj) in self.dictionary.iteritems():
            if 'translation' in obj.keys():
                self.reversed_dictionary.update({
                    obj['translation']: key
                })
            else:
                print u'ERROR: %s does not have a translation property.'\
                        % (key,)



class Articles(Properties):
    """ Geogebra article articles from SVN as dictionary. """

    def __init__(self, language='en', pages=None):
        """
        Setup language and pages.

        :language: Language code found in language.py.
        :pages: List of wikipages(dict) with title key. Title is used to link
                articles to wikipages(article['wikiid']).
        """
        super(Articles, self).__init__(language=language, pages=pages)


    def get(self):
        """
        Load articles from SVN. Return dictionary of articles.
        """
        if self.language.code != 'en':
            # raw data does not include names that are equal in english
            url = _svn_url() + 'wiki.properties'
            self._raw_data = urlopen(url).read().decode('latin1')
            self._find_articles()
            self.convert_raw_data_to_dictionary()
        if self.language.code == 'nn':
            # nn is superset of nb, load nb first
            url = _svn_url() + 'wiki_no_NO.properties'
            self._raw_data = urlopen(url).read().decode('latin1')
            self._find_articles()
            self.convert_raw_data_to_dictionary()

        print u'Fetching articles from SVN.'
        url = _svn_url() + self._wiki_properties()
        self._raw_data = urlopen(url).read().decode('latin1')
        self._find_articles()
        self.convert_raw_data_to_dictionary()

        self.validate_dictionary()
        self.link_pageid()

        return self.dictionary

    def link_pageid(self):
        """
        Find articles in wiki. Save pageid as 'wikiid' on object in dictionary.
        """
        self.reverse_dictionary()

        for page in self.pages:
            key = page['title']
            if key in self.reversed_dictionary.iterkeys():
                en_key = self.reversed_dictionary[key]
                self.dictionary[en_key].update({
                    'wikiid': page['id']
                })

    def _wiki_properties(self):
        """ Return wiki properties for self.language. """
        return 'wiki{0}.properties'.format(self.language.properties_infix)


    def _find_articles(self):
        """
        Removes lines from self._raw_data which isn't wiki articles.
        """
        # get java generator
        url = _svn_url().replace('properties', 'wiki') + 'ImportGenerator.java'
        generator = urlopen(url).read().decode('latin1')

        # find articles
        regex = r'\t\taddArticle\(sb, "([a-zA-Z]+)"'
        articles = re.findall(regex, generator)

        articles_only = u''
        for line in self._raw_data.split('\n'):
            keyword = line.split('=')[0]
            if keyword in articles:
                articles_only += line + '\n'

        self._raw_data = articles_only



class Commands(Properties):
    """ Geogebra commands from SVN as dictionary. """

    def __init__(self, language='en', pages=None):
        """
        Setup language and pages.

        :language: Language code found in language.py.
        :pages: List of wikipages(dict) with title key. Title is used to link
                commands to wikipages(command['wikiid']).
        """
        super(Commands, self).__init__(language=language, pages=pages)


    def get(self):
        """
        Load commands from SVN. Return dictionary of commands.
        """
        # load several times from SVN, instead of circular depency
        if self.language.code != 'en':
            # raw data does not include names that are equal in english
            url = _svn_url() + 'command.properties'
            self._raw_data = urlopen(url).read().decode('latin1')
            self.convert_raw_data_to_dictionary()
        if self.language.code == 'nn':
            # superset of nb, load nb first
            url = _svn_url() + 'command_no_NO.properties'
            self._raw_data = urlopen(url).read().decode('latin1')
            self.convert_raw_data_to_dictionary()

        print u'Fetching commands from SVN.'
        url = _svn_url() + self._command_properties()
        self._raw_data = urlopen(url).read().decode('latin1')
        self.convert_raw_data_to_dictionary()
        self.validate_dictionary()
        self.link_pageid()

        return self.dictionary


    def link_pageid(self):
        """
        Find commands in wiki. Save pageid as 'wikiid' on object in dictionary.
        """
        self.reverse_dictionary()
        cmd_string = self.dictionary['Command']['translation']

        # only loop command pages
        pages = [p for p in self.pages if self.is_command_page(p)]
        for page in pages:
            key = page['title'].replace(u' ' + cmd_string, '')
            if key in self.reversed_dictionary.iterkeys():
                en_key = self.reversed_dictionary[key]
                self.dictionary[en_key].update({
                    'wikiid': page['id']
                })


    def is_command_page(self, page):
        """
        Return true if ' Command$' matches page['title'].
        """
        command_string = self.dictionary['Command']['translation']
        regex = ' ' + command_string + '$'
        match = re.search(regex, page['title'])
        return match != None


    def _command_properties(self):
        """ Return command properties for self.language. """
        return 'command{0}.properties'.format(self.language.properties_infix)



def capitalize(string):
    """
    Capitalize a string without lowering all other chararcters.
    """
    return string.replace(string[0], string[0].upper(), 1)


def _svn_url():
    """ Return URL to SVN. """
    return 'http://dev.geogebra.org/svn/branches/wiki/geogebra/properties/'
