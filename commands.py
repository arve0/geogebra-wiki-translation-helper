# -*- coding: utf-8 -*-
"""
File: commands.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class which gets all commands with translation from SVN.
"""

from urllib import urlopen
import json
import codecs

class Commands(object):
    """ Class for commands """

    # Variables

    def __init__(self, language=None, language_code=None):
        self.language = language or 'English'
        self.language_code = language_code or 'en'
        self.filename = 'data/commands-%s.json' % (self.language_code,)
        self.commands = None
        self.raw_data = None

        # Infix codes
        if self.language_code == 'nb':
            self.commands_infix = '_no_NO'
        elif self.language_code == 'nn':
            self.commands_infix = '_no_NO_NY'
        elif self.language_code != 'en':
            self.commands_infix = '_' + self.language_code
        else:
            self.commands_infix = ''


    def get_api_url(self):
        """
        Returns URL to command.properties in SVN, for given self.language.
        """
        return 'https://geogebra.googlecode.com/svn/trunk/geogebra/desktop/' + \
           'geogebra/properties/command%s.properties' % (self.commands_infix,)


    def convert_raw_data_to_dictionary(self):
        """ Convert the raw data to a list of dictionaries """
        if self.language_code != 'en':
            # raw data does not include names that are the same in english
            self.load_from_json('data/commands-en.json')
        else: self.commands = {}
        lines = self.raw_data.split('\n')
        for line in lines:
            translation = ''
            words = line.split('=')
            if '.Syntax' not in words[0]:
                if words[0] == 'Command':
                    # Special case
                    continue
                translation = words[1]
            else:
                command = words[0].split('.')[0]
                if translation == '':
                    obj = {
                        command:{
                            'syntax': words[1] # translation == english
                        }
                    }
                else:
                    obj = {
                        command: {
                            'translation': translation,
                            'syntax': words[1]
                        }
                    }
                self.commands.update(obj)


    def load_from_svn(self):
        """
        Load commands from SVN, convert raw data and store them to self.commands
        """
        print 'Fetching from SVN...'
        self.raw_data = urlopen(self.get_api_url()).read().decode('ISO-8859-1')
        self.convert_raw_data_to_dictionary()


    def save_to_json(self):
        """ Stores the data gotten from SVN to a json file. """
        print 'Storing data to: ' + self.filename
        obj = {
            'language': self.language,
            'language_code': self.language_code,
            'commands': self.commands,
        }
        file_ = codecs.open(self.filename, 'w', encoding='utf8')
        # use utf-8 encoding(instead of escaped ascii), to make json files easy
        # to read for humans
        json_str = json.dumps(obj, ensure_ascii=False, encoding='utf8')
        file_.write(json_str)
        file_.close()


    def load_from_json(self, filename=None):
        """ Loads data from json file. """
        if not filename:
            filename = self.filename
        print 'Loading file ' + filename
        file_ = codecs.open(filename, encoding='utf8')
        obj = json.load(file_)
        file_.close()
        self.commands = obj['commands']


    def print_status(self):
        """ Prints number of commands in object. """
        msg = 'Language: %s(%s), Number of commands: %i' \
                % (self.language, self.language_code, len(self.commands))
        print msg
