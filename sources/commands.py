# -*- coding: utf-8 -*-
"""
File: commands.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class Commands: Get commands from SVN. Return as dictionary.
"""


from urllib import urlopen
import re
from language import Language


class Commands(object):
    """ Geogebra commands from SVN as dictionary. """

    def __init__(self, language='en', pages=None):
        """
        Setup language and pages.

        :language: Language code found in language.py.
        :pages: List of wikipages(dict) with title key. Title is used to link
                commands to wikipages(command['wikiid']).
        """
        self.language = Language(language.lower())
        self.commands = {}
        self._raw_data = None
        self.commands_translated = {}
        self.pages = pages


    def get(self):
        """
        Load commands from SVN. Return dictionary of commands.
        """
        if self.language.code != 'en':
            # raw data does not include names that are equal in english
            self._raw_data = urlopen(_en_svn_url()).read()\
                    .decode('ISO-8859-1')
            self.convert_raw_data_to_dictionary()

        print u'Fetching commands from SVN.'
        self._raw_data = urlopen(self._svn_url()).read().decode('latin1')
        self.convert_raw_data_to_dictionary()
        self.validate_commands_dict()
        self.link_pageid()

        return self.commands


    def convert_raw_data_to_dictionary(self):
        """ Convert the raw data from SVN to a dictionary. """
        lines = self._raw_data.split('\n')
        for line in lines:
            words = line.split('=')
            if '.Syntax' not in words[0]:
                # capitalize without lowering all other chars (ex: nPr Command)
                command = _capitalize(words[0])
                key = 'translation'
            else:
                command = _capitalize(words[0].split('.')[0])
                key = 'syntax'
            # raw data is escaped unicode, to keep format(explicit \n), decode
            # as latin1(back to str) -> decode as escaped unicode
            value = _capitalize(words[1])
            value = value.encode('latin1').decode('unicode-escape')
            # two possibilities: english or not english
            # if english -> we got empty dictionary (no key)
            # if not english -> we need to update all properties (key exist)
            # -> test for key for detecting english/not english
            if command in self.commands.iterkeys():
                self.commands[command].update({
                    key: value
                })
            else:
                self.commands.update({
                    command: {
                        key: value
                    }
                })


    def link_pageid(self):
        """
        Find command in wiki. Save pageid as command['wikiid'] on command
        dictionary.
        """
        self.reverse_translated_commands()
        cmd_string = self.commands['Command']['translation']
        cmd_pages = [p for p in self.pages if is_command_page(p, cmd_string)]
        for page in cmd_pages:
            command = page['title'].replace(u' ' + cmd_string, '')
            if command in self.commands_translated.iterkeys():
                en_command = self.commands_translated[command]
                self.commands[en_command].update({
                    'wikiid': page['id']
                })

    def validate_commands_dict(self):
        """
        Check that every command dict has translation key.
        """
        for (command, obj) in self.commands.iteritems():
            if 'translation' not in obj.keys():
                self.commands[command].update({
                    'translation': command
                })


    def reverse_translated_commands(self):
        """
        Map translated commands to English commands (reverse dict).
        """
        for (command, obj) in self.commands.iteritems():
            if 'translation' in obj.keys():
                self.commands_translated.update({
                    obj['translation']: command
                })
            else:
                print u'ERROR: %s does not have a translation property.'\
                        % (command,)


    def _svn_url(self):
        """ Return URL to command.properties in SVN for self.language. """
        return ('http://dev.geogebra.org/svn/branches/wiki/geogebra/properties/'
                + 'command{0}.properties'.format(self.language.commands_infix))


    def print_status(self):
        """ Print number of commands. """
        msg = u'Language: %s(%s), Number of commands: %i' \
                .format(self.language, self.language.code, len(self.commands))
        print msg


def _en_svn_url():
    """
    Return URL to command.properties in SVN for English.
    """
    return 'https://geogebra.googlecode.com/svn/trunk/geogebra/' + \
        'desktop/geogebra/properties/command.properties'

def _capitalize(string):
    """
    Capitalize a string without lowering all other chararcters.
    """
    return string.replace(string[0], string[0].upper(), 1)

def is_command_page(page, command_string):
    """
    Return true if ' Command$' matches page['title'].
    """
    regex = ' ' + command_string + '$'
    match = re.search(regex, page['title'])
    return match != None
